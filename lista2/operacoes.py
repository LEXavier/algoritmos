# from estruturas import Fila, Pilha, PilhaInt
# from array import array











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
            