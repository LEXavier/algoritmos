from estruturas import Fila, Pilha



def inverte_pilha_com_fila(pilha):
    # Questão 4.a
    # O(n^2 + n) = O(n)

    quantidade = pilha.get_quantidade()
    fila = Fila(quantidade)

    for i in range(quantidade): # n * O(1) = O(n)
        dado = pilha.desempilha() # O(1)
        fila.enfileira(dado) # O(1)

    for i in range(quantidade): # n * O(n) = O(n^2)
        dado = fila.desenfileira() # O(n)
        pilha.empilha(dado) # O(1)
    return pilha

def inverte_pilha_com_pilha(pilha):
    # Questão 4.c
    # 

    quantidade = pilha.get_quantidade()
    pilha_aux = Pilha(quantidade)

    for i in range(quantidade):
        dado = pilha.desempilha()
        pilha_aux.empilha(dado)

    return pilha_aux

def inverte_pilha_com_duas_pilhas(pilha):
    # Questão 4.b
    #

    quantidade = pilha.get_quantidade()

    pilha_aux1 = Pilha(quantidade)
    pilha_aux2 = Pilha(quantidade)

    for i in range(quantidade):
        dado = pilha.desempilha()
        pilha_aux1.empilha(dado)

    for i in range(quantidade):
        dado = pilha_aux1.desempilha()
        pilha_aux2.empilha(dado)

    for i in range(quantidade):
        dado = pilha_aux2.desempilha()
        pilha.empilha(dado)

    return pilha

def inverte_fila_com_duas_filas(fila):
    # Questão 5.b
    #

    quantidade = fila.get_quantidade()

    fila_aux1 = Fila(quantidade)
    fila_aux2 = Fila(quantidade)

    for i in range(quantidade):

        dado1 = fila.desenfileira()

        fila_aux1.enfileira(dado1)

        for j in range(i):
            dado2 = fila_aux2.desenfileira()
            fila_aux1.enfileira(dado2)

        for j in range(i+1):
            dado2 = fila_aux1.desenfileira()
            fila_aux2.enfileira(dado2)
    return fila_aux2

def inverte_fila_com_pilha(fila):
    # Questão 5.a
    # 
    
    quantidade = fila.get_quantidade()
    pilha = Pilha(quantidade)

    for i in range(quantidade):
        dado = fila.desenfileira()
        pilha.empilha(dado)

    for i in range(quantidade):
        dado = pilha.desempilha()
        fila.enfileira(dado)

    return fila