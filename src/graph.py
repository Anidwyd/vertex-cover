from random import uniform
from parser import parse

class Graph:

    def __init__(self, nb_sommets, sommets, nb_aretes, aretes):
        self.nb_sommets = nb_sommets
        self.sommets = sommets
        self.nb_aretes = nb_aretes
        self.aretes = aretes

    # =========================== #
    # --------- OP BASE --------- #
    # =========================== #

    def suppr_aretes(self, v):
        self.aretes = [e for e in self.aretes if v not in e]
        self.nb_aretes = len(self.aretes)

    def suppr_som(G, v):
        sommets = [u for u in G.sommets if u != v]
        aretes = [e for e in G.aretes if v not in e]

        return Graph(G.nb_sommets-1, sommets, len(aretes), aretes)

    def suppr_soms(G, L):
        sommets = [u for u in G.sommets if u not in L]
        aretes = [(u,v) for (u,v) in G.aretes if u not in L and v not in L]

        return Graph(len(sommets), sommets, len(aretes), aretes)

    def arites(self):
        arites = [0] * (max(self.sommets)+1)

        for u in self.sommets:
            for e in self.aretes:
                if u in e: arites[u] += 1

        return arites

    def degmax(self):
        return max(self.arites())

    def som_degmax(self):
        tab_arites = self.arites()
        degmax = max(tab_arites)

        return -1 if degmax == 0 else tab_arites.index(degmax) 

    def som_adjacents(self, u):
        adj = []
        for (v,w) in self.aretes:
            if u == v:
                adj.append(w)
            elif u == w:
                adj.append(v)

        return adj
    
    def is_empty(self):
        return not self.sommets

    def show(self):
        print("----------------------------",
            "\nsommets   :", self.sommets,
            "\naretes    :", self.aretes,
            "\n----------------------------\n")

    # =========================== #
    # -------- BUILDERS --------- #
    # =========================== #

    @staticmethod
    def from_text(filename):
        return Graph(*parse(filename))

    @staticmethod
    def random(n, p):
        sommets = [i for i in range(n)]
        nb_aretes = 0
        adjacences = [set() for i in range(n)]
        aretes = []

        for i in range(n):
            for j in sommets:
                if i != j and i not in adjacences[j]:
                    rand = uniform(.1, .9)
                    if rand <= p:
                        aretes.append((i,j))
                        adjacences[i].add(j)
                        nb_aretes += 1

        return Graph(n, sommets, nb_aretes, aretes)