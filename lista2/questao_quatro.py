from fila import FilaStr as Fila
from pilha import PilhaStr as Pilha

def inverte_pilha_com_fila(pilha:Pilha) -> Pilha:
    # Questão 4.a
    # O(n^2 + n) = O(n)

    tam = pilha.tam
    fila = Fila(tam)

    for i in range(tam): # n * O(1) = O(n)
        dado = pilha.desempilha() # O(1)
        fila.enfileira(dado) # O(1)

    for i in range(tam): # n * O(n) = O(n^2)
        dado = fila.desenfileira() # O(n)
        pilha.empilha(dado) # O(1)
    return pilha

def inverte_pilha_com_pilha(pilha:Pilha) -> Pilha:
    # Questão 4.c
    # 

    tam = pilha.tam
    pilha_aux = Pilha(tam)

    for i in range(tam):
        dado = pilha.desempilha()
        pilha_aux.empilha(dado)

    return pilha_aux

def inverte_pilha_com_duas_pilhas(pilha:Pilha) -> Pilha:
    # Questão 4.b
    #

    tam = pilha.tam

    pilha_aux1 = Pilha(tam)
    pilha_aux2 = Pilha(tam)

    for i in range(tam):
        dado = pilha.desempilha()
        pilha_aux1.empilha(dado)

    for i in range(tam):
        dado = pilha_aux1.desempilha()
        pilha_aux2.empilha(dado)

    for i in range(tam):
        dado = pilha_aux2.desempilha()
        pilha.empilha(dado)

    return pilha