from copy import deepcopy
from math import ceil, sqrt

from graph import Graph

# =========================== #
# ------ APPROXIMATION ------ #
# =========================== #

def couplage(G):
    C = set()

    for (u,v) in G.aretes:
        if (v not in C) and (u not in C):
            C.add(v)
            C.add(u)

    return C

def glouton(G):
    C = set()
    newG = deepcopy(G)
    v_max = G.som_degmax()
    
    while newG.nb_aretes > 0:
        C.add(v_max)
        newG.suppr_aretes(v_max)
        v_max = newG.som_degmax()

    return C

# ============================ #
# ----- BRANCH & REDUCE ------ #
# ============================ #

class Node:
    def __init__(self, G, C, s):
        self.G = G  # graphe actuel
        self.C = C  # couplage actuel
        self.s = s  # sommet(s) actuel(s)

def branch(G):
    C = set()
    u,v = G.aretes[0]
    pile = [Node(G, {u}, u), Node(G, {v}, v)]
    
    cpt = 0
    
    while pile != []:
        curr = pile.pop()
        cpt+=1

        if curr.G.nb_aretes == 0: continue

        newG = Graph.suppr_som(curr.G, curr.s)
        newC = curr.C.union({curr.s})

        if newG.nb_aretes == 0:
            if not C or len(curr.C) < len(C):
                C = newC

        else:
            u,v = newG.aretes[0]
            pile += [Node(newG, newC, u), Node(newG, newC, v)]

    return C, cpt


def get_binf(G):
    delta = G.degmax()

    if delta == 0: return 0

    n = G.nb_sommets
    m = G.nb_aretes

    b1 = ceil(m*1.0 / delta)
    b2 = len(couplage(G))/2
    b3 = (2*n-1 - sqrt((2*n -1)**2 - 8*m)) / 2.0

    return max(b1, max(b2, b3))


def branch_bound(G, approx=couplage):
    C = set()

    u,v = G.aretes[0]
    pile = [ Node(G, {u}, u), Node(G, {v}, v) ]
    
    bsup = -1
    cpt = 0

    while pile != []:
        curr = pile.pop()
        cpt += 1

        if curr.G.nb_aretes == 0: continue

        newG = Graph.suppr_som(curr.G, curr.s)
        newC = curr.C.union({curr.s})

        binf = get_binf(newG)
        
        if binf == 0:
            if bsup < 0 or len(newC) < bsup:
                C = newC
                bsup = len(C)
            continue

        if bsup > 0 and (len(newC) + binf >= bsup): continue

        Creal = approx(newG)

        if len(Creal) + len(newC) < bsup:
            C = newC.union(Creal)
            bsup = len(C)

        else:
            u,v = newG.aretes[0]
            pile += [ Node(newG, newC, u), Node(newG, newC, v) ]

    return C, cpt


def bb_improved(G, approx=couplage):
    C = set()

    u,v = G.aretes[0]
    pile = [ Node(G, {u}, u), Node(G, {v}, v) ]
    
    bsup = -1
    cpt = 0

    while pile != []:
        curr = pile.pop()
        cpt += 1

        if curr.G.nb_aretes == 0: continue

        if type(curr.s) is list:
            newG = Graph.suppr_soms(curr.G, curr.s)
            newC = curr.C.union(curr.s)
        else:
            newG = Graph.suppr_som(curr.G, curr.s)
            newC = curr.C.union({curr.s})

        binf = get_binf(newG)
        
        if binf == 0:
            if bsup < 0 or len(newC) < bsup:
                C = newC
                bsup = len(C)
            continue

        if bsup > 0 and (len(newC) + binf >= bsup): continue

        Creal = approx(newG)

        if len(Creal) + len(newC) < bsup:
            C = newC.union(Creal)
            bsup = len(C)

        else:
            u = newG.aretes[0][0]
            adj_u = newG.som_adjacents(u)
            pile += [ Node(newG, newC, u), Node(newG, newC, adj_u) ]

    return C, cpt