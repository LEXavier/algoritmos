from typing import Protocol, TypeVar 

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