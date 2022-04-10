import math
#Exercicio 4.1
impar = lambda x: x%2 !=0

#Exercicio 4.2
positivo = lambda x: x>0

#Exercicio 4.3
comparar_modulo = lambda x,y: abs(x) < abs(y)

#Exercicio 4.4
cart2pol = lambda x,y: (math.sqrt(x**2+y**2), math.atan2(y,x))  

#Exercicio 4.5
ex5 = lambda f,g,h: lambda x, y, z: h(f(x, y), g(y, z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista:
        return True
    
    quantificador_universal(lista[1:],f)
    return  f(lista[0])

#Exercicio 4.9
def ordem(lista, f):
    if lista:
        var = ordem(lista[1:],f)
        if var == None:
            return lista[0]
        elif  f(lista[0],var):
            return lista[0]

        else:
            return var
    
    return None

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if lista:
        v,lst = filtrar_ordem(lista[1:],f)
        if v == None:
            return lista[0],[]
        elif  f(lista[0],v):
            lst+=[v]
            return lista[0],lst
        else:
            return v,[lista[0]]+lst
    
    return None,[]

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if lista:
        if len(lista) == 1 :
            return lista
        for i in range (len(lista)):
            if  ordem(lista[i],lista[0]):
                print(lista[0],lista[i])
                lista[0],lista[i] = lista[i],lista[0]
        return [lista[0]]+ordenar_seleccao(lista[1:],ordem)
    
    return None
