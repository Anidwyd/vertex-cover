from copy import deepcopy
from math import ceil, sqrt

from graph import Graph

# =========================== #
# ------ APPROXIMATION ------ #
# =========================== #

def couplage(G):
    C = set()

    for u in G.sommets:
        for v in G.adjacences[u]:
            if (v not in C) and (u not in C):
                C.add(v)
                C.add(u)

    return C

def glouton(G):
    C = set()
    G_ = deepcopy(G)
    v_max = G.som_degmax()
    
    while G_.nb_aretes > 0:
        C.add(v_max)
        G_.suppr_aretes(v_max)
        v_max = G_.som_degmax()

    return C

# ============================ #
# ----- BRANCH & REDUCE ------ #
# ============================ #

class Node:
    def __init__(self, G, C):
        self.G = G
        self.C = C

def branch_naive(G):
    C = set()
    pile = []
    pile.append(Node())


def branch_it(G):
    nb_node = 0
    pile = [Node(G,set())]
    Cbest = set(G.sommets)

    while pile != []:

        curr = pile.pop()

        if curr.G.nb_aretes == 0:
            if len(curr.C) < len(Cbest):
                Cbest = curr.C
            continue

        checked = []

        for u in curr.G.sommets:
            if u in checked: continue
            checked.append(u)

            adj_u = curr.G.adjacences[u]
            if not adj_u: continue
            checked += adj_u

            for v in adj_u:
                if v in checked: continue
                # Générer le graphe formé à partir de G en supprimant v,
                # et le vertex cover contenant v 
                G_v = deepcopy(curr.G)
                G_v.suppr_som(v)
                pile.append(Node(G_v, curr.C.union({v})))
                nb_node += 1

            # Générer le graphe formé à partir de G en supprimant u,
            # et le vertex cover contenant u
            G_u = deepcopy(curr.G)
            G_u.suppr_som(u)
            pile.append(Node(G_u, curr.C.union({u})))
            nb_node += 1

    return Cbest, nb_node

def get_binf(G):
    delta = G.degmax()

    if delta == 0:
        return delta

    n = G.nb_sommets
    m = G.nb_aretes

    b1 = ceil(m*1.0 / delta)
    b2 = len(couplage(G))/2
    b3 = (2*n-1 - sqrt((2*n -1)**2 - 8*m)) / 2.0

    return max(b1, max(b2, b3))
    
def branch_bound_it(G):
    nb_node = 0
    pile = [Node(G,set())]
    Cbest = set()
    bsup = -1

    while pile != []:
        curr = pile.pop()
        binf = get_binf(curr.G)

        if binf == 0:
            if not Cbest or len(curr.C) < bsup:
                Cbest = curr.C
                bsup = len(Cbest)
            continue

        if bsup > 0 and (len(curr.C) + binf >= bsup):
            continue

        Creal = couplage(curr.G)

        if len(Creal) + len(curr.C) < bsup:
            Cbest = curr.C.union(Creal)
            bsup = len(Cbest)
            continue

        for u in curr.G.sommets:
            adj_u = curr.G.adjacences[u]
            if not adj_u: continue

            for v in adj_u:
                # Générer le graphe formé à partir de G en supprimant v,
                # et le vertex cover contenant v 
                G_v = deepcopy(curr.G)
                G_v.suppr_som(v)
                pile.append(Node(G_v, curr.C.union({v})))
                nb_node += len(adj_u)

            # Générer le graphe formé à partir de G en supprimant u
            G_u = deepcopy(curr.G)
            G_u.suppr_som(u)
            pile.append(Node(G_u, curr.C.union({u})))
            nb_node += 1

    return Cbest, nb_node

def branch_bound_it2(G):
    nb_node = 0
    root = Node(G,set())
    pile = []
    pile.append(root)
    Cbest = set()
    bsup = -1

    while pile != []:
        curr = pile.pop()
        binf = get_binf(curr.G)

        if binf == 0:
            if not Cbest or len(curr.C) < bsup:
                Cbest = curr.C
                bsup = len(Cbest)
            continue

        if bsup > 0 and (len(curr.C) + binf >= bsup):
            continue

        Creal = couplage(curr.G)

        if len(Creal) + len(curr.C) < bsup:
            Cbest = curr.C.union(Creal)
            bsup = len(Cbest)
            continue

        checked = []
        for u in curr.G.sommets:
            if u in checked: continue
            checked.append(u)

            adj_u = [v for v in curr.G.adjacences[u] if v not in checked]
            if not adj_u: continue
            checked += adj_u

            # Générer le graphe formé à partir de G en supprimant tous
            # les voisins de u.
            G_v = deepcopy(curr.G)
            G_v.suppr_soms(adj_u)
            pile.append(Node(G_v, curr.C.union(adj_u)))
            nb_node += len(adj_u)

            # Générer le graphe formé à partir de G en supprimant u
            G_u = deepcopy(curr.G)
            G_u.suppr_som(u)
            pile.append(Node(G_u, curr.C.union({u})))
            nb_node += 1

    return Cbest, nb_node