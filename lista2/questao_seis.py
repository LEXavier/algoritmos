from pilha import PilhaInt as Pilha

class PilhaMin(Pilha):
    
    __slots__ = ('mins',)
    
    def __init__(self, n_max):
        
        super().__init__(n_max)
        self.mins = Pilha(n_max)
    
    def empilha(self, valor:int) -> None:
        
        menor = self.mins.topo()
        
        if (self.tam == 0) or (menor <= valor):
            self.mins.empilha(valor)
        
        super().empilha(valor)
        
        
    def desempilha(self) -> int:
        valor = super().desempilha()
        
        menor = self.mins.topo()
        
        if valor == menor:
            self.mins.desempilha()
        
        return valor
    
    def obter_minimo(self) -> int :
        return self.mins.topo()