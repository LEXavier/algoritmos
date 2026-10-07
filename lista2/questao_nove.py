from array import array 
from typing import Protocol, TypeVar

t = TypeVar('t')

class No[t]:
    def __init__(self, dado:t) -> None:
        self.dado = dado
        self.proximo = None
        self.anterior = None 
        
class SacoVaiEVem[t]:
    
    __slots__ = ('inicio', 'fim', 'tam',)
    
    def __init__(self) -> None:
        self.inicio = None
        self.fim = None
        self.tam = 0
    
    def adiciona(self, dado:t) -> None:
        
        no = No(dado)
        
        if self.inicio is None:
            self.inicio = no
            self.fim = no
        else:
            no.anterior = self.fim # type: ignore
            self.fim.proximo = no # type: ignore
            self.fim = no
        
        self.tam += 1

    def itera(self):
        atual = self.inicio
        
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
            
    def iteravolta(self):
        atual = self.fim
        
        while atual is not None:
            yield atual.dado
            atual = atual.anterior
            
    def busca(self, dado:t) -> t | None:
        
        atual = self.inicio
        
        while atual is not None:
            if atual.dado == dado:
                return atual.dado
            
            atual = atual.proximo
        
        return None
    
    def remove(self, dado:t) -> None:
        
        atual = self.inicio
        
        while atual is not None:
            
            if atual.dado == dado:
                
                if atual.anterior is not None:
                    atual.anterior.proximo = atual.proximo
                else:
                    self.inicio = atual.proximo
            
                if atual.proximo is not None:
                    atual.proximo.anterior = atual.anterior
                else:
                    self.fim = atual.anterior
                
                self.tam -= 1
                return
            
            atual = atual.proximo

class SacoTAD[t](Protocol):
    
    def adicionar(self, valor:t) -> None:
        ...
    
    def iterar(self) -> None:
        ...
    
    def buscar(self, valor:t) -> bool:
        ...
    
    def remover(self, valor:t) -> t:
        ...
    
    def libera(self) -> None:
        ...
