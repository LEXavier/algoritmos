from array import array
from fila import FilaStr as Fila

class Pilha2F:
    
    __slots__ = ('fila1', 'fila2', 'n_max', 'tam')
    
    def __init__(self, n_max=1000):
        
        self.n_max = n_max
        
        self.fila1 = Fila(n_max)
        self.fila2 = Fila(n_max)
        
        self.tam = 0
    
    def empilha(self, valor: str) -> None:
        
        self.fila1.enfileira(valor)
        self.tam += 1
    
    def desempilha(self) -> str:
        
        for i in range(self.tam - 1):
            valor = self.fila1.desenfileira()
            self.fila2.enfileira(valor)
        
        dado = self.fila1.desenfileira()
        
        for i in range(self.tam - 1):
            valor = self.fila2.desenfileira()
            self.fila1.enfileira(valor)
        
        self.tam -= 1
        
        return dado
    
    def topo(self) -> str:
        for i in range(self.tam - 1):
            valor = self.fila1.desenfileira()
            self.fila2.enfileira(valor)
        
        dado = self.fila1.desenfileira()
        
        for i in range(self.tam - 1):
            valor = self.fila2.desenfileira()
            self.fila1.enfileira(valor)
        
        return dado
        
    def libera(self) -> None:
        self.fila1.libera()
        self.fila2.libera()
        self.tam = 0

