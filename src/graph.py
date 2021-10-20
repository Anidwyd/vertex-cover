from random import uniform
from parser import parse

class Graph:
    """
    Un graphe est représenté par une liste de sommets et
    une liste d'arêtes. 
    """

    def __init__(self, nb_sommets, sommets, nb_aretes, aretes):
        self.nb_sommets = nb_sommets
        self.sommets = sommets
        self.nb_aretes = nb_aretes
        self.aretes = aretes

    # =========================== #
    # --------- OP BASE --------- #
    # =========================== #

    def suppr_aretes(self, v):
        """
        Supprime les arêtes incidentes au sommet v.
        :param v: le sommet
        """
        self.aretes = [e for e in self.aretes if v not in e]
        self.nb_aretes = len(self.aretes)

    def suppr_som(G, v):
        """
        Retourne un nouveau graphe obtenu à partir de G en supprimant le sommet v
        et les arêtes incidentes.
        :param G: le graphe
        :param v: le sommet
        :return: une copie de G sans le sommet v et ses arêtes incidentes
        """
        sommets = [u for u in G.sommets if u != v]
        aretes = [e for e in G.aretes if v not in e]

        return Graph(G.nb_sommets-1, sommets, len(aretes), aretes)

    def suppr_soms(G, S):
        """
        Retourne un nouveau graphe obtenu à partir de G en supprimant tous les
        sommets de S et leurs arêtes incidentes.
        :param G: le graphe
        :param S: l'ensemble de sommets
        :return: une copie de G sans les sommets de S et leurs arêtes incidentes
        """
        sommets = [u for u in G.sommets if u not in S]
        aretes = [(u,v) for (u,v) in G.aretes if u not in S and v not in S]

        return Graph(len(sommets), sommets, len(aretes), aretes)

    def arites(self):
        """
        Retourne la liste des degrés des sommets du graphe G.
        :param G: le graphe
        :return: arites la liste des degrés des sommets du graphe G
        """
        arites = [0] * (max(self.sommets)+1)

        # Pour chaque sommet, on compte le nombre d'aretes dans lequel
        # il est impliqué.
        for u in self.sommets:
            for e in self.aretes:
                if u in e: arites[u] += 1

        return arites

    def deg(self, u):
        """
        Retourne le degré du sommet u du graphe.
        :param u: le sommet
        :return: le degré de u
        """
        return self.arites()[u]

    def degmax(self):
        """
        Détermine le degré maximum du graphe.
        :return: le degré maximum du graphe.
        """
        return max(self.arites())

    def som_degmax(self):
        """
        Détermine le sommet de degré maximum du graphe.
        :return: - le sommet de degré maximum dans le graphe ou
                 - -1 si le graphe n'est pas connecté
        """
        tab_arites = self.arites()
        degmax = max(tab_arites)

        return -1 if degmax == 0 else tab_arites.index(degmax) 

    def som_adjacents(self, u):
        """
        Détermine la liste des sommets adjacents à u dans le graphe.
        :param u: le sommet
        :return: les sommets à adjacents à u
        """
        adj = []
        for (v,w) in self.aretes:
            if u == v:
                adj.append(w)
            elif u == w:
                adj.append(v)

        return adj

    def show(self, name=None):
        print("--------------------------------")
        if name : print(('[' + name + ']').center(32))
        print("sommets   :", self.sommets,
            "\naretes    :", self.aretes,
            "\n--------------------------------\n")

    # =========================== #
    # ------- GENERATION -------- #
    # =========================== #

    @staticmethod
    def from_text(filename):
        """
        Génère un graphe à partir d'un fichier texte.
        :param filename: le nom du fichier
        :return: le graphe généré
        """
        return Graph(*parse(filename))

    @staticmethod
    def random(n, p):
        """
        Génère un graphe aléatoire.
        :param n: le nombre de sommet du graphe
        :param p: la probabilité de présence d'une arête
        :return: le graphe généré
        """
        sommets = [i for i in range(n)]
        nb_aretes = 0
        adjacences = [set() for i in range(n)]
        aretes = []

        for i in sommets:
            for j in sommets:
                if i == j or i in adjacences[j]:
                    continue
                
                if uniform(.1, .9) <= p:
                    aretes.append((i,j))
                    adjacences[i].add(j)
                    nb_aretes += 1

        return Graph(n, sommets, nb_aretes, aretes)