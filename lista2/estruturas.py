# Lista de Exercícios 1

from array import array

class Deque:
    # TAD para a Questão 1.a
    def __init__(self, tamanho):

        self.__tamanho = tamanho
        self.__dados = array('w', '\0' * tamanho)
        self.__quantidade = 0

    def insere_fim(self, valor):
        # Insere elemento no fim
        # O(1)
        if self.__quantidade >= self.__tamanho:
          raise OverflowError('Capacidade máxima do TAD atingida')
        else:
          self.__dados[self.__quantidade] = valor
          self.__quantidade = self.__quantidade + 1

    def remove_fim(self):
        # O(1)
        if self.__quantidade <= 0:
          raise IndexError('TAD vazio')
        else:
          dado = self.__dados[self.__quantidade - 1]
          self.__dados[self.__quantidade - 1] = '\x00'
          self.__quantidade = self.__quantidade - 1
          return dado
  
    def insere_inicio(self, valor):
        # O(n)
        if self.__quantidade >= self.__tamanho:
          raise OverflowError('Capacidade máxima do TAD atingida')
        else:
          for i in range(self.__quantidade, 0, -1):
            self.__dados[i] = self.__dados[i-1]
          self.__dados[0] = valor
          self.__quantidade = self.__quantidade + 1

    def remove_inicio(self):
        # O(n)
        if self.__quantidade <= 0:
          raise IndexError('TAD vazio')
        else:
          dado = self.__dados[0]
          for i in range(self.__quantidade-1):
            self.__dados[i] = self.__dados[i+1]
          self.__dados[self.__quantidade - 1] = '\x00'
          self.__quantidade = self.__quantidade - 1
          return dado

    def inicio(self):
        # O(1)
        if self.__quantidade <= 0:
          raise IndexError('TAD vazio')
        return self.__dados[0]

    def fim(self):
        # O(1)
        if self.__quantidade <= 0:
          raise IndexError('TAD vazio')
        return self.__dados[self.__quantidade-1]

    def libera(self):
        self.__dados.clear()
        self.__tamanho = None
        self.__quantidade = None

##################################

class PilhaDeque:
    # TAD da questão 1.b
    
    def __init__(self, tamanho):
        self.__dados = Deque(tamanho)

    def empilha(self, valor):
        # O(1)
        self.__dados.insere_fim(valor)

    def desempilha(self):
        # O(1)
        return self.__dados.remove_fim()

    def topo(self):
        # O(1)
        return self.__dados.fim()
  
    def libera(self):
        
        self.__dados.libera()

##################################

class FilaDeque:
    # TAD da questão 1.c

    def __init__(self, tamanho):

        self.__dados = Deque(tamanho)
  
    def enfileira(self, valor):

        self.__dados.insere_fim(valor)

    def desenfileira(self):

        return self.__dados.remove_inicio()
  
    def frente(self):

        return self.__dados.inicio()

    def libera(self):
        self.__dados.libera()

##################################

## Questão 2

class Fila:

  def __init__(self, tamanho):
    if tamanho <= 0:
      raise ValueError('Tamanho da fila deve ser positivo')
    self.__tamanho = tamanho
    self.__quantidade = 0
    self.__dados = array('w', '\0' * tamanho)

  def enfileira(self, valor):
    # O(1)
    if self.__quantidade >= self.__tamanho:
      raise OverflowError
    else:
      self.__dados[self.__quantidade] = valor
      self.__quantidade = self.__quantidade + 1

  def desenfileira(self):
    # O(n)
    if self.__quantidade <= 0:
      raise IndexError
    else:
      valor = self.__dados[0]
      for i in range(self.__quantidade-1):
        self.__dados[i] = self.__dados[i+1]
      self.__dados[self.__quantidade-1] = '\0'
      self.__quantidade = self.__quantidade - 1
      return valor

  def frente(self):
    # O(1)
    if self.__quantidade <= 0:
      raise IndexError('Fila vazia')
    return self.__dados[0]

  def libera(self):
    self.__dados = None
    self.__quantidade = None
    self.__tamanho = None

  def get_tamanho(self):
    return self.__tamanho

  def get_quantidade(self):
    return self.__quantidade

#################################

class PilhaDuplaFila:

  def __init__(self, tamanho):
    if tamanho <= 0:
      raise ValueError('Tamanho da pilha deve ser positivo')
    self.__tamanho = tamanho
    self.__quantidade = 0
    self.__fila1 = Fila(tamanho)
    self.__fila2 = Fila(tamanho)

  def empilha(self, valor):
    # O(1)
    if self.__quantidade >= self.__tamanho:
      raise OverflowError('Pilha cheia')
    self.__fila1.enfileira(valor) # O(1)
    self.__quantidade = self.__quantidade + 1

  def topo(self):
    # O(2n^2) = O(n^2)
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')
    for i in range(self.__quantidade): # n * O(n + 1) = O(n^2)
      valor = self.__fila1.desenfileira() # O(n)
      self.__fila2.enfileira(valor) # O(1)
    dado = valor
    for i in range(self.__quantidade): # n * O(n)
      valor = self.__fila2.desenfileira() # O(n)
      self.__fila1.enfileira(valor) # O(1)
    return dado

  def desempilha(self):
    # O(2n^2) = O(n^2)
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')
    for i in range(self.__quantidade): # n * O(n + 1) = O(n^2)
      valor = self.__fila1.desenfileira() # O(n)
      self.__fila2.enfileira(valor) # O(1)
    dado = valor
    for i in range(self.__quantidade-1): # n * O(n - 1 + 1) = O(n^2)
      valor = self.__fila2.desenfileira() # O(n)
      self.__fila1.enfileira(valor) # O(1)
    self.__fila2.desenfileira()
    self.__quantidade = self.__quantidade - 1
    return dado

  def libera(self):
    self.__fila1.libera()
    self.__fila2.libera()
    self.__quantidade = None
    self.__tamanho = None

#################################

class Pilha:

  def __init__(self, tamanho):
    self.tamanho = tamanho
    self.__tamanho = tamanho
    self.__quantidade = 0
    self.__dados = array('w', '\0'*tamanho)

  def empilha(self, valor):
    # O(1)
    if self.__quantidade >= self.__tamanho:
      raise OverflowError('Pilha cheia')

    self.__dados[self.__quantidade] = valor
    self.__quantidade = self.__quantidade + 1

  def desempilha(self):
    # O(1)
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')

    valor = self.__dados[self.__quantidade-1]
    self.__dados[self.__quantidade - 1] = '\0'
    self.__quantidade = self.__quantidade - 1

    return valor

  def topo(self):
    return self.__dados[self.__quantidade - 1]

  def get_tamanho(self):
    return self.__tamanho

  def get_quantidade(self):
    return self.__quantidade

#################################``

class FilaDuplaPilha:

  def __init__(self, tamanho):

    self.__tamanho = tamanho
    self.__quantidade = 0
    self.__pilha1 = Pilha(tamanho)
    self.__pilha2 = Pilha(tamanho)

  def enfileira(self, valor):
    # O(1)
    if self.__quantidade >= self.__tamanho:
      raise OverflowError('Fila cheia')
    self.__pilha1.empilha(valor) # O(1)
    self.__quantidade = self.__quantidade + 1 # O(1)

  def desenfileira(self):
    # O(n + n) = O(n)
    if self.__quantidade <= 0:
      raise IndexError('Fila vazia')

    for i in range(self.__quantidade - 1): # n * O(1) = O(n)
      valor = self.__pilha1.desempilha() # O(1)
      self.__pilha2.empilha(valor) # O(1)
    dado = self.__pilha1.desempilha()
    for i in range(self.__quantidade - 1): # n * O(1) = # O(n)
      valor = self.__pilha2.desempilha() # O(1)
      self.__pilha1.empilha(valor) # O(1)
    self.__quantidade = self.__quantidade - 1
    return dado

  def frente(self):
    # O(n)
    if self.__quantidade <= 0:
      raise IndexError('Fila vazia')
    for i in range(self.__quantidade):
      valor = self.__pilha1.desempilha()
      self.__pilha2.empilha(valor)
    dado = valor
    for i in range(self.__quantidade):
      valor = self.__pilha2.desempilha()
      self.__pilha1.empilha(valor)
    return dado

class PilhaMin:

  def __init__(self, tamanho):
    self.__tamanho = tamanho
    self.__quantidade = 0
    # self.__minimo = None
    self.__dados = array('i', tamanho * [0])
    self.__minimos = PilhaInt(tamanho)

  def get_tamanho(self):
    return self.__tamanho

  def topo(self):
    # O(1)
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')
    return self.__dados[self.__quantidade-1]       

  def empilha(self, valor):
    if self.__quantidade >= self.__tamanho:
      raise OverflowError('Pilha cheia')
    
    self.__dados[self.__quantidade] = valor
    
    if self.__quantidade == 0:
      self.__minimos.empilha(valor) # O(1)
    else:
      if self.__minimos.topo() > valor :
        self.__minimos.empilha(valor) # O(1)
      
    self.__quantidade = self.__quantidade + 1

  def desempilha(self):
    if self.__quantidade <= 0 :
      raise IndexError('Pilha vazia')
    
    dado = self.__dados[self.__quantidade-1]
    
    if self.__minimos.topo() == dado :
      self.__minimos.desempilha()
      
    self.__quantidade = self.__quantidade - 1
    
    return dado

  def obter_minimo(self):
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')
    return self.__minimos.topo()
  
class PilhaInt:

  def __init__(self, tamanho):
    self.tamanho = tamanho
    self.__tamanho = tamanho
    self.__quantidade = 0
    self.__dados = array('i', [0]*tamanho)

  def empilha(self, valor):
    # O(1)
    if self.__quantidade >= self.__tamanho:
      raise OverflowError('Pilha cheia')

    self.__dados[self.__quantidade] = valor
    self.__quantidade = self.__quantidade + 1

  def desempilha(self):
    # O(1)
    if self.__quantidade <= 0:
      raise IndexError('Pilha vazia')

    valor = self.__dados[self.__quantidade-1]
    self.__quantidade = self.__quantidade - 1

    return valor

  def topo(self):
    return self.__dados[self.__quantidade - 1]

  def get_tamanho(self):
    return self.__tamanho

  def get_quantidade(self):
    return self.__quantidade
  
class PegaEntreMaiores:
  
  def __init__(self):
    pass
  
  def insere(self, valor):
    raise NotImplementedError
  
  def maior(self):
    return self.kmaior(1)
  
  def segundo_maior(self):
    return self.kmaior(2)
  
  def kmaior(self, k):
    raise NotImplementedError
  
  def tamanho(self):
    raise NotImplementedError

class PegaEntreMaioresNaoOrdenado:
  def __init__(self):
    pass

class PegaEntreMaioresOrdenadoIneficiente:
  def __init__(self):
    pass

class PegaEntreMaioresOrdenadoEficiente:
  def __init__(self):
    pass

class PegaEntreMaioresQuickSelect:
  def __init__(self):
    pass
  
class SacoVaiEVem:
  def __init__(self):
    pass
