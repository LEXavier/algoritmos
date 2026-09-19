from deque import Deque

class PilhaDeque:
    
    __slots__ = ('dados')
    
    def __init__(self, n_max):
        self.dados = Deque(n_max)
    
    def empilha(self, valor:str) -> None:
        self.dados.insere_fim(valor)
        
    def desempilha(self) -> str:
        return self.dados.remove_fim()
    
    def topo(self) -> str:
        return self.dados.fim()
    
    def libera(self) -> None:
        self.dados = Deque(0)

class FilaDeque:
    
    __slots__ = ('dados')
    
    def __init__(self, n_max):
        self.dados = Deque(n_max)
    
    def enfileira(self, valor: str) -> None:
        self.dados.insere_fim(valor)
    
    def desenfileira(self) -> str:
        return self.dados.remove_inicio()
    
    def frente(self) -> str:
        return self.dados.inicio()
    
    def libera(self) -> None:
        self.dados = Deque(0)