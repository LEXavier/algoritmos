# from estruturas import Fila, Pilha, PilhaInt
# from array import array



# def inverte_pilha_com_fila(pilha):
#     # Questão 4.a
#     # O(n^2 + n) = O(n)

#     quantidade = pilha.get_quantidade()
#     fila = Fila(quantidade)

#     for i in range(quantidade): # n * O(1) = O(n)
#         dado = pilha.desempilha() # O(1)
#         fila.enfileira(dado) # O(1)

#     for i in range(quantidade): # n * O(n) = O(n^2)
#         dado = fila.desenfileira() # O(n)
#         pilha.empilha(dado) # O(1)
#     return pilha

# def inverte_pilha_com_pilha(pilha):
#     # Questão 4.c
#     # 

#     quantidade = pilha.get_quantidade()
#     pilha_aux = Pilha(quantidade)

#     for i in range(quantidade):
#         dado = pilha.desempilha()
#         pilha_aux.empilha(dado)

#     return pilha_aux

# def inverte_pilha_com_duas_pilhas(pilha):
#     # Questão 4.b
#     #

#     quantidade = pilha.get_quantidade()

#     pilha_aux1 = Pilha(quantidade)
#     pilha_aux2 = Pilha(quantidade)

#     for i in range(quantidade):
#         dado = pilha.desempilha()
#         pilha_aux1.empilha(dado)

#     for i in range(quantidade):
#         dado = pilha_aux1.desempilha()
#         pilha_aux2.empilha(dado)

#     for i in range(quantidade):
#         dado = pilha_aux2.desempilha()
#         pilha.empilha(dado)

#     return pilha

# def inverte_fila_com_duas_filas(fila):
#     # Questão 5.b
#     #

#     quantidade = fila.get_quantidade()

#     fila_aux1 = Fila(quantidade)
#     fila_aux2 = Fila(quantidade)

#     for i in range(quantidade):

#         dado1 = fila.desenfileira()

#         fila_aux1.enfileira(dado1)

#         for j in range(i):
#             dado2 = fila_aux2.desenfileira()
#             fila_aux1.enfileira(dado2)

#         for j in range(i+1):
#             dado2 = fila_aux1.desenfileira()
#             fila_aux2.enfileira(dado2)
#     return fila_aux2

# def inverte_fila_com_pilha(fila):
#     # Questão 5.a
#     # 
    
#     quantidade = fila.get_quantidade()
#     pilha = Pilha(quantidade)

#     for i in range(quantidade):
#         dado = fila.desenfileira()
#         pilha.empilha(dado)

#     for i in range(quantidade):
#         dado = pilha.desempilha()
#         fila.enfileira(dado)

#     return fila

# def eh_operador(char):
#     return (char == '-') or (char == '+') or (char == '*') or (char == '/')

# def eh_operando(char):
#     return (char >= 'A') and (char <= 'Z')

# def mapeia_operando(char, valores):
#     if char == 'A':
#         return valores[0]
#     elif char == 'B':
#         return valores[1]
#     elif char == 'C':
#         return valores[2]
#     elif char == 'D':
#         return valores[3]
#     elif char == 'E':
#         return valores[4]
#     elif char == 'F':
#         return valores[5]
#     elif char == 'G':
#         return valores[6]
#     else:
#         raise ValueError(f'Expressão com valor operando {char}')
    
# def opera(a, b, operacao):
#     if operacao == '+':
#         return a+b
#     if operacao == '-':
#         return a-b
#     if operacao == '*':
#         return a*b
#     if operacao == '/':
#         if b > 0:
#             return int(a/b)
#         else:
#             raise ZeroDivisionError

# def avalia_polonesa_reversa(expressao, valores):
#     # Considerando o mapeamento: A <- valores[0]; B <- valores[1]; ... ; G <- valores[6]
    
#     tamanho = len(expressao)
#     operandos = PilhaInt(tamanho)
    
#     for i in range(tamanho):
#         char = expressao[i]  
#         if eh_operador(char):  
            
#             operando1 = operandos.desempilha()
#             operando2 = operandos.desempilha()
#             valor = opera(operando2, operando1, char) 
#             operandos.empilha(valor)
#             # print(f"{operando2} {char} {operando1} = {valor}")
#         else:
#             if eh_operando(char):
#                 valor = mapeia_operando(char, valores)
#                 operandos.empilha(valor)
#             else:
#                 raise ValueError(f'Expressão com valor inesperado {expressao[i]}')
            
#     return operandos.desempilha()
            

# def polonesa_reversa(expressao):
    
#     tamanho = len(expressao)
    
#     pol = Fila(tamanho)
#     operadores = Pilha(tamanho)
#     tamanho_final = 0
    
#     for i in range(tamanho):
        
#         char = expressao[i]
        
#         if eh_operando(char) :
#             pol.enfileira(char)
#             tamanho_final = tamanho_final + 1
#         elif eh_operador(char) :
#             operadores.empilha(char)
#         elif char == ')' :
#             operador = operadores.desempilha()
#             pol.enfileira(operador)
#             tamanho_final = tamanho_final + 1
#         elif char != '(':
#             raise ValueError(f'Expressão com valor inesperado {expressao[i]}')
        
#     expressao_pr = array('w', tamanho_final * '\0')
     
#     for i in range(tamanho_final):
#         expressao_pr[i] = pol.desenfileira()
    
#     return expressao_pr
            