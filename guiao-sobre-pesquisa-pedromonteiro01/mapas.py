from constraintsearch import *

region = ['A', 'B', 'C', 'D', 'E']
colors = ['red', 'blue', 'green', 'yellow', 'white']

#constraints: país vizinho não pode ter a mesma cor

mapa = {
    'A': 'BED',
    'B': 'AEC',
    'C': 'BED',
    'D': 'AEC',
    'E': 'ABCD'
}

def constrain(p1, c1, p2, c2):
    return c1 != c2

cs = ConstraintSearch(
    {R: colors for R in region},
    {(P1, P2): constrain for P1 in region for P2 in mapa[P1]}
)
print(cs.search())