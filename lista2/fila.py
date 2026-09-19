from typing import Protocol, TypeVar 
from array import array

t = TypeVar("t")

class FilaTAD[t](Protocol):
    
    def enfileira(self, valor: t) -> None:
        ...
    
    def desenfileira(self) -> t:
        ...
    
    def frente(self) -> t:
        ...
    
    def libera(self) -> None:
        ...

class FilaStr:
    
    __slots__ = ('dados', 'tam', 'n_max')
    
    def __init__(self, n_max=1000):
        
        self.n_max = n_max
        self.dados = array('w', ['\0'] * n_max )
        self.tam = 0
        
    def enfileira(self, valor: str) -> None:
        
        if self.tam >= self.n_max:
            raise OverflowError('Fila cheia')
        
        self.dados[self.tam] = valor
        self.tam += 1
        
    def desenfileira(self) -> str:
        
        if self.tam == 0:
            raise IndexError('Fila vazia')
        
        valor = self.dados[0]
        
        for i in range(self.tam-1):
            self.dados[i] = self.dados[i+1]
        
        self.tam -= 1
        
        return valor
    
    def frente(self) -> str:
        return self.dados[0]
    
    def libera(self) -> None:
        self.dados = array('w')
        self.tam = 0