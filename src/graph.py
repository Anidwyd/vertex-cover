from random import uniform
from parser import parse

class Graph:

    def __init__(self, nb_sommets, sommets, nb_aretes, adjacences, name='G'):
        self.nb_sommets = nb_sommets
        self.nb_aretes = nb_aretes
        self.sommets = sommets
        self.adjacences = adjacences
        self.name = name if name else 'G'

    # =========================== #
    # --------- OP BASE --------- #
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
        self.nb_sommets -= 1
        self.suppr_aretes(v)

    def suppr_soms(self, ens):
        for v in ens:
            self.suppr_som(v)

    def arites(self):
        return [len(self.adjacences[i]) for i in range(max(self.sommets)+1)]

    def degmax(self):
        return max(self.arites())

    def som_degmax(self):
        tab_arites = self.arites()
        degmax = max(tab_arites)

        return -1 if degmax == 0 else tab_arites.index(degmax) 
    
    def is_empty(self):
        return not self.sommets

    def show(self):
        print("----------- ", self.name, " -----------",
            "\nsommets  :", self.sommets,
            "\naretes   :", self.adjacences,
            "\n----------------------------\n")


    # =========================== #
    # -------- BUILDERS --------- #
    # =========================== #

    @staticmethod
    def from_text(filename, name=None):
        return Graph(*parse(filename), name)

    @staticmethod
    def random(n, p, name=None):
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

        return Graph(n, sommets, nb_aretes, adjacences, name)