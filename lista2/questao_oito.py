from array import array
from typing import TypeVar, Protocol, runtime_checkable

t = TypeVar('t')

@runtime_checkable
class PegaEntreMaiores[t](Protocol):
    
    def insere(self, valor:t) -> None:
        ...
        
    def maior(self) -> t:
        ...
    
    def segundo_maior(self) -> t:
        ...
    
    def k_maior(self) -> t:
        ...
    
    def tamanho(self) -> int :
        ...
    
    
class PegaEntreMaioresNaoOrdenado:
    
    __slots__ = ('dados', 'tam', 'n_max')
    
    def __init__(self, n_max:int):
        
        self.tam = 0
        self.n_max = n_max
        self.dados = array('w', '\0' * n_max)
        
    def insere(self, valor:str) -> None: # Complexidade O(1)
        
        if self.tam >= self.n_max:
            raise OverflowError
        
        self.dados[self.tam] = valor
        self.tam += 1
    
    def maior(self) -> str: # Complexidade O(n)
        
        maior = '\0'
        
        for i in range(self.tam):
            
            if (maior < self.dados[i]) or (maior == '\0'):
                
                maior = self.dados[i]
        
        return maior
    
    def segundo_maior(self) -> str : # Complexidade O(n)
        
        maiores = array('w', ['\0','\0'])
        
        for i in range(self.tam):
            
            valor = self.dados[i]
            
            if (valor > maiores[0]):
                
                maiores[1] = maiores[0]
                maiores[0] = valor
            
            elif (valor > maiores[1]):
                
                maiores[1] = valor
        
        return maiores[1]
    
    def k_maior(self, k) -> str :
        
        maiores = array('w', '\0' * self.tam)
        
        maiores[0] = self.dados[0]
        
        for i in range(1, self.tam):
            
            valor = self.dados[i]
            
            j = 0
            
            while (j < i) and (maiores[j] >= valor):
                j += 1
            
            if maiores[j] < valor:
                
                for p in range(j,i):
                    maiores[p+1] = maiores[p]
                    
                maiores[j] = valor
        
        return maiores[k]
    
    def tamanho(self):
        
        return self.tam
            
            
            
        
    