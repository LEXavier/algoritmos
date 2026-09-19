from fila import FilaStr as Fila
from pilha import PilhaStr as Pilha

def inverte_fila_com_pilha(fila:Fila) -> Fila:
    # Questão 5.a
    # 
    
    quantidade = fila.tam
    pilha = Pilha(quantidade)

    for i in range(quantidade):
        dado = fila.desenfileira()
        pilha.empilha(dado)

    for i in range(quantidade):
        dado = pilha.desempilha()
        fila.enfileira(dado)

    return fila

def inverte_fila_com_duas_filas(fila:Fila) -> Fila:
    # Questão 5.b
    #

    quantidade = fila.tam

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