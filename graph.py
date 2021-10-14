from random import uniform
from parser import parse
import copy

class Graph:

    def __init__(self, nb_som, sommets, nb_aretes, adjacences):
        self.nb_som = nb_som
        self.nb_aretes = nb_aretes
        self.sommets = sommets
        self.adjacences = adjacences


    # =========================== #
    # ========= OP BASE ========= #
    # =========================== #

    def suppr_aretes(self, v):
        for l in self.adjacences:
            if v in l:
                l.remove(v)
                self.nb_aretes -= 1
        self.nb_aretes -= len(self.adjacences[v])
        self.adjacences[v] = set()

    def suppr_som(self, v):
        self.sommets.remove(v)
        self.nb_som -= 1
        self.suppr_aretes(v)

    def suppr_soms(self, ens):
        for v in ens:
            self.suppr_som(v)

    def arites(self):
        res = [0] * self.nb_som
        for i in range(self.nb_som):
            res[i] = len(self.adjacences[i])

        return res

    def som_degmax(self):
        tab_arites = self.arites()
        degmax = max(tab_arites)

        return -1 if degmax == 0 else tab_arites.index(degmax) 
    
    def is_empty(self):
        return not self.sommets

    def show(self):
        print("sommets:", self.sommets, "\naretes :", self.adjacences)


    # =========================== #
    # ======== BUILDERS ========= #
    # =========================== #

    @staticmethod
    def from_text(filename):
        return Graph(*parse(filename))

    @staticmethod
    def random(n, p):
        sommets = [i for i in range(n)]
        nb_aretes = 0
        adjacences = [set() for i in range(n)]

        for i in range(n):
            for j in sommets:
                if i != j and i not in adjacences[j]:
                    rand = uniform(.1, .9)
                    if rand <= p:
                        adjacences[i].add(j)
                        nb_aretes += 1

        return Graph(n, sommets, nb_aretes, adjacences)


    # =========================== #
    # ====== APROXIMATIONS ====== #
    # =========================== #

    def couplage(self):
        C = set()

        for u in self.sommets:
            for v in self.adjacences[u]:
                if (v not in C) and (u not in C):
                    C.add(v)
                    C.add(u)

        return C

    def glouton(self):
        C = set()
        G = copy.deepcopy(self)
        v_max = G.som_degmax()
        
        while G.nb_aretes > 0:
            C.add(v_max)
            G.suppr_aretes(v_max)
            v_max = G.som_degmax()

        return C


    # =========================== #
    # ===== BRANCH & REDUCE ===== #
    # =========================== #
         
    def branch(self, pile=list()):
        
        if self.nb_aretes <= 0: return set()

        C = set(self.sommets)

        for u in self.sommets:
            for v in self.adjacences[u]:
                Cu = set()
                Cv = set()

                G_u = copy.deepcopy(self)   # G sans u
                G_u.suppr_som(u)
                # pile.append(G_u.sommets)
                Cu.add(u)
                Cu.update(G_u.branch())
                
                G_v = copy.deepcopy(self)   # G sans v
                G_v.suppr_som(v)
                # pile.append(G_v.sommets)
                Cv.add(v)
                Cv.update(G_v.branch())

                if min(len(Cu),len(Cv)) < len(C):
                    C = Cu if len(Cu) < len(Cv) else Cv
        return C