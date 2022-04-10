# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#
from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Association):
    one = dict()
    
    def __init__(self, e1, assoc, e2):
        print(AssocOne.one)
        
        if assoc not in AssocOne.one:
            AssocOne.one[assoc] = dict()
        assert e2 not in AssocOne.one[assoc] or AssocOne.one[assoc][e2] = self
        Association.__init__(self, e1, assoc, e2)
        
class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        assert isinstance(e2, (int, float))
        Association.__init__(self, e1, assoc, e2)
        

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None,tipo=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2)
                and (tipo == None or isinstance(d.relation, tipo))]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    # Note: We have to convert to set to remove duplicate values
    
    def list_associations(self):
        '''
        l = []
        for d in self.declarations:
            if isinstance(d.relation,Association):
                l.append(d.relation.name)
        return list(set(l))
        '''
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association)]))

    def list_objects(self):
        return list(set([d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))
    
    def list_users(self):
        return list(set([d.user for d in self.declarations]))
    
    def list_types(self):
        return list(set(
            [d.relation.entity2 for d in self.declarations if isinstance(d.relation, (Subtype, Member))] + 
            [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Subtype)]
        ))
        
    def list_relations_by_user(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))
        
    def list_local_associations(self, entity):
        return set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) 
         and entity in [d.relation.entity1, d.relation.entity2]])
    
    def associations_by_user(self, user):
        return len(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) and d.user == user]))
        
    def list_local_associations_by_user(self, entity):
        return list(set(
            [(d.relation.name, d.user) for d in self.declarations if isinstance(d.relation, Association) 
             and entity in [d.relation.entity1, d.relation.entity2]]
        ))
        
    def predecessor(self, e1, e2):
        # e2 is a subtype/member of e1 (in other words, entity1 = e2 and entity2 = e1)
        filtered = [d for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == e2]
        for d in filtered:
            if d.relation.entity2 == e1 or self.predecessor(e1, d.relation.entity2):
                return True
        return False
    
    def predecessor_path(self, e1, e2):
        for d in [
            d 
            for d in self.declarations
            if isinstance(d.relation, (Member,Subtype)) and d.relation.entity1 == e2
        ]:
            if d.relation.entity2 == e1:
                return [e1,e2]
            
            return self.predecessor_path(e1,d.relation.entity2) + [e2]
        
        return None
    
    def query(self, entity, assoc=None):
        pds = self.query_local(e1=entity, tipo=(Member, Subtype))
        pds_assoc = []

        for e2 in [d.relation.entity2 for d in pds]:
            pds_assoc.extend(self.query(e2, assoc))

        local_assoc = self.query_local(e1=entity, rel=assoc, tipo=Association)
        
        return pds_assoc + local_assoc
    
    def query2(self, entity, rel=None):
        pds = self.query_local(e1=entity, tipo=(Member, Subtype))
        pds_assoc = []

        for e2 in [d.relation.entity2 for d in pds]:
            pds_assoc.extend(self.query(e2, rel))
    
        local_assoc = self.query_local(e1=entity, rel=rel)
        
        return pds_assoc + local_assoc
    
    def query_cancel(self, entity, assoc=None):
        pds = self.query_local(e1=entity, tipo=(Member, Subtype))
        
        local_assoc = self.query_local(e1=entity, rel=assoc)

        pds_assoc = []
        for e2 in [d.relation.entity2 for d in pds]:
            pds_assoc.extend([d for d in self.query_cancel(e2, assoc) if d.relation.name not in [l.relation.name for l in local_assoc]])
            
        return pds_assoc + local_assoc
    
    def query_down(self, entity, assoc, first=True):
        
        dcds = self.query_local(e2=entity, tipo=(Member, Subtype))
        
        dcds_assoc = []
        for e1 in [d.relation.entity1 for d in dcds]:
            dcds_assoc.extend(self.query_down(e1, assoc, False))
            
        if first:
            local_assoc = []
        else:
            local_assoc = self.query_local(e1=entity, rel=assoc)
            
        return dcds_assoc + local_assoc
    
    def query_induce(self, entity, assoc):
        dcds_assoc = self.query_down(entity, assoc)
        
        assoc_values = [d.relation.entity2 for d in dcds_assoc]
        
        for c, _ in Counter(assoc_values).most_common(1):
            return c
        
    def query_local_assoc(self, entity, assoc):
        local = self.query_local(e1=entity, rel=assoc, tipo=Association)
        
        for d in local:
            