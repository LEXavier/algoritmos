from fila import FilaTAD
from pilha import PilhaTAD
from questao_um import PilhaDeque, FilaDeque

## Questão 1.b

def testa_pilha_deque(pilha:PilhaTAD[str]):
    raise NotImplementedError

## Questão 1.c

def testa_fila_deque(fila:FilaTAD[str]):
    raise NotImplementedError

def executa_testes():
    
    pilha_deque = PilhaDeque(10)
    fila_deque = FilaDeque(10)
    
    testa_pilha_deque(pilha_deque)
    testa_fila_deque(fila_deque)
    