from typing import Protocol, TypeVar, runtime_checkable
from array import array

t = TypeVar("t")

@runtime_checkable
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
    
    def libera(self) -> None :
        self.dados = array('w')
        self.n_max = 0
        self.tam
    
    
class PilhaInt:
    
    __slots__ = ('dados', 'tam', 'n_max')
    
    def __init__(self, n_max=1000) -> None: # Complexidade O(1)
        self.n_max = n_max
        self.dados = array('B', bytes(n_max))
        self.tam = 0
    
    def empilha(self, valor: int) -> None: # Complexidade O(1)
        if self.tam >= self.n_max :
            raise OverflowError('Pilha cheia')
        
        self.dados[self.tam] = valor
        self.tam += 1
    
    def desempilha(self) -> int: # Complexidade O(1)
        if self.tam == 0 :
            raise IndexError('Pilha vazia')
        
        valor = self.dados[self.tam - 1]
        self.tam -= 1
        
        return valor
    
    def topo(self) -> int: # Complexidade O(1)
        if self.tam == 0 :
            raise IndexError('Pilha vazia')
        
        return self.dados[self.tam - 1]
        
    def libera(self) -> None: # Complexidade O(1)
        self.dados = array('B')
        self.tam = 0
        self.n_max = 0