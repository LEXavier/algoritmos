import unittest

from estruturas import (
    Deque,
    PilhaDeque,
    FilaDeque,
    Fila,
    Pilha,
    PilhaDuplaFila,
    FilaDuplaPilha,
    PilhaMin
)

from operacoes import (
    inverte_pilha_com_fila,
    inverte_pilha_com_duas_pilhas,
    inverte_pilha_com_pilha,
    inverte_fila_com_pilha,
    inverte_fila_com_duas_filas,
    avalia_polonesa,
    polonesa,
)

from pega_entre_maiores import (
    PegaEntreMaioresNaoOrdenado,
    PegaEntreMaioresOrdenadoIneficiente,
    PegaEntreMaioresOrdenadoEficiente,
    PegaEntreMaioresQuickSelect,
)

from saco import SacoVaiEVem


# ============================================================
# DEQUE
# ============================================================

class TesteDeque(unittest.TestCase):

    def test_operacoes_nos_dois_extremos(self):
        deque = Deque(5)

        deque.insere_fim("B")
        deque.insere_inicio("A")
        deque.insere_fim("C")

        self.assertEqual(deque.inicio(), "A")
        self.assertEqual(deque.fim(), "C")

        self.assertEqual(deque.remove_inicio(), "A")
        self.assertEqual(deque.remove_fim(), "C")
        self.assertEqual(deque.remove_inicio(), "B")

    def test_deque_vazio(self):
        deque = Deque(3)

        with self.assertRaises(IndexError):
            deque.remove_inicio()

        with self.assertRaises(IndexError):
            deque.remove_fim()

    def test_deque_cheio(self):
        deque = Deque(2)

        deque.insere_fim("A")
        deque.insere_fim("B")

        with self.assertRaises(OverflowError):
            deque.insere_fim("C")


# ============================================================
# PILHA COM DEQUE
# ============================================================

class TestePilhaDeque(unittest.TestCase):

    def test_lifo(self):
        pilha = PilhaDeque(5)

        pilha.empilha("A")
        pilha.empilha("B")
        pilha.empilha("C")

        self.assertEqual(pilha.topo(), "C")
        self.assertEqual(pilha.desempilha(), "C")
        self.assertEqual(pilha.desempilha(), "B")
        self.assertEqual(pilha.desempilha(), "A")

    def test_pilha_vazia(self):
        pilha = PilhaDeque(3)

        with self.assertRaises(IndexError):
            pilha.desempilha()


# ============================================================
# FILA COM DEQUE
# ============================================================

class TesteFilaDeque(unittest.TestCase):

    def test_fifo(self):
        fila = FilaDeque(5)

        fila.enfileira("A")
        fila.enfileira("B")
        fila.enfileira("C")

        self.assertEqual(fila.frente(), "A")
        self.assertEqual(fila.desenfileira(), "A")
        self.assertEqual(fila.desenfileira(), "B")
        self.assertEqual(fila.desenfileira(), "C")

    def test_fila_vazia(self):
        fila = FilaDeque(3)

        with self.assertRaises(IndexError):
            fila.desenfileira()


# ============================================================
# FILA SEQUENCIAL
# ============================================================

class TesteFila(unittest.TestCase):

    def test_fifo(self):
        fila = Fila(5)

        fila.enfileira("A")
        fila.enfileira("B")
        fila.enfileira("C")

        self.assertEqual(fila.frente(), "A")
        self.assertEqual(fila.desenfileira(), "A")
        self.assertEqual(fila.desenfileira(), "B")
        self.assertEqual(fila.desenfileira(), "C")

    def test_capacidade(self):
        fila = Fila(2)

        fila.enfileira("A")
        fila.enfileira("B")

        with self.assertRaises(OverflowError):
            fila.enfileira("C")

    def test_fila_vazia(self):
        fila = Fila(3)

        with self.assertRaises(IndexError):
            fila.desenfileira()


# ============================================================
# PILHA SEQUENCIAL
# ============================================================

class TestePilha(unittest.TestCase):

    def test_lifo(self):
        pilha = Pilha(5)

        pilha.empilha("A")
        pilha.empilha("B")
        pilha.empilha("C")

        self.assertEqual(pilha.topo(), "C")
        self.assertEqual(pilha.desempilha(), "C")
        self.assertEqual(pilha.desempilha(), "B")
        self.assertEqual(pilha.desempilha(), "A")

    def test_capacidade(self):
        pilha = Pilha(2)

        pilha.empilha("A")
        pilha.empilha("B")

        with self.assertRaises(OverflowError):
            pilha.empilha("C")

    def test_pilha_vazia(self):
        pilha = Pilha(3)

        with self.assertRaises(IndexError):
            pilha.desempilha()


# ============================================================
# PILHA COM DUAS FILAS
# ============================================================

class TestePilhaDuasFilas(unittest.TestCase):

    def test_lifo(self):
        pilha = PilhaDuplaFila(5)

        pilha.empilha("A")
        pilha.empilha("B")
        pilha.empilha("C")

        self.assertEqual(pilha.topo(), "C")
        self.assertEqual(pilha.desempilha(), "C")
        self.assertEqual(pilha.desempilha(), "B")
        self.assertEqual(pilha.desempilha(), "A")


# ============================================================
# FILA COM DUAS PILHAS
# ============================================================

class TesteFilaDuplaPilha(unittest.TestCase):

    def test_fifo(self):
        fila = FilaDuplaPilha(5)

        fila.enfileira("A")
        fila.enfileira("B")
        fila.enfileira("C")

        self.assertEqual(fila.frente(), "A")
        self.assertEqual(fila.desenfileira(), "A")
        self.assertEqual(fila.desenfileira(), "B")
        self.assertEqual(fila.desenfileira(), "C")


# ============================================================
# INVERSÃO DE PILHA
# ============================================================

class TesteInversaoPilha(unittest.TestCase):

    def _testar_inversao(self, funcao):
        pilha = Pilha(10)

        for valor in ["A", "B", "C", "D"]:
            pilha.empilha(valor)

        resultado = funcao(pilha)

        if resultado is None:
            resultado = pilha

        valores = []

        for _ in range(4):
            valores.append(resultado.desempilha())

        self.assertEqual(
            valores,
            ["A", "B", "C", "D"]
        )

    def test_com_fila(self):
        self._testar_inversao(
            inverte_pilha_com_fila
        )

    def test_com_duas_pilhas(self):
        self._testar_inversao(
            inverte_pilha_com_duas_pilhas
        )

    def test_com_pilha(self):
        self._testar_inversao(
            inverte_pilha_com_pilha
        )


# ============================================================
# INVERSÃO DE FILA
# ============================================================

class TesteInversaoFila(unittest.TestCase):

    def _testar_inversao(self, funcao):
        fila = Fila(10)

        for valor in ["A", "B", "C", "D"]:
            fila.enfileira(valor)

        resultado = funcao(fila)

        if resultado is None:
            resultado = fila

        valores = []

        for _ in range(4):
            valores.append(resultado.desenfileira())

        self.assertEqual(
            valores,
            ["D", "C", "B", "A"]
        )

    def test_com_pilha(self):
        self._testar_inversao(
            inverte_fila_com_pilha
        )

    def test_com_duas_filas(self):
        self._testar_inversao(
            inverte_fila_com_duas_filas
        )


# ============================================================
# PILHA MÍNIMO
# ============================================================

class TestePilhaMin(unittest.TestCase):

    def test_minimo(self):
        pilha = PilhaMin(10)

        for valor in [5, 2, 8, 1, 3]:
            pilha.empilha(valor)

        self.assertEqual(pilha.obterMinimo(), 1)
        self.assertEqual(pilha.topo(), 3)

        self.assertEqual(pilha.desempilha(), 3)
        self.assertEqual(pilha.obterMinimo(), 1)

        self.assertEqual(pilha.desempilha(), 1)
        self.assertEqual(pilha.obterMinimo(), 2)

    def test_pilha_min_vazia(self):
        pilha = PilhaMin(5)

        with self.assertRaises(IndexError):
            pilha.obterMinimo()


# ============================================================
# NOTAÇÃO POLONESA
# ============================================================

class TestePolonesa(unittest.TestCase):

    def test_avaliacao(self):
        resultado = avalia_polonesa(
            "AB+",
            {"A": 3, "B": 4}
        )

        self.assertEqual(resultado, 7)

    def test_conversao(self):
        resultado = polonesa(
            "((A+B)*(C-(F/D)))"
        )

        self.assertIsNotNone(resultado)


# ============================================================
# PEGA ENTRE MAIORES
# ============================================================

class TestePegaEntreMaiores(unittest.TestCase):

    def _testar_implementacao(self, classe):
        estrutura = classe(10)

        valores = ["D", "B", "A", "C", "E"]

        for valor in valores:
            try:
                estrutura.insere(valor)
            except AttributeError:
                estrutura.insere_fim(valor)

        if hasattr(estrutura, "tamanho"):
            self.assertEqual(
                estrutura.tamanho(),
                5
            )

        if hasattr(estrutura, "pega"):
            self.assertEqual(
                estrutura.pega(1),
                "E"
            )

    def test_nao_ordenado(self):
        self._testar_implementacao(
            PegaEntreMaioresNaoOrdenado
        )

    def test_ordenado_ineficiente(self):
        self._testar_implementacao(
            PegaEntreMaioresOrdenadoIneficiente
        )

    def test_ordenado_eficiente(self):
        self._testar_implementacao(
            PegaEntreMaioresOrdenadoEficiente
        )

    def test_quickselect(self):
        self._testar_implementacao(
            PegaEntreMaioresQuickSelect
        )


# ============================================================
# SACO VAI E VEM
# ============================================================

class TesteSaco(unittest.TestCase):

    def test_existencia(self):
        saco = SacoVaiEVem(10)

        self.assertIsNotNone(saco)


# ============================================================
# EXECUÇÃO DOS TESTES
# ============================================================

def executar_testes():
    suite = unittest.defaultTestLoader.loadTestsFromModule(
        __import__(__name__)
    )

    resultado = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)

    total = resultado.testsRun
    falhas = len(resultado.failures)
    erros = len(resultado.errors)
    ignorados = len(resultado.skipped)

    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)

    print(f"Testes executados: {total}")
    print(f"Falhas:            {falhas}")
    print(f"Erros:             {erros}")
    print(f"Ignorados:         {ignorados}")

    if falhas == 0 and erros == 0:
        print("\nResultado: TESTES CONCLUÍDOS SEM FALHAS.")
    else:
        print("\nResultado: EXISTEM TESTES COM FALHA OU ERRO.")

    return resultado