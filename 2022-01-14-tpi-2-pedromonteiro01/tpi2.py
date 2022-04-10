#encoding: utf8
# Pedro Miguel Afonso de Pina Monteiro
# 97484

from semantic_network import *
from bayes_net import *

from collections import Counter


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def source_confidence(self,user):
        # IMPLEMENT HERE
        assoc_ans = {}
        correct = wrong = 0
        
        for d in self.query_local():
            if isinstance(d.relation, AssocOne):
                key = (d.relation.entity1, d.relation.name)
                if key not in assoc_ans.keys():
                    assoc_ans[key] = [d.relation.entity2]
                else:
                    assoc_ans[key].append(d.relation.entity2)
        
        for k,v in assoc_ans.items():
            assoc_ans[k] = dict(Counter(v))
        
        for d in self.query_local(user=user):
            if isinstance(d.relation, AssocOne):
                votes = list(dict(assoc_ans[(d.relation.entity1, d.relation.name)]).values())
                
                if dict(assoc_ans[(d.relation.entity1, d.relation.name)]).get(d.relation.entity2) == max(votes):
                    correct += 1
                else:
                    wrong += 1
                    
        return (1-0.75**correct)*0.75**wrong
        

    def query_with_confidence(self,entity,assoc):
        # IMPLEMENT HERE
        assoc_ans = {}
        counter = 0 # counter a ser usado para obter o numero de parents
        for d in self.query_local(e1=entity, relname=assoc):
            if isinstance(d.relation, AssocOne):
                key = (d.relation.entity1, d.relation.name)
                if key not in assoc_ans.keys():
                    assoc_ans[key] = [d.relation.entity2]
                else:
                    assoc_ans[key].append(d.relation.entity2)
        
        
        for k,v in assoc_ans.items():
            assoc_ans[k] = dict(Counter(v))
            
        local_assoc = {}
        for d in assoc_ans.values():
            #print(d)
            print(d)
            T = sum(d.values())
            for e2, n in d.items():
                local_assoc[e2] = (n/(2*T)) + (1-n/(2*T))*(1-0.95**n)*(0.95**(T-n)) # fórmula no enunciado
        
        inheritance_conf = {} 
        for d in self.query_local(e1=entity):
            if isinstance(d.relation, (Member,Subtype)):
                counter += 1 # aumentar o numero de parents
                conf = self.query_with_confidence(d.relation.entity2, assoc)
                
                #print(conf)
                for e2, c in conf.items():
                    if e2 in inheritance_conf.keys():
                        inheritance_conf[e2].append(c)
                    else:
                        inheritance_conf[e2] = [c]
        
        parents = counter # o num de parents vai ser igual ao numero de vezes em que a condiçao isistance(Member, Subtype)
                          # é verificada
        for k,v in inheritance_conf.items():
            inheritance_conf[k] = sum(v)/parents # atualizar o valor guardado dividido pelo número de parents
        
        if inheritance_conf == {} and local_assoc != None: # no caso de nao haver inherited results e o local_assoc nao for vazio
            return local_assoc
        elif local_assoc == {} and inheritance_conf != None: # no caso de nao haver local_assoc e o inheritance_conf nao for vazio
            return {k:v*0.9 for k,v in inheritance_conf.items()}
        else: # para o caso de haver local_assoc e inherited results 
            for e2, conf in local_assoc.items():
                local_assoc[e2] *= 0.9
                 
            for k,v in inheritance_conf.items():
                if k in local_assoc.keys(): 
                    local_assoc[k] += v*0.1 # caso e2 já esteja em local_assoc soma-se o valor em inherited results multiplicado por 0.1
                else:
                    local_assoc[k] = v*0.1 # se nao estiver deve ser guardado o valor em inherited results multiplicado por 0.1
            return local_assoc     
    
class MyBN(BayesNet):

    def __init__(self, lstprob = None):
        self.net = [] if lstprob ==None else lstprob
        BayesNet.__init__(self)
        # IMPLEMENT HERE (if needed)

    def individual_probabilities(self):
        # IMPLEMENT HERE
        vars = [var for var in self.dependencies]
        # vars -> [a, b_a, c_s, d, ...]
        
        individual_probs = parents = {}
        for var in vars:
            for p in self.dependencies[var]:
                # p -> frozenset
                parents[var] = self.dependencies[var]
                
        #parents -> {'a':{frozenset():0.003}, ...}
        
        for k,v in parents.items(): # k -> var | v -> {frozenset():0.003}
            prob = 0
            for k1, v1 in v.items(): # k1 -> frozenset() | v1 = 0.003
                if len(k1) == 0: # caso o frozenset esteja vazio, a prob de 'a' vai ser igual a v1
                    individual_probs[k] = v1
                else: # caso o frozenset nao esteja vazio
                    s = list(k1) # transformei em lista para ser mais facil de trabalhar
                    temp = 1
                    for c in s: # c -> ('a', True)
                        if c[1] == True: # caso seja True é apenas multiplicar pelo valor de P('a')
                            temp *= individual_probs[c[0]] 
                        else:
                            temp *= 1 - individual_probs[c[0]] # no caso de ser False, é necessário calcular
                                                               # P(!'a') = 1 - P('a')
                    prob += temp * v1 # a prob é a soma total dos pais quando sao negativos e quando sao positivos
                    
                    individual_probs[k] = prob
        
        return individual_probs
        