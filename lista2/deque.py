from typing import Protocol, TypeVar
from array import array

t = TypeVar("t")

####### Questão 1.a

class DequeTAD(Protocol[t]):
    
    def inicio(self) -> object:
        ...
        
    def fim(self) -> object:
        ...
    
    def insere_inicio(self, valor: t) -> None:
        ...
    
    def insere_fim(self, valor: t) -> None:
        ...
    
    def remove_inicio(self) -> t:
        ...
    
    def remove_fim(self) -> t:
        ...

class Deque:
    
    __slots__ = ('dados', 'tam', 'n_max')
    
    def __init__(self, n_max=1000):
        self.n_max = n_max
        self.dados = array('w', bytes(n_max))
        self.tam = 0
        
    def inicio(self) -> str: # Complexidade O(1)
        
        if self.tam == 0:
            raise IndexError('Deque vazio')
        
        return self.dados[0]
    
    def fim(self) -> str: # Complexidade O(1)
        
        if self.tam == 0:
            raise IndexError('Deque vazio')
        
        return self.dados[self.tam - 1]
    
    def insere_inicio(self, valor:str) -> None: # Complexidade O(n)
        
        if self.tam >= self.n_max:
            raise OverflowError('Deque cheio')
        
        i = 0
        for i in range(self.tam) :
            self.dados[i+1] = self.dados[i]
        
        self.dados[0] = valor
        self.tam += 1
    
    def insere_fim(self, valor:str) -> None: # Complexidade O(1)
        
        if self.tam >= self.n_max:
            raise OverflowError('Deque cheio')
        
        self.dados[self.tam] = valor
        self.tam += 1
    
    def remove_inicio(self) -> str: # Complexidade O(n)
        
        if self.tam == 0:
            raise IndexError('Deque vazio')
        
        valor = self.dados[0]
        
        for i in range(self.tam-1):
            self.dados[i] = self.dados[i+1]
        
        self.tam -= 1
        
        return valor
    
    def remove_fim(self) -> str: # Complexidade O(1)
        
        if self.tam == 0:
            raise IndexError('Deque vazio')
        
        valor = self.dados[self.tam-1]
        self.tam -= 1
        
        return valor
    