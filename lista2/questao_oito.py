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
    
    def k_maior(self, k:int) -> str :
        
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
    
class PegaEntreMaioresOrdInef(PegaEntreMaioresNaoOrdenado):
    
    def __init__(self, n_max):
        super().__init__(n_max)
        
    def insere(self, valor: str) -> None:
        
        # Implementa InsertionSort
        # Complexidade O(n), porque TAD está sempre ordenado
        
        if self.tam >= self.n_max:
            raise OverflowError
        
        i = 0
        
        while (i < self.tam) and (self.dados[i] >= valor): # O(n)
            i += 1
            
        if (self.dados[i] < valor): # O(n)
            for j in range(i, self.tam):
                self.dados[j+1] = self.dados[j]
        
        self.dados[i] = valor # O(1)
        
        self.tam += 1
        
    def maior(self) -> str:
        return self.dados[0]
    
    def segundo_maior(self) -> str:
        return self.dados[1]
    
    def k_maior(self, k:int) -> str:
        return self.dados[k-1]

def pivoteia(arr:array, ini:int, fim:int) -> int:
    
    pivo = arr[fim]
    
    maiores = 0
    
    for i in range(ini, fim):
        if arr[i] >= pivo:
            maiores += 1
            valor = arr[maiores]
            arr[maiores] = arr[i]
            arr[i] = valor
    
    arr[fim] = arr[maiores + 1]
    arr[maiores + 1] = pivo
    
    return maiores + 1

def quick_sort(arr:array, ini:int, fim:int) -> None:
    
    if fim <= ini :
        return None
    
    pos_pivo = pivoteia(arr, ini, fim)
    
    quick_sort(arr, ini, pos_pivo - 1)
    quick_sort(arr, pos_pivo + 1, fim)
    
def quick_select(arr:array[str], k:int, ini:int, fim:int) -> str:

    if (fim - ini < 0):
        raise IndexError
    if (k < 0) or k > (fim - ini + 1):
        raise IndexError("Índice procurado inválido")
    
    while ini <= fim:
        pos_pivo = pivoteia(arr, ini, fim)

        if pos_pivo == k:
            return arr[pos_pivo]

        if k < pos_pivo:
            fim = pos_pivo - 1
        else:
            ini = pos_pivo + 1
    
    return arr[ini]
    
    
    
class PegaEntreMaioresOrdEfic(PegaEntreMaioresNaoOrdenado):
    
    def __init__(self, n_max:int) -> None:
        super().__init__(n_max)
    
    def insere(self, valor:str) -> None:
        
        if self.tam >= self.n_max :
            raise OverflowError('TAD cheio')
        
        self.dados[self.tam] = valor 
        self.tam += 1
        
        quick_sort(self.dados, 0, self.tam)
    
    def k_maior(self, k: int) -> str:
        return self.dados[k-1]
    
    def maior(self) -> str :
        return self.dados[0]
    
    def segundo_maior(self) -> str:
        return self.dados[1]
   
class PegaEntreMaioresQuickSDelect(PegaEntreMaioresNaoOrdenado):
    
    def k_maior(self, k: int) -> str:
        return quick_select(self.dados, k, 0, self.tam - 1)
    
    def maior(self):
        return self.k_maior(1)
    
    def segundo_maior(self) -> str:
        return self.k_maior(2)