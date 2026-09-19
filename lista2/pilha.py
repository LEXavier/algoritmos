from typing import Protocol, TypeVar
from array import array

t = TypeVar("t")

class PilhaTAD[t](Protocol):
    
    def empilha(self, valor: t) -> None:
        ...
    
    def desempilha(self) -> t:
        ...
    
    def topo(self) -> t:
        ...
        
    def libera(self) -> None:
        ...

class PilhaStr:

    __slots__ = ('dados', 'tam', 'n_max')
    
    def __init__(self, n_max):
        
        self.n_max = n_max
        self.dados = array('w', ['\0'] * n_max)
        self.tam = 0

    def empilha(self, valor:str) -> None:
        
        if self.tam >= self.n_max:
            raise OverflowError('Pilha cheia')

        self.dados[self.tam] = valor
        self.tam += 1

    def desempilha(self):
        # O(1)
        if self.tam <= 0:
            raise IndexError('Pilha vazia')

        valor = self.dados[self.tam - 1]
        self.tam -= 1

        return valor

    def topo(self):
        return self.dados[self.tam - 1]