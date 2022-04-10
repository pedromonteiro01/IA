#Exercicio 1.1
def comprimento(lista):
    if lista:
        return 1 + comprimento(lista[1:])
    return 0

#Exercicio 1.2
def soma(lista):
    if comprimento(lista)==0:
        return 0
    else:
        return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
    if comprimento(lista)==0:
        return False
    if lista[0]==elem:
        return True
    return existe(lista[1:],elem)

#Exercicio 1.4
def concat(l1, l2):
    if comprimento(l1) == 0:
        return l2
    elif comprimento(l2) == 0:
        return l1
    else:
        l1.append(l2[0])
        return concat(l1,l2[1:])
    

#Exercicio 1.5
def inverte(lista):
    if comprimento(lista) != 0:
        l = lista.pop(0)
        inverte(lista)
        lista.append(l)
        return lista
    else:
        return []

#Exercicio 1.6
def capicua(lista):
    if comprimento(lista) == 0:
        return False
    else:
        if lista[0] == lista[-1]:
            capicua(lista[1:-1])
            return True
        else:
            return False
    

#Exercicio 1.7
def explode(lista):
    if comprimento(lista) == 0:
        return []
    else:
        return concat(lista[0], explode(lista[1:]))

#Exercicio 1.8
def substitui(lista, original, novo):
    if comprimento(lista) == 0:
        return []
    
    if lista[0] == original:
        lista[0] = novo
     
    return [lista[0]] + substitui(lista[1:],original,novo)
            
#Exercicio 1.9  #TODO
def junta_ordenado(lista1, lista2):
    if comprimento(lista1) == 0:
        return lista2
    elif comprimento(lista2) == 0:
        return lista1
    else:
        lambda_sort = lambda x,y: [min(x,y),max(x,y)]
        return lambda_sort(lista1[0], lista2[0]) + junta_ordenado(lista1[1:], lista2[1:])

#Exercicio 1.10
def conjunto(lista):
    pass

#Exercicio 2.1
def separar(lista):
    if lista:
        a,b = lista[0]
        listaA, listaB = separar(lista[1:])
        return [a] + listaA, [b] + listaB
    
    return [], []

#Exercicio 2.2
def remove_e_conta(lista,elem):
    if lista:
        (lst, i) = remove_e_conta(lista[1:],elem) 
        
        if lista[0] == elem:
            return (lst, i+1) 
        else:
            return [lista[0]] + lst, i #[lista[0]] + lst -> list + list -> list
        
    if lista == []:
        return ([], 0)

def elemento_total(lista, elem):
    pass

#Exercicio 3.1
def cabeca(lista):
    if comprimento(lista) == 0:
        return None
    
    return lista[0]

#Exercicio 3.2
def cauda(lista):
    if comprimento(lista) == 0:
        return None
    
    return lista[1:]

#Exercicio 3.3
def juntar(l1, l2):
    if len(l1) != len(l2):
        return None
    
    if l1 == []:
        return []
    
    return [(l1[0], l2[0])] + juntar(l1[1:], l2[1:])

#Exercicio 3.4
def menor(lista):
    if comprimento(lista) == 0:
        return None
    
    m = menor(lista[1:])
    if m is None or lista[0] < m:
        return lista[0]
    
    return m

#Exercicio 3.6
def max_min(lista):
	pass