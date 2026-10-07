from pilha import PilhaStr, PilhaInt
from fila import FilaStr
from array import array

def traduz_operando(char:str, vals:bytes):
    
    idx = ord(char) - ord('A')
    return vals[idx]

def computa_polonesa_reversa(n_var:int, vals:bytes, expr:str) -> int:
    
    operandos = PilhaInt(len(expr))
    
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
    
    operadores = PilhaStr(n_var-1)
    
    for c in expr:
        
        if ('A' <= c <= 'G'):
            
            pol_rev.enfileira(c)
        
        elif (c == '+') or (c == '/') or (c == '*') or (c == '-'):
            
            operadores.empilha(c)
            
        elif (c == ')'):
            
            pol_rev.enfileira(operadores.desempilha())
    
    resp = array('w', '\0'* pol_rev.tam)
    
    for i in range(pol_rev.tam):
        
        resp[i] = pol_rev.desenfileira()
    
    return resp
    
    # ((A+B)+C)) -> AB+C+