"""Testes unitários de todas as questões da Lista 2.

Uso:
    python executa_testes.py              # todas as questões
    python executa_testes.py 6 8          # somente as questões 6 e 8
    python executa_testes.py base         # somente pilha.py e fila.py
    python executa_testes.py -v           # um teste por linha
    python executa_testes.py --resumo     # somente a tabela final
"""

import collections
import io
import itertools
import random
import signal
import string
import sys
import unittest
from array import array
from collections import Counter

from fila import FilaStr, FilaTAD
from pilha import PilhaInt, PilhaStr, PilhaTAD
from questao_um import Deque, FilaDeque, PilhaDeque
from questao_dois import Pilha2F
from questao_tres import Fila2P
from questao_quatro import (
    inverte_pilha_com_duas_pilhas,
    inverte_pilha_com_fila,
    inverte_pilha_com_pilha,
)
from questao_cinco import inverte_fila_com_duas_filas, inverte_fila_com_pilha
from questao_seis import PilhaMin
from questao_sete import (
    computa_polonesa_reversa,
    converte_parentizada_para_polonesa_reversa,
)
from questao_oito import (
    PegaEntreMaiores,
    PegaEntreMaioresNaoOrdenado,
    PegaEntreMaioresOrdEfic,
    PegaEntreMaioresOrdInef,
    PegaEntreMaioresQuickSDelect,
    quick_sort,
)
from questao_nove import SacoVaiEVem


# ============================================================
# Apoio: limite de tempo, auxiliares e cenários comuns de Pilha e Fila
# ============================================================

LETRAS = string.ascii_letters + string.digits


class TempoEsgotado(AssertionError):
    pass


class CasoDeTeste(unittest.TestCase):
    """TestCase que falha se um teste demorar mais que LIMITE_SEGUNDOS."""

    LIMITE_SEGUNDOS = 1

    def setUp(self):
        super().setUp()

        if not hasattr(signal, 'SIGALRM'):  # Windows: sem proteção de tempo
            return

        def estourou(sinal, quadro):
            raise TempoEsgotado(
                f'Teste excedeu {self.LIMITE_SEGUNDOS}s (possível laço infinito)'
            )

        anterior = signal.signal(signal.SIGALRM, estourou)
        signal.setitimer(signal.ITIMER_REAL, self.LIMITE_SEGUNDOS)

        def restaura():
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, anterior)

        self.addCleanup(restaura)


def empilha_tudo(pilha, valores):
    for valor in valores:
        pilha.empilha(valor)
    return pilha


def esvazia_pilha(pilha):
    """Desempilha tudo e devolve os valores na ordem topo -> base."""
    valores = []
    while pilha.tam > 0:
        valores.append(pilha.desempilha())
    return valores


def enfileira_tudo(fila, valores):
    for valor in valores:
        fila.enfileira(valor)
    return fila


def esvazia_fila(fila):
    """Desenfileira tudo e devolve os valores na ordem frente -> fim."""
    valores = []
    while fila.tam > 0:
        valores.append(fila.desenfileira())
    return valores


class ContratoPilha:
    """Cenários de uma Pilha de caracteres. Subclasses definem cria(n_max)."""

    def cria(self, n_max):
        raise NotImplementedError

    def test_satisfaz_pilha_tad(self):
        self.assertIsInstance(self.cria(4), PilhaTAD)

    def test_ordem_lifo(self):
        pilha = self.cria(5)
        empilha_tudo(pilha, 'abcde')
        self.assertEqual([pilha.desempilha() for _ in range(5)], list('edcba'))

    def test_um_elemento(self):
        pilha = self.cria(1)
        pilha.empilha('x')
        self.assertEqual(pilha.topo(), 'x')
        self.assertEqual(pilha.desempilha(), 'x')

    def test_topo_nao_remove(self):
        pilha = self.cria(3)
        empilha_tudo(pilha, 'ab')
        self.assertEqual(pilha.topo(), 'b')
        self.assertEqual(pilha.topo(), 'b')
        self.assertEqual(pilha.desempilha(), 'b')
        self.assertEqual(pilha.topo(), 'a')
        self.assertEqual(pilha.desempilha(), 'a')

    def test_topo_acompanha_cada_empilha(self):
        pilha = self.cria(4)
        for letra in 'wxyz':
            pilha.empilha(letra)
            self.assertEqual(pilha.topo(), letra)

    def test_operacoes_intercaladas(self):
        pilha = self.cria(4)
        empilha_tudo(pilha, 'ab')
        self.assertEqual(pilha.desempilha(), 'b')
        empilha_tudo(pilha, 'cd')
        self.assertEqual(pilha.desempilha(), 'd')
        self.assertEqual(pilha.desempilha(), 'c')
        pilha.empilha('e')
        self.assertEqual(pilha.desempilha(), 'e')
        self.assertEqual(pilha.desempilha(), 'a')

    def test_elementos_repetidos(self):
        pilha = self.cria(6)
        empilha_tudo(pilha, 'aabbaa')
        self.assertEqual([pilha.desempilha() for _ in range(6)], list('aabbaa'))

    def test_reuso_apos_encher_e_esvaziar(self):
        pilha = self.cria(3)
        for rodada in ('abc', 'xyz', 'mno'):
            empilha_tudo(pilha, rodada)
            self.assertEqual(
                [pilha.desempilha() for _ in range(3)], list(reversed(rodada))
            )

    def test_libera_executa(self):
        pilha = self.cria(3)
        empilha_tudo(pilha, 'ab')
        pilha.libera()

    def test_aleatorio_contra_modelo(self):
        rng = random.Random(2024)
        capacidade = 6
        pilha = self.cria(capacidade)
        modelo = []

        for _ in range(400):
            if rng.random() < 0.55 and len(modelo) < capacidade:
                letra = rng.choice(LETRAS)
                pilha.empilha(letra)
                modelo.append(letra)
            elif modelo:
                self.assertEqual(pilha.desempilha(), modelo.pop())

            if modelo:
                self.assertEqual(pilha.topo(), modelo[-1])


class ContratoFila:
    """Cenários de uma Fila de caracteres. Subclasses definem cria(n_max)."""

    def cria(self, n_max):
        raise NotImplementedError

    def test_satisfaz_fila_tad(self):
        self.assertIsInstance(self.cria(4), FilaTAD)

    def test_ordem_fifo(self):
        fila = self.cria(5)
        enfileira_tudo(fila, 'abcde')
        self.assertEqual([fila.desenfileira() for _ in range(5)], list('abcde'))

    def test_um_elemento(self):
        fila = self.cria(1)
        fila.enfileira('x')
        self.assertEqual(fila.frente(), 'x')
        self.assertEqual(fila.desenfileira(), 'x')

    def test_frente_nao_remove(self):
        fila = self.cria(3)
        enfileira_tudo(fila, 'ab')
        self.assertEqual(fila.frente(), 'a')
        self.assertEqual(fila.frente(), 'a')
        self.assertEqual(fila.desenfileira(), 'a')
        self.assertEqual(fila.frente(), 'b')
        self.assertEqual(fila.desenfileira(), 'b')

    def test_frente_nao_muda_ao_enfileirar(self):
        fila = self.cria(4)
        for letra in 'wxyz':
            fila.enfileira(letra)
            self.assertEqual(fila.frente(), 'w')

    def test_operacoes_intercaladas(self):
        fila = self.cria(4)
        enfileira_tudo(fila, 'ab')
        self.assertEqual(fila.desenfileira(), 'a')
        enfileira_tudo(fila, 'cd')
        self.assertEqual(fila.desenfileira(), 'b')
        self.assertEqual(fila.desenfileira(), 'c')
        fila.enfileira('e')
        self.assertEqual(fila.desenfileira(), 'd')
        self.assertEqual(fila.desenfileira(), 'e')

    def test_elementos_repetidos(self):
        fila = self.cria(6)
        enfileira_tudo(fila, 'aabbab')
        self.assertEqual([fila.desenfileira() for _ in range(6)], list('aabbab'))

    def test_reuso_apos_encher_e_esvaziar(self):
        fila = self.cria(3)
        for rodada in ('abc', 'xyz', 'mno'):
            enfileira_tudo(fila, rodada)
            self.assertEqual([fila.desenfileira() for _ in range(3)], list(rodada))

    def test_libera_executa(self):
        fila = self.cria(3)
        enfileira_tudo(fila, 'ab')
        fila.libera()

    def test_aleatorio_contra_modelo(self):
        rng = random.Random(2025)
        capacidade = 6
        fila = self.cria(capacidade)
        modelo = []

        for _ in range(400):
            if rng.random() < 0.55 and len(modelo) < capacidade:
                letra = rng.choice(LETRAS)
                fila.enfileira(letra)
                modelo.append(letra)
            elif modelo:
                self.assertEqual(fila.desenfileira(), modelo.pop(0))

            if modelo:
                self.assertEqual(fila.frente(), modelo[0])


# ============================================================
# Estruturas base (pilha.py e fila.py)
# ============================================================

class TestePilhaStr(ContratoPilha, CasoDeTeste):

    def cria(self, n_max):
        return PilhaStr(n_max)


class TesteFilaStr(ContratoFila, CasoDeTeste):

    def cria(self, n_max):
        return FilaStr(n_max)


class TestePilhaInt(CasoDeTeste):

    def test_ordem_lifo(self):
        pilha = PilhaInt(4)
        for valor in (1, 2, 3, 4):
            pilha.empilha(valor)
        self.assertEqual([pilha.desempilha() for _ in range(4)], [4, 3, 2, 1])

    def test_topo_nao_remove(self):
        pilha = PilhaInt(2)
        pilha.empilha(7)
        self.assertEqual(pilha.topo(), 7)
        self.assertEqual(pilha.topo(), 7)
        self.assertEqual(pilha.desempilha(), 7)

    def test_aceita_negativos(self):
        pilha = PilhaInt(2)
        pilha.empilha(-5)
        self.assertEqual(pilha.topo(), -5)
        self.assertEqual(pilha.desempilha(), -5)

    def test_aceita_valores_maiores_que_um_byte(self):
        pilha = PilhaInt(2)
        pilha.empilha(100_000)
        self.assertEqual(pilha.desempilha(), 100_000)


# ============================================================
# Questão 1: Deque (1.a), PilhaDeque (1.b) e FilaDeque (1.c)
# ============================================================

class TesteDeque(CasoDeTeste):

    def test_satisfaz_deque_tad(self):
        for metodo in ('inicio', 'fim', 'insere_inicio', 'insere_fim',
                       'remove_inicio', 'remove_fim'):
            self.assertTrue(callable(getattr(Deque, metodo, None)), metodo)

    def test_insere_fim_remove_fim_funciona_como_pilha(self):
        deque = Deque(4)
        for letra in 'abcd':
            deque.insere_fim(letra)
        self.assertEqual([deque.remove_fim() for _ in range(4)], list('dcba'))

    def test_insere_fim_remove_inicio_funciona_como_fila(self):
        deque = Deque(4)
        for letra in 'abcd':
            deque.insere_fim(letra)
        self.assertEqual([deque.remove_inicio() for _ in range(4)], list('abcd'))

    def test_insere_inicio_remove_inicio_funciona_como_pilha(self):
        deque = Deque(4)
        for letra in 'abcd':
            deque.insere_inicio(letra)
        self.assertEqual([deque.remove_inicio() for _ in range(4)], list('dcba'))

    def test_insere_inicio_remove_fim_funciona_como_fila(self):
        deque = Deque(4)
        for letra in 'abcd':
            deque.insere_inicio(letra)
        self.assertEqual([deque.remove_fim() for _ in range(4)], list('abcd'))

    def test_insere_inicio_preserva_elementos_existentes(self):
        deque = Deque(5)
        for letra in 'bcd':
            deque.insere_fim(letra)
        deque.insere_inicio('a')
        self.assertEqual([deque.remove_inicio() for _ in range(4)], list('abcd'))

    def test_inicio_e_fim_consultam_sem_remover(self):
        deque = Deque(3)
        for letra in 'abc':
            deque.insere_fim(letra)
        self.assertEqual(deque.inicio(), 'a')
        self.assertEqual(deque.fim(), 'c')
        self.assertEqual(deque.inicio(), 'a')
        self.assertEqual(deque.fim(), 'c')
        self.assertEqual(deque.remove_inicio(), 'a')
        self.assertEqual(deque.remove_fim(), 'c')
        self.assertEqual(deque.inicio(), 'b')
        self.assertEqual(deque.fim(), 'b')

    def test_um_elemento_e_inicio_e_fim_ao_mesmo_tempo(self):
        for insere in ('insere_inicio', 'insere_fim'):
            deque = Deque(1)
            getattr(deque, insere)('x')
            self.assertEqual(deque.inicio(), 'x')
            self.assertEqual(deque.fim(), 'x')

    def test_insercoes_nos_dois_extremos(self):
        deque = Deque(5)
        deque.insere_fim('c')
        deque.insere_inicio('b')
        deque.insere_fim('d')
        deque.insere_inicio('a')
        deque.insere_fim('e')
        self.assertEqual(deque.inicio(), 'a')
        self.assertEqual(deque.fim(), 'e')
        self.assertEqual([deque.remove_inicio() for _ in range(5)], list('abcde'))

    def test_remocoes_alternadas_nos_dois_extremos(self):
        deque = Deque(5)
        for letra in 'abcde':
            deque.insere_fim(letra)
        self.assertEqual(deque.remove_inicio(), 'a')
        self.assertEqual(deque.remove_fim(), 'e')
        self.assertEqual(deque.remove_inicio(), 'b')
        self.assertEqual(deque.remove_fim(), 'd')
        self.assertEqual(deque.remove_inicio(), 'c')

    def test_capacidades_diversas(self):
        for capacidade in (1, 2, 3, 5, 10, 16):
            deque = Deque(capacidade)
            letras = LETRAS[:capacidade]
            for letra in letras:
                deque.insere_fim(letra)
            self.assertEqual(
                [deque.remove_inicio() for _ in range(capacidade)], list(letras),
                f'capacidade {capacidade}',
            )

    def test_reuso_apos_encher_e_esvaziar(self):
        deque = Deque(3)
        for rodada in ('abc', 'xyz'):
            for letra in rodada:
                deque.insere_inicio(letra)
            self.assertEqual([deque.remove_fim() for _ in range(3)], list(rodada))

    def test_aleatorio_contra_modelo(self):
        rng = random.Random(1)
        capacidade = 7
        deque = Deque(capacidade)
        modelo = collections.deque()

        for _ in range(600):
            operacao = rng.choice(
                ('insere_inicio', 'insere_fim', 'remove_inicio', 'remove_fim')
            )

            if operacao.startswith('insere'):
                if len(modelo) == capacidade:
                    continue
                letra = rng.choice(LETRAS)
                if operacao == 'insere_inicio':
                    deque.insere_inicio(letra)
                    modelo.appendleft(letra)
                else:
                    deque.insere_fim(letra)
                    modelo.append(letra)
            elif not modelo:
                continue
            elif operacao == 'remove_inicio':
                self.assertEqual(deque.remove_inicio(), modelo.popleft())
            else:
                self.assertEqual(deque.remove_fim(), modelo.pop())

            if modelo:
                self.assertEqual(deque.inicio(), modelo[0])
                self.assertEqual(deque.fim(), modelo[-1])


class TestePilhaDeque(ContratoPilha, CasoDeTeste):

    def cria(self, n_max):
        return PilhaDeque(n_max)

    def test_armazena_somente_em_um_deque(self):
        self.assertIsInstance(self.cria(3).dados, Deque)


class TesteFilaDeque(ContratoFila, CasoDeTeste):

    def cria(self, n_max):
        return FilaDeque(n_max)

    def test_armazena_somente_em_um_deque(self):
        self.assertIsInstance(self.cria(3).dados, Deque)


# ============================================================
# Questão 2: Pilha2F, pilha implementada com duas filas
# ============================================================

class TestePilha2F(ContratoPilha, CasoDeTeste):

    def cria(self, n_max):
        return Pilha2F(n_max)

    def test_armazena_somente_em_duas_filas(self):
        pilha = self.cria(3)
        self.assertIsInstance(pilha.fila1, FilaStr)
        self.assertIsInstance(pilha.fila2, FilaStr)

    def test_filas_guardam_exatamente_os_elementos_empilhados(self):
        pilha = self.cria(5)
        empilha_tudo(pilha, 'abcd')
        pilha.topo()
        pilha.desempilha()
        self.assertEqual(pilha.fila1.tam + pilha.fila2.tam, 3)

    def test_topo_repetido_muitas_vezes_nao_perde_elementos(self):
        pilha = self.cria(4)
        empilha_tudo(pilha, 'abcd')
        for _ in range(10):
            self.assertEqual(pilha.topo(), 'd')
        self.assertEqual([pilha.desempilha() for _ in range(4)], list('dcba'))


# ============================================================
# Questão 3: Fila2P, fila implementada com duas pilhas
# ============================================================

class TesteFila2P(ContratoFila, CasoDeTeste):

    def cria(self, n_max):
        return Fila2P(n_max)

    def test_armazena_somente_em_duas_pilhas(self):
        fila = self.cria(3)
        self.assertIsInstance(fila.pilha1, PilhaStr)
        self.assertIsInstance(fila.pilha2, PilhaStr)

    def test_pilhas_guardam_exatamente_os_elementos_enfileirados(self):
        fila = self.cria(5)
        enfileira_tudo(fila, 'abcd')
        fila.frente()
        fila.desenfileira()
        self.assertEqual(fila.pilha1.tam + fila.pilha2.tam, 3)

    def test_frente_repetida_muitas_vezes_nao_perde_elementos(self):
        fila = self.cria(4)
        enfileira_tudo(fila, 'abcd')
        for _ in range(10):
            self.assertEqual(fila.frente(), 'a')
        self.assertEqual([fila.desenfileira() for _ in range(4)], list('abcd'))


# ============================================================
# Questão 4: inversão de pilha com (a) uma fila, (b) duas pilhas, (c) uma pilha
# ============================================================

class ContratoInvertePilha:
    """Subclasses definem `inverte`. O texto é empilhado da esquerda para a
    direita, então depois de inverter o topo deve ser o primeiro caractere."""

    inverte = None

    def _inverte(self, texto, n_max=None):
        pilha = PilhaStr(len(texto) if n_max is None else n_max)
        empilha_tudo(pilha, texto)
        retorno = type(self).inverte(pilha)
        return pilha, (pilha if retorno is None else retorno)

    def _verifica(self, texto, n_max=None):
        _, resultado = self._inverte(texto, n_max)
        self.assertEqual(esvazia_pilha(resultado), list(texto))

    def test_pilha_vazia(self):
        self._verifica('')

    def test_um_elemento(self):
        self._verifica('a')

    def test_dois_elementos(self):
        self._verifica('ab')

    def test_varios_elementos(self):
        self._verifica('abcdefg')

    def test_elementos_repetidos(self):
        self._verifica('aabbbca')

    def test_palindromo(self):
        self._verifica('arara')

    def test_pilha_com_capacidade_maior_que_a_quantidade(self):
        self._verifica('abc', n_max=10)

    def test_pilha_grande(self):
        self._verifica('abcdefghij' * 20)

    def test_inverte_a_propria_pilha_recebida(self):
        # O enunciado pede `void inverte(std::stack<char>* p)`: o conteúdo
        # de P deve ser invertido, e não devolvido em outra pilha.
        pilha, _ = self._inverte('abcd')
        self.assertEqual(esvazia_pilha(pilha), list('abcd'))

    def test_inverter_duas_vezes_restaura_a_ordem_original(self):
        _, resultado = self._inverte('abcde')
        retorno = type(self).inverte(resultado)
        resultado = resultado if retorno is None else retorno
        self.assertEqual(esvazia_pilha(resultado), list('edcba'))

    def test_pilha_continua_utilizavel_depois_de_inverter(self):
        _, resultado = self._inverte('abc', n_max=5)
        resultado.empilha('z')
        self.assertEqual(resultado.topo(), 'z')
        self.assertEqual(esvazia_pilha(resultado), list('zabc'))


class TesteInvertePilhaComFila(ContratoInvertePilha, CasoDeTeste):
    inverte = inverte_pilha_com_fila


class TesteInvertePilhaComDuasPilhas(ContratoInvertePilha, CasoDeTeste):
    inverte = inverte_pilha_com_duas_pilhas


class TesteInvertePilhaComUmaPilha(ContratoInvertePilha, CasoDeTeste):
    inverte = inverte_pilha_com_pilha


# ============================================================
# Questão 5: inversão de fila com (a) uma pilha, (b) duas filas
# ============================================================

class ContratoInverteFila:
    """Subclasses definem `inverte`. O texto é enfileirado da esquerda para a
    direita, então depois de inverter a frente deve ser o último caractere."""

    inverte = None

    def _inverte(self, texto, n_max=None):
        fila = FilaStr(len(texto) if n_max is None else n_max)
        enfileira_tudo(fila, texto)
        retorno = type(self).inverte(fila)
        return fila, (fila if retorno is None else retorno)

    def _verifica(self, texto, n_max=None):
        _, resultado = self._inverte(texto, n_max)
        self.assertEqual(esvazia_fila(resultado), list(reversed(texto)))

    def test_fila_vazia(self):
        self._verifica('')

    def test_um_elemento(self):
        self._verifica('a')

    def test_dois_elementos(self):
        self._verifica('ab')

    def test_varios_elementos(self):
        self._verifica('abcdefg')

    def test_elementos_repetidos(self):
        self._verifica('aabbbca')

    def test_palindromo(self):
        self._verifica('arara')

    def test_fila_com_capacidade_maior_que_a_quantidade(self):
        self._verifica('abc', n_max=10)

    def test_fila_grande(self):
        self._verifica('abcdefghij' * 10)

    def test_inverte_a_propria_fila_recebida(self):
        # O enunciado pede `void inverte(std::queue<char>* f)`: o conteúdo
        # de F deve ser invertido, e não devolvido em outra fila.
        fila, _ = self._inverte('abcd')
        self.assertEqual(esvazia_fila(fila), list('dcba'))

    def test_inverter_duas_vezes_restaura_a_ordem_original(self):
        _, resultado = self._inverte('abcde')
        retorno = type(self).inverte(resultado)
        resultado = resultado if retorno is None else retorno
        self.assertEqual(esvazia_fila(resultado), list('abcde'))

    def test_fila_continua_utilizavel_depois_de_inverter(self):
        _, resultado = self._inverte('abc', n_max=5)
        resultado.enfileira('z')
        self.assertEqual(resultado.frente(), 'c')
        self.assertEqual(esvazia_fila(resultado), list('cbaz'))


class TesteInverteFilaComPilha(ContratoInverteFila, CasoDeTeste):
    inverte = inverte_fila_com_pilha


class TesteInverteFilaComDuasFilas(ContratoInverteFila, CasoDeTeste):
    inverte = inverte_fila_com_duas_filas


# ============================================================
# Questão 6: PilhaMin, pilha com obter_minimo() em tempo constante
# ============================================================

class TestePilhaMin(CasoDeTeste):

    def _cria(self, valores, n_max=None):
        pilha = PilhaMin(len(valores) if n_max is None else n_max)
        for valor in valores:
            pilha.empilha(valor)
        return pilha

    def _verifica_minimo_a_cada_passo(self, valores):
        """Empilha e depois desempilha tudo, conferindo topo e mínimo sempre."""
        pilha = PilhaMin(len(valores))
        modelo = []

        for valor in valores:
            pilha.empilha(valor)
            modelo.append(valor)
            self.assertEqual(pilha.topo(), valor)
            self.assertEqual(pilha.obter_minimo(), min(modelo))

        while modelo:
            self.assertEqual(pilha.obter_minimo(), min(modelo))
            self.assertEqual(pilha.desempilha(), modelo.pop())

    def test_satisfaz_pilha_tad(self):
        self.assertIsInstance(PilhaMin(3), PilhaTAD)
        self.assertTrue(callable(getattr(PilhaMin, 'obter_minimo', None)))

    def test_ordem_lifo(self):
        pilha = self._cria([5, 1, 4, 2])
        self.assertEqual([pilha.desempilha() for _ in range(4)], [2, 4, 1, 5])

    def test_topo_nao_remove(self):
        pilha = self._cria([3, 8])
        self.assertEqual(pilha.topo(), 8)
        self.assertEqual(pilha.topo(), 8)
        self.assertEqual(pilha.desempilha(), 8)
        self.assertEqual(pilha.topo(), 3)

    def test_minimo_com_um_elemento(self):
        self.assertEqual(self._cria([42]).obter_minimo(), 42)

    def test_obter_minimo_nao_altera_a_pilha(self):
        pilha = self._cria([4, 2, 9])
        self.assertEqual(pilha.obter_minimo(), 2)
        self.assertEqual(pilha.obter_minimo(), 2)
        self.assertEqual([pilha.desempilha() for _ in range(3)], [9, 2, 4])

    def test_sequencia_crescente(self):
        self._verifica_minimo_a_cada_passo([1, 2, 3, 4, 5])

    def test_sequencia_decrescente(self):
        self._verifica_minimo_a_cada_passo([5, 4, 3, 2, 1])

    def test_sequencia_embaralhada(self):
        self._verifica_minimo_a_cada_passo([5, 3, 7, 3, 8, 1, 9, 2])

    def test_minimo_no_meio_da_pilha(self):
        pilha = self._cria([7, 1, 9, 8])
        self.assertEqual(pilha.obter_minimo(), 1)
        pilha.desempilha()
        pilha.desempilha()
        self.assertEqual(pilha.obter_minimo(), 1)
        pilha.desempilha()
        self.assertEqual(pilha.obter_minimo(), 7)

    def test_minimo_repetido(self):
        pilha = self._cria([2, 1, 1, 3])
        self.assertEqual(pilha.desempilha(), 3)
        self.assertEqual(pilha.obter_minimo(), 1)
        self.assertEqual(pilha.desempilha(), 1)
        self.assertEqual(pilha.obter_minimo(), 1)
        self.assertEqual(pilha.desempilha(), 1)
        self.assertEqual(pilha.obter_minimo(), 2)

    def test_todos_iguais(self):
        self._verifica_minimo_a_cada_passo([4, 4, 4, 4])

    def test_valores_negativos(self):
        self._verifica_minimo_a_cada_passo([3, -2, 5, -7, 0, -7])

    def test_zero(self):
        self._verifica_minimo_a_cada_passo([0, 5, 0, 1])

    def test_valores_maiores_que_um_byte(self):
        self._verifica_minimo_a_cada_passo([1000, 70_000, 256, 1_000_000])

    def test_minimo_apos_empilhar_de_novo(self):
        pilha = self._cria([5, 2], n_max=4)
        pilha.desempilha()
        self.assertEqual(pilha.obter_minimo(), 5)
        pilha.empilha(3)
        self.assertEqual(pilha.obter_minimo(), 3)
        pilha.empilha(6)
        self.assertEqual(pilha.obter_minimo(), 3)

    def test_aleatorio_contra_modelo(self):
        rng = random.Random(6)
        capacidade = 12
        pilha = PilhaMin(capacidade)
        modelo = []

        for _ in range(600):
            if rng.random() < 0.55 and len(modelo) < capacidade:
                valor = rng.randint(-50, 50)
                pilha.empilha(valor)
                modelo.append(valor)
            elif modelo:
                self.assertEqual(pilha.desempilha(), modelo.pop())

            if modelo:
                self.assertEqual(pilha.topo(), modelo[-1])
                self.assertEqual(pilha.obter_minimo(), min(modelo))


# ============================================================
# Questão 7: avaliação (7.a) e conversão (7.b) em notação polonesa reversa
# ============================================================

def valores(*numeros):
    """Usa bytes (tipo declarado na função) sempre que os valores couberem."""
    if all(0 <= numero <= 255 for numero in numeros):
        return bytes(numeros)
    return list(numeros)


def computa(expressao, *numeros):
    return computa_polonesa_reversa(len(numeros), valores(*numeros), expressao)


def converte(expressao):
    n_var = sum(1 for c in expressao if c.isalpha())
    resultado = converte_parentizada_para_polonesa_reversa(n_var, expressao)
    return resultado if isinstance(resultado, str) else ''.join(resultado)


class TesteComputaPolonesaReversa(CasoDeTeste):

    def test_uma_variavel(self):
        self.assertEqual(computa('A', 9), 9)

    def test_soma(self):
        self.assertEqual(computa('AB+', 2, 3), 5)

    def test_multiplicacao(self):
        self.assertEqual(computa('AB*', 4, 6), 24)

    def test_subtracao_respeita_ordem_dos_operandos(self):
        self.assertEqual(computa('AB-', 9, 4), 5)

    def test_subtracao_com_resultado_negativo(self):
        self.assertEqual(computa('AB-', 2, 5), -3)

    def test_divisao_respeita_ordem_dos_operandos(self):
        self.assertEqual(computa('AB/', 8, 2), 4)

    def test_divisao_inteira(self):
        self.assertEqual(computa('AB/', 7, 2), 3)

    def test_divisao_inteira_com_dividendo_negativo(self):
        # Usa o `//` do Python, que arredonda para baixo: -7 // 2 == -4
        self.assertEqual(computa('AB/', -7, 2), -4)

    def test_exemplo_do_enunciado(self):
        # O enunciado informa saída -4, mas a própria explicação ("2-6=-4")
        # ignora o resultado de 1/1 e a multiplicação final. A avaliação
        # padrão de "33+211/-*" é (3+3) * (2 - (1/1)) = 6.
        self.assertEqual(computa('AB+CED/-*', 3, 3, 2, 1, 1), 6)

    def test_resultado_intermediario_negativo(self):
        self.assertEqual(computa('AB-C*', 1, 5, 3), -12)

    def test_valores_de_entrada_negativos(self):
        self.assertEqual(computa('AB+', -3, 4), 1)

    def test_resultado_maior_que_um_byte(self):
        self.assertEqual(computa('AB*', 200, 200), 40_000)

    def test_variavel_repetida(self):
        self.assertEqual(computa('AA*', 4), 16)

    def test_variaveis_fora_de_ordem(self):
        self.assertEqual(computa('CA-B/', 2, 3, 20), 6)

    def test_sete_variaveis_encadeadas(self):
        self.assertEqual(computa('AB+C+D+E+F+G+', 1, 2, 3, 4, 5, 6, 7), 28)

    def test_sete_operandos_empilhados_antes_de_operar(self):
        self.assertEqual(computa('ABCDEFG++++++', 1, 2, 3, 4, 5, 6, 7), 28)

    def test_quatro_operacoes_juntas(self):
        # ((A + B) * C - D) / E = ((2 + 3) * 4 - 6) / 7 = 2
        self.assertEqual(computa('AB+C*D-E/', 2, 3, 4, 6, 7), 2)

    def test_zero_como_operando(self):
        self.assertEqual(computa('AB*C+', 0, 9, 5), 5)


class TesteConverteParaPolonesaReversa(CasoDeTeste):

    def test_exemplo_do_enunciado(self):
        self.assertEqual(converte('((A+B)*(C-(F/D)))'), 'AB+CFD/-*')

    def test_cada_operacao_isolada(self):
        for operador in '+-*/':
            self.assertEqual(converte(f'(A{operador}B)'), f'AB{operador}', operador)

    def test_uma_variavel(self):
        self.assertEqual(converte('A'), 'A')

    def test_aninhamento_a_esquerda(self):
        self.assertEqual(converte('((A+B)+C)'), 'AB+C+')

    def test_aninhamento_a_direita(self):
        self.assertEqual(converte('(A+(B*C))'), 'ABC*+')

    def test_aninhamento_dos_dois_lados(self):
        self.assertEqual(converte('((A+B)*(C-D))'), 'AB+CD-*')

    def test_aninhamento_profundo_a_direita(self):
        self.assertEqual(converte('(A-(B-(C-D)))'), 'ABCD---')

    def test_aninhamento_profundo_a_esquerda(self):
        self.assertEqual(converte('(((A-B)-C)-D)'), 'AB-C-D-')

    def test_operadores_diferentes_em_cada_nivel(self):
        self.assertEqual(converte('((A/B)-(C*D))'), 'AB/CD*-')

    def test_sete_variaveis(self):
        self.assertEqual(converte('(((A+B)*(C-D))/((E+F)-G))'), 'AB+CD-*EF+G-/')

    def test_variavel_repetida(self):
        self.assertEqual(converte('((A*A)+A)'), 'AA*A+')

    def test_mantem_a_ordem_dos_operandos(self):
        self.assertEqual(converte('((G-A)/(C-B))'), 'GA-CB-/')

    def test_saida_tem_um_caractere_por_operando_e_operador(self):
        saida = converte('((A+B)*(C-(F/D)))')
        self.assertEqual(len(saida), 9)
        self.assertNotIn('(', saida)
        self.assertNotIn(')', saida)

    def test_conversao_seguida_de_avaliacao(self):
        # ((A+B)*(C-(E/D))) com A=3 B=3 C=2 D=1 E=1  ->  (3+3) * (2 - 1/1) = 6
        polonesa = converte('((A+B)*(C-(E/D)))')
        self.assertEqual(computa(polonesa, 3, 3, 2, 1, 1), 6)


# ============================================================
# Questão 8: estratégias do TAD PegaEntreMaiores e o quick_sort
# ============================================================

class ContratoPegaEntreMaiores:
    """Subclasses definem `classe`. O k de k_maior começa em 1 (k=1 é o maior)
    e elementos repetidos contam como posições diferentes."""

    classe = None

    def _cria(self, texto, n_max=None):
        tad = self.classe(len(texto) + 3 if n_max is None else n_max)
        for letra in texto:
            tad.insere(letra)
        return tad

    def _verifica_todos_os_k(self, texto, n_max=None):
        tad = self._cria(texto, n_max)
        esperado = sorted(texto, reverse=True)
        obtido = [tad.k_maior(k) for k in range(1, len(texto) + 1)]
        self.assertEqual(obtido, esperado)

    def test_satisfaz_tad(self):
        self.assertIsInstance(self._cria(''), PegaEntreMaiores)

    def test_tamanho_vazio(self):
        self.assertEqual(self._cria('').tamanho(), 0)

    def test_tamanho_conta_elementos_inseridos_e_nao_a_capacidade(self):
        tad = self.classe(10)
        for quantidade, letra in enumerate('abcd', start=1):
            tad.insere(letra)
            self.assertEqual(tad.tamanho(), quantidade)

    def test_um_elemento(self):
        tad = self._cria('m')
        self.assertEqual(tad.maior(), 'm')
        self.assertEqual(tad.k_maior(1), 'm')

    def test_dois_elementos_em_ordem_crescente(self):
        tad = self._cria('ab')
        self.assertEqual(tad.maior(), 'b')
        self.assertEqual(tad.segundo_maior(), 'a')

    def test_dois_elementos_em_ordem_decrescente(self):
        tad = self._cria('ba')
        self.assertEqual(tad.maior(), 'b')
        self.assertEqual(tad.segundo_maior(), 'a')

    def test_maior_e_segundo_maior_com_insercao_embaralhada(self):
        tad = self._cria('dbfaec')
        self.assertEqual(tad.maior(), 'f')
        self.assertEqual(tad.segundo_maior(), 'e')

    def test_maior_inserido_por_ultimo(self):
        tad = self._cria('abcz')
        self.assertEqual(tad.maior(), 'z')
        self.assertEqual(tad.segundo_maior(), 'c')

    def test_maior_inserido_primeiro(self):
        tad = self._cria('zabc')
        self.assertEqual(tad.maior(), 'z')
        self.assertEqual(tad.segundo_maior(), 'c')

    def test_k_maior_coincide_com_maior_e_segundo_maior(self):
        tad = self._cria('qwerty')
        self.assertEqual(tad.k_maior(1), tad.maior())
        self.assertEqual(tad.k_maior(2), tad.segundo_maior())

    def test_todos_os_k_insercao_crescente(self):
        self._verifica_todos_os_k('abcdefgh')

    def test_todos_os_k_insercao_decrescente(self):
        self._verifica_todos_os_k('hgfedcba')

    def test_todos_os_k_insercao_embaralhada(self):
        self._verifica_todos_os_k('dbfahceg')

    def test_todos_os_k_com_repetidos(self):
        self._verifica_todos_os_k('banana')

    def test_todos_os_k_com_todos_iguais(self):
        self._verifica_todos_os_k('zzzzz')

    def test_todos_os_k_com_maiusculas_minusculas_e_digitos(self):
        self._verifica_todos_os_k('aZ3bY1c')

    def test_todos_os_k_com_tad_cheio(self):
        self._verifica_todos_os_k('dbfahceg', n_max=8)

    def test_maior_repetido(self):
        tad = self._cria('azbz')
        self.assertEqual(tad.maior(), 'z')
        self.assertEqual(tad.segundo_maior(), 'z')
        self.assertEqual(tad.k_maior(3), 'b')

    def test_menor_elemento_e_o_ultimo_k(self):
        tad = self._cria('dbfaec')
        self.assertEqual(tad.k_maior(6), 'a')

    def test_respostas_acompanham_novas_insercoes(self):
        tad = self.classe(6)
        tad.insere('c')
        self.assertEqual(tad.maior(), 'c')
        tad.insere('a')
        self.assertEqual(tad.maior(), 'c')
        self.assertEqual(tad.segundo_maior(), 'a')
        tad.insere('x')
        self.assertEqual(tad.maior(), 'x')
        self.assertEqual(tad.segundo_maior(), 'c')
        tad.insere('m')
        self.assertEqual(tad.segundo_maior(), 'm')
        self.assertEqual(tad.k_maior(4), 'a')

    def test_consultas_repetidas_nao_alteram_o_resultado(self):
        texto = 'dbfahceg'
        tad = self._cria(texto)
        esperado = sorted(texto, reverse=True)

        for k in (5, 1, 8, 3, 3, 2, 7, 4, 6, 1):
            self.assertEqual(tad.k_maior(k), esperado[k - 1], f'k={k}')

        self.assertEqual(tad.maior(), 'h')
        self.assertEqual(tad.segundo_maior(), 'g')
        self.assertEqual(tad.tamanho(), 8)

    def test_aleatorio_todos_os_k(self):
        rng = random.Random(8)
        for tamanho in (3, 10, 40):
            texto = ''.join(rng.choice(LETRAS) for _ in range(tamanho))
            self._verifica_todos_os_k(texto)

    def test_aleatorio_grande(self):
        rng = random.Random(88)
        texto = ''.join(rng.choice(LETRAS) for _ in range(150))
        tad = self._cria(texto)
        esperado = sorted(texto, reverse=True)

        self.assertEqual(tad.tamanho(), 150)
        self.assertEqual(tad.maior(), esperado[0])
        self.assertEqual(tad.segundo_maior(), esperado[1])
        for k in (1, 2, 10, 75, 149, 150):
            self.assertEqual(tad.k_maior(k), esperado[k - 1], f'k={k}')


class TesteNaoOrdenado(ContratoPegaEntreMaiores, CasoDeTeste):
    classe = PegaEntreMaioresNaoOrdenado


class TesteOrdenacaoIneficiente(ContratoPegaEntreMaiores, CasoDeTeste):
    classe = PegaEntreMaioresOrdInef


class TesteOrdenacaoEficiente(ContratoPegaEntreMaiores, CasoDeTeste):
    classe = PegaEntreMaioresOrdEfic


class TesteQuickSelect(ContratoPegaEntreMaiores, CasoDeTeste):
    classe = PegaEntreMaioresQuickSDelect


class TesteQuickSort(CasoDeTeste):
    """quick_sort(arr, ini, fim) ordena arr[ini..fim] em ordem decrescente
    (o TAD ordenado guarda o maior elemento na posição 0)."""

    def _verifica(self, texto):
        arr = array('w', texto)
        quick_sort(arr, 0, len(texto) - 1)
        self.assertEqual(list(arr), sorted(texto, reverse=True))

    def test_vazio(self):
        self._verifica('')

    def test_um_elemento(self):
        self._verifica('a')

    def test_dois_elementos(self):
        self._verifica('ab')
        self._verifica('ba')

    def test_ja_ordenado(self):
        self._verifica('hgfedcba')

    def test_ordem_inversa(self):
        self._verifica('abcdefgh')

    def test_embaralhado(self):
        self._verifica('dbfahceg')

    def test_repetidos(self):
        self._verifica('banana')
        self._verifica('zzzz')

    def test_aleatorio(self):
        rng = random.Random(80)
        for tamanho in (5, 30, 200):
            self._verifica(''.join(rng.choice(LETRAS) for _ in range(tamanho)))

    def test_ordena_somente_o_intervalo_pedido(self):
        arr = array('w', 'zzacbdaa')
        quick_sort(arr, 2, 5)
        self.assertEqual(''.join(arr), 'zzdcbaaa')


# ============================================================
# Questão 9: SacoVaiEVem, saco com iterador direto e reverso
# ============================================================

LIMITE_ITERACAO = 10_000


class TesteSacoVaiEVem(CasoDeTeste):

    def _cria(self, valores):
        saco = SacoVaiEVem()
        for valor in valores:
            saco.adiciona(valor)
        return saco

    def _lista(self, iterador):
        """Materializa um iterador, falhando se ele não terminar."""
        itens = list(itertools.islice(iterador, LIMITE_ITERACAO))
        self.assertLess(len(itens), LIMITE_ITERACAO, 'iterador não termina')
        return itens

    def _verifica_conteudo(self, saco, esperado):
        """Confere os elementos (sem exigir ordem) e a coerência ida/volta."""
        ida = self._lista(saco.itera())
        volta = self._lista(saco.iteravolta())
        self.assertEqual(Counter(ida), Counter(esperado))
        self.assertEqual(volta, list(reversed(ida)))

    def _encontrou(self, resultado):
        return resultado is not None and resultado is not False

    def test_saco_vazio_nao_itera_nada(self):
        saco = SacoVaiEVem()
        self.assertEqual(self._lista(saco.itera()), [])
        self.assertEqual(self._lista(saco.iteravolta()), [])

    def test_um_elemento(self):
        saco = self._cria(['a'])
        self.assertEqual(self._lista(saco.itera()), ['a'])
        self.assertEqual(self._lista(saco.iteravolta()), ['a'])

    def test_itera_percorre_todos_os_elementos(self):
        self._verifica_conteudo(self._cria('abcde'), 'abcde')

    def test_iteravolta_e_o_inverso_de_itera(self):
        saco = self._cria('abcde')
        ida = self._lista(saco.itera())
        self.assertEqual(self._lista(saco.iteravolta()), ida[::-1])
        self.assertEqual(len(ida), 5)

    def test_dois_elementos(self):
        self._verifica_conteudo(self._cria('ab'), 'ab')

    def test_elementos_repetidos_sao_mantidos(self):
        self._verifica_conteudo(self._cria('aabab'), 'aabab')

    def test_iterar_varias_vezes_da_o_mesmo_resultado(self):
        saco = self._cria('abc')
        primeira = self._lista(saco.itera())
        self._lista(saco.iteravolta())
        self.assertEqual(self._lista(saco.itera()), primeira)

    def test_iteradores_simultaneos_sao_independentes(self):
        saco = self._cria('abc')
        ida = self._lista(saco.itera())
        pares = list(zip(saco.itera(), saco.iteravolta()))
        self.assertEqual(pares, list(zip(ida, ida[::-1])))

    def test_aceita_inteiros_incluindo_zero(self):
        saco = self._cria([3, 0, -1, 0])
        self._verifica_conteudo(saco, [3, 0, -1, 0])
        self.assertTrue(self._encontrou(saco.busca(0)))
        self.assertTrue(self._encontrou(saco.busca(-1)))

    def test_busca_elemento_existente(self):
        saco = self._cria('abcde')
        for letra in 'abcde':
            self.assertTrue(self._encontrou(saco.busca(letra)), letra)

    def test_busca_elemento_inexistente(self):
        self.assertFalse(self._encontrou(self._cria('abc').busca('z')))

    def test_busca_em_saco_vazio(self):
        self.assertFalse(self._encontrou(SacoVaiEVem().busca('a')))

    def test_busca_nao_altera_o_saco(self):
        saco = self._cria('abc')
        saco.busca('b')
        saco.busca('z')
        self._verifica_conteudo(saco, 'abc')

    def test_remove_elemento_do_meio(self):
        saco = self._cria('abcde')
        saco.remove('c')
        self._verifica_conteudo(saco, 'abde')

    def test_remove_primeiro_elemento_adicionado(self):
        saco = self._cria('abcde')
        saco.remove('a')
        self._verifica_conteudo(saco, 'bcde')

    def test_remove_ultimo_elemento_adicionado(self):
        saco = self._cria('abcde')
        saco.remove('e')
        self._verifica_conteudo(saco, 'abcd')

    def test_remove_unico_elemento(self):
        saco = self._cria('a')
        saco.remove('a')
        self._verifica_conteudo(saco, '')

    def test_elemento_removido_nao_e_mais_encontrado(self):
        saco = self._cria('abc')
        saco.remove('b')
        self.assertFalse(self._encontrou(saco.busca('b')))
        self.assertTrue(self._encontrou(saco.busca('a')))
        self.assertTrue(self._encontrou(saco.busca('c')))

    def test_remove_somente_uma_ocorrencia_de_repetido(self):
        saco = self._cria('abab')
        saco.remove('a')
        self._verifica_conteudo(saco, 'abb')
        self.assertTrue(self._encontrou(saco.busca('a')))

    def test_remove_todos_os_elementos(self):
        saco = self._cria('abcd')
        for letra in 'cadb':
            saco.remove(letra)
        self._verifica_conteudo(saco, '')

    def test_adiciona_depois_de_esvaziar(self):
        saco = self._cria('ab')
        saco.remove('a')
        saco.remove('b')
        saco.adiciona('x')
        saco.adiciona('y')
        self._verifica_conteudo(saco, 'xy')

    def test_adiciona_depois_de_remover_extremos(self):
        saco = self._cria('abc')
        saco.remove('a')
        saco.remove('c')
        saco.adiciona('d')
        self._verifica_conteudo(saco, 'bd')

    def test_aleatorio_contra_modelo(self):
        rng = random.Random(9)
        saco = SacoVaiEVem()
        modelo = Counter()

        for _ in range(300):
            valor = rng.randint(0, 9)
            if rng.random() < 0.6:
                saco.adiciona(valor)
                modelo[valor] += 1
            elif modelo[valor] > 0:
                saco.remove(valor)
                modelo[valor] -= 1

            self.assertEqual(self._encontrou(saco.busca(valor)), modelo[valor] > 0)

        self._verifica_conteudo(saco, list(modelo.elements()))


# ============================================================
# Execução
# ============================================================

QUESTOES = {
    'base': (TestePilhaStr, TesteFilaStr, TestePilhaInt),
    '1': (TesteDeque, TestePilhaDeque, TesteFilaDeque),
    '2': (TestePilha2F,),
    '3': (TesteFila2P,),
    '4': (TesteInvertePilhaComFila, TesteInvertePilhaComDuasPilhas,
          TesteInvertePilhaComUmaPilha),
    '5': (TesteInverteFilaComPilha, TesteInverteFilaComDuasFilas),
    '6': (TestePilhaMin,),
    '7': (TesteComputaPolonesaReversa, TesteConverteParaPolonesaReversa),
    '8': (TesteNaoOrdenado, TesteOrdenacaoIneficiente, TesteOrdenacaoEficiente,
          TesteQuickSelect, TesteQuickSort),
    '9': (TesteSacoVaiEVem,),
}


def rotulo(chave):
    return 'Estruturas base' if chave == 'base' else f'Questão {chave}'


def executar(chaves, verbosidade=1, somente_resumo=False):
    carregador = unittest.defaultTestLoader
    suites = {
        chave: unittest.TestSuite(
            carregador.loadTestsFromTestCase(classe) for classe in QUESTOES[chave]
        )
        for chave in chaves
    }

    saida = io.StringIO() if somente_resumo else sys.stderr
    resultado = unittest.TextTestRunner(stream=saida, verbosity=verbosidade).run(
        unittest.TestSuite(suites.values())
    )

    falhas = {chave: set() for chave in chaves}
    erros = {chave: set() for chave in chaves}

    for registro, destino in ((resultado.failures, falhas), (resultado.errors, erros)):
        for teste, _ in registro:
            teste = getattr(teste, 'test_case', teste)
            for chave in chaves:
                if isinstance(teste, QUESTOES[chave]):
                    destino[chave].add(teste.id())

    print('\n' + '=' * 60)
    print('RESUMO DOS TESTES')
    print('=' * 60)
    print(f"{'':<18}{'Testes':>8}{'OK':>8}{'Falhas':>8}{'Erros':>8}")

    totais = [0, 0, 0, 0]
    for chave in chaves:
        total = suites[chave].countTestCases()
        n_falhas = len(falhas[chave] - erros[chave])
        n_erros = len(erros[chave])
        linha = (total, total - n_falhas - n_erros, n_falhas, n_erros)
        totais = [a + b for a, b in zip(totais, linha)]
        print(f'{rotulo(chave):<18}' + ''.join(f'{n:>8}' for n in linha))

    print('-' * 60)
    print(f"{'Total':<18}" + ''.join(f'{n:>8}' for n in totais))

    if resultado.wasSuccessful():
        print('\nResultado: TESTES CONCLUÍDOS SEM FALHAS.')
    else:
        print('\nResultado: EXISTEM TESTES COM FALHA OU ERRO.')

    return resultado


def principal(argumentos):
    verbosidade = 2 if '-v' in argumentos else 1
    somente_resumo = '--resumo' in argumentos
    pedidos = [a for a in argumentos if not a.startswith('-')]

    desconhecidos = [p for p in pedidos if p not in QUESTOES]
    if desconhecidos:
        print(f'Questão desconhecida: {", ".join(desconhecidos)}')
        print(f'Opções: {", ".join(QUESTOES)}')
        return 2

    chaves = [chave for chave in QUESTOES if chave in pedidos] or list(QUESTOES)
    resultado = executar(chaves, verbosidade, somente_resumo)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(principal(sys.argv[1:]))
