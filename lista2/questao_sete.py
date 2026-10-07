from pilha import PilhaStr, PilhaInt
from fila import FilaStr
from array import array

def traduz_operando(char:str, vals:bytes):
    
    idx = ord(char) - ord('A')
    return vals[idx]

def computa_polonesa_reversa(n_var:int, vals:bytes, expr:str) -> int:
    
    operandos = PilhaInt(n_var)
    
    for c in expr:
        
        if ('A' <= c <= 'G'):
            
            op = traduz_operando(c, vals)
            operandos.empilha(op)
        
        elif (c == '*') or (c == '-') or (c == '+') or (c == '/'):
            
            op2 = operandos.desempilha()
            op1 = operandos.desempilha()
            
            if (c == '*') :  res = op1 * op2
            elif (c == '/'): res = op1 // op2
            elif (c == '+'): res = op1 + op2 
            elif (c == '-'): res = op1 - op2
            
            operandos.empilha(res)
            
        else:
            raise ValueError(f'Caracter {c} não esperado')
        
    return operandos.desempilha()

def converte_parentizada_para_polonesa_reversa(n_var:int, expr: str) -> array[str]:
    
    pol_rev = FilaStr(2 * n_var - 1)
    
    operandos = PilhaStr(n_var)
    operadores = PilhaStr(n_var-1)
    
    n_operandos = 0
    opr = '\0'
    
    for c in expr:
        
        if ('A' <= c <= 'G'):
            
            operandos.empilha(c)
            n_operandos += 1
        
        elif (c == '+') or (c == '/') or (c == '*') or (c == '-'):
            
            opr = c
            
        elif (c == ')'):
            
            if n_operandos == 1:
                op = operandos.desempilha()
                
                pol_rev.enfileira(op)
                pol_rev.enfileira(opr)
            
            elif n_operandos == 2:
                
                op2 = operandos.desempilha()
                op1 = operandos.desempilha()
                
                pol_rev.enfileira(op2)
            
            else:
                raise ValueError('Expressão inválida')
    
    resp = array('w', '\0'* pol_rev.tam)
    
    for i in range(pol_rev.tam):
        
        resp[i] = pol_rev.desenfileira()
    
    return resp
    
    # ((A+B)+C)) -> AB+C+