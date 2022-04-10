from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

def make_domain(amigos):
    return {A:[(B,C) for B in amigos for C in amigos if A not in [B,C] and B != C ]for A in amigos}     

def constrain(a1, t1, a2, t2):
    b1, c1 = t1
    b2, c2 = t2
    
    if b1 == b2 or c1 == c2:
        return False
    
    if ("Bernardo") in (b1,b2) and ("Bernardo", "Claudio") not in (t1,t2):
        return False
        
    return True

def make_constrain_graph(amigos):
    return {(A1, A2): constrain for A1 in amigos for A2 in amigos if A1 != A2}

cs = ConstraintSearch(make_domain(amigos), make_constrain_graph(amigos))

print(cs.search())
