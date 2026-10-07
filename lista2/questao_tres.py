from array import array
from pilha import PilhaStr as Pilha

class Fila2P:
    
    __slots__ = ('pilha1', 'pilha2', 'n_max', 'tam')

    def __init__(self, n_max):

        self.n_max = n_max
        self.pilha1 = Pilha(n_max)
        self.pilha2 = Pilha(n_max)
        self.tam = 0

    def enfileira(self, valor):
        
        if self.tam >= self.n_max:
            raise OverflowError('Fila cheia')
        self.pilha1.empilha(valor) 
        self.tam += 1 

    def desenfileira(self):
        
        if self.tam <= 0:
            raise IndexError('Fila vazia')

        for i in range(self.tam - 1): # n * O(1) = O(n)
            valor = self.pilha1.desempilha() # O(1)
            self.pilha2.empilha(valor) # O(1)
            
        dado = self.pilha1.desempilha()
        
        for i in range(self.tam - 1): # n * O(1) = # O(n)
            valor = self.pilha2.desempilha() # O(1)
            self.pilha1.empilha(valor) # O(1)
            
        self.tam = self.tam - 1
        return dado

    def frente(self):
        # O(n)
        if self.tam <= 0:
            raise IndexError('Fila vazia')
        
        for i in range(self.tam):
            valor = self.pilha1.desempilha()
            self.pilha2.empilha(valor)
            
        dado = valor
        
        for i in range(self.tam):
            valor = self.pilha2.desempilha()
            self.pilha1.empilha(valor)
        
        return dado