from typing import Protocol, TypeVar

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