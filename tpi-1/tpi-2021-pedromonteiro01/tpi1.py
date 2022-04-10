# Pedro Miguel Afonso de Pina Monteiro
# 97484

from tree_search import *
from cidades import *

class MyNode(SearchNode):
    def __init__(self,state,parent,cost,heuristic,arg3=None,arg4=None,arg5=None):
        super().__init__(state,parent)
        self.cost = cost
        self.heuristic = heuristic
        self.eval = round(cost + heuristic)
        self.childrens = []

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',seed=0):
        super().__init__(problem,strategy,seed)
        # add root and all_nodes
        # MyNode(state,parent,cost,heuristic)
        heuristic = self.problem.domain.heuristic(self.problem.initial, self.problem.goal)
        root = MyNode(problem.initial, None, 0, heuristic)
        self.all_nodes = [root]
        self.cost = 0
        self.solution_tree = None

    def astar_add_to_open(self,lnewnodes):
        #IMPLEMENT HERE
        # to create this function I used the code provided in the class by professor Diogo Gomes as a base
        self.open_nodes += lnewnodes
        self.open_nodes.sort(key=lambda node: self.all_nodes[node].cost + self.all_nodes[node].heuristic)

    def propagate_eval_upwards(self,node):
        #IMPLEMENT HERE
        #lst = [child.eval for child in node.childrens]
        if node.childrens:
            node.eval = min([child.eval for child in node.childrens])

        if node.parent != None:
            self.propagate_eval_upwards(self.all_nodes[node.parent])
            
    def search2(self,atmostonce=False):
        #IMPLEMENT HERE
        #copy from search()
        while self.open_nodes != []:
            nodeID = self.open_nodes.pop(0)
            node = self.all_nodes[nodeID]
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                return self.get_path(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    #newnode = SearchNode(newstate,nodeID)
                    # create an instance do MyNode
                    #(self,state,parent,cost,heuristic,arg3=None,arg4=None,arg5=None)
                    cost = node.cost + self.problem.domain.cost(node.state, a)
                    heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                    newnode = MyNode(newstate, nodeID, cost, heuristic)
                    states = [node.state for node in self.all_nodes]
                    is_state_in = [newstate in states]
                    if atmostonce and True in (is_state_in):
                        all_nodes = self.all_nodes[states.index(newstate)]
                        
                        if newnode.cost < all_nodes.cost:
                            self.all_nodes[states.index(newstate)] = newnode # in case that newnode.cost >=
                    else:                             # self.all_nodes[states.index(newstate)].cost should continue
                        self.all_nodes.append(newnode)
                        lnewnodes.append(len(self.all_nodes)-1) # node position will be len - 1
                        
                    node.childrens.append(newnode)  
            self.propagate_eval_upwards(node)
            self.add_to_open(lnewnodes)
            
        return None

    def repeated_random_depth(self,numattempts=3,atmostonce=False):
        #IMPLEMENT HERE
        cost = 0
        
        #  run a certain number of attempts of 'rand_depth' and pick the best result in terms of cost
        for i in range(numattempts):
            strategy = 'rand_depth' # 'rand_depth' is a strategy defined in tree_search
            tree = MyTree(self.problem, strategy, i) # i -> seed in each attempt should be the number of the attempt
            search = tree.search2()
            if cost != 0:
                if tree.cost < cost:
                    cost = tree.cost
                    self.solution_tree = tree
            #else       
            cost = tree.cost
            self.solution_tree = tree
                
        return search   

    def make_shortcuts(self):
        #IMPLEMENT HERE
        # https://www.w3schools.com/python/ref_list_index.asp
        cities = self.get_path(self.solution)
        connections = self.problem.domain.connections
        self.used_shortcuts=[]
        shortcuts = [(c1,c2) for c1 in cities for c2 in cities for conn in connections 
                               if c1 in conn and c2 in conn and cities.index(c2)-cities.index(c1) > 1]
        for shortcut in shortcuts:
            for i in range(len(cities)-2):
                if cities[i]==shortcut[0] and cities[i+2]==shortcut[1]:
                    cities.pop(i+1)
                    self.used_shortcuts.append(shortcut)

        return cities 


class MyCities(Cidades):
    def __init__(self, connections, coordinates):
        super().__init__(connections, coordinates)
    
    def maximum_tree_size(self,depth):   # assuming there is no loop prevention
        #IMPLEMENT HERE
        #actions = sum([len(self.actions(c)) for c in self.coordinates.keys()])   
        #self.coordinates.keys() returns all cities
        avg_branch = sum([len(self.actions(c)) for c in self.coordinates.keys()]) / len(self.coordinates)
        return (avg_branch**(depth + 1) - 1)/(avg_branch - 1) # source: AED course slides