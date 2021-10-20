from copy import deepcopy
from math import ceil, sqrt

from graph import Graph

# =========================== #
# ------ APPROXIMATION ------ #
# =========================== #

def couplage(G):
    """
    Détermine une couverture réalisable de G
    à partir d'un couplage de G.
    :param G: le graphe
    :return: C une couverture de G
    """
    C = set()

    for (u,v) in G.aretes:
        if (v not in C) and (u not in C):
            C.add(v)
            C.add(u)

    return C

def glouton(G):
    """
    Détermine une couverture de G de manière gloutonne
    (on ajoute toujours le sommet de degré maximum).
    :param G: le graphe
    :return: C une couverture de G
    """
    C = set()
    newG = deepcopy(G)
    
    while newG.nb_aretes > 0:
        v_max = newG.som_degmax()
        C.add(v_max)
        newG.suppr_aretes(v_max)

    return C

# ============================ #
# ----- BRANCH & REDUCE ------ #
# ============================ #

# ============================ #

class Node:
    """
    Noeud de l'arbre de recherche.
    Contient le graphe actuel, sa couverture (partielle), et le
    sommet (ou la liste de sommets) ajouté(e) par le noeud parent.
    """
    def __init__(self, G, C, S):
        self.G = G
        self.C = C
        self.S = S



def get_binf(G):
    """
    Determine une borne une borne inférieure de la taille de la
    couverture du graphe G.
    :param G: le graphe
    :return: une borne inférieure de |couverture|
    """
    delta = G.degmax()

    if delta == 0: return 0

    n = G.nb_sommets
    m = G.nb_aretes

    b1 = ceil(m*1.0 / delta)
    b2 = len(couplage(G))/2
    b3 = (2*n-1 - sqrt((2*n -1)**2 - 8*m)) / 2.0

    return max(b1, max(b2, b3))

# ============================ #


def branch(G):
    """
    Détermine un vertex-cover du graphe G en utilisant un algorithme
    de branchement simple.
    :param G: le graphe
    :return: C une couverture de G
    """

    # Si le graphe n'est pas connecté, renvoyer l'ensemble vide
    if G.nb_aretes == 0: return set()

    C = set()   # Ensemble de sommets vide

    # Recupèrer la "première" arête (u,v) de G.
    # Ajouter dans la pile le cas ou u est dans la couverture et
    # celui ou v est dans la couverture
    u,v = G.aretes[0]
    pile = [ Node(G, {u}, u) , Node(G, {v}, v) ]
    
    cpt = 0     # Compteur du nombre de noeuds créés
    
    while pile != []:
        # Recupèrer le dernier noeud de la pile  
        curr = pile.pop()
        cpt += 1

        # Déterminer le graphe qui ne contient pas le ommet S et ses
        # arêtes incidentes, et ajouter S à la couverture actuelle
        newG = Graph.suppr_som(curr.G, curr.S)
        newC = curr.C.union({curr.S})

        # Si le nouveau graphe n'a plus d'arêtes, on se
        # trouve sur une feuille.
        if newG.nb_aretes == 0:
            # Si la taille de la couverture actuelle est une meilleure
            # solution, ou si C est vide, on met C à jour
            if not C or len(curr.C) < len(C):
                C = newC

        # Sinon on branche à partir d'une arête (u,v) du nouveau graphe
        else:
            u,v = newG.aretes[0]
            pile += [ Node(newG, newC, u) , Node(newG, newC, v) ]

    return C, cpt


def branch_bound(G, approx=couplage):
    """
    Détermine un vertex-cover du graphe G en utilisant un algorithme
    de branch and bound.
    :param G: le graphe
    :param approx: algorithme de calcul d'une solution réalisable
    :return: C une couverture de G
    """
    if G.nb_aretes == 0: return set()

    C = set()
    u,v = G.aretes[0]
    pile = [ Node(G, {u}, u) , Node(G, {v}, v) ]
    
    bsup = -1000    # borne supérieure
    cpt = 0

    while pile != []:
        curr = pile.pop()
        cpt += 1

        newG = Graph.suppr_som(curr.G, curr.S)
        newC = curr.C.union({curr.S})

        # Calcule de la borne inférieur du noeud
        binf = get_binf(newG)
        
        # Si la borne inf est nulle, on est sur une feuille,
        # mise à jour de C et de la borne sup.
        if binf == 0:
            if bsup < 0 or len(newC) < bsup:
                C = newC
                bsup = len(C)
            continue

        # Si le noeud ne peut s'assurer une solution de taille plus
        # petite que la borne sup, élaguer.
        if bsup > 0 and (len(newC) + binf >= bsup): continue

        # Sinon, calculer une solution réalisable pour le noeud
        Creal = approx(newG)

        # Si cette solution + la couverture actuelle est meilleure
        # que C : mise à jour de C + élagage.
        if len(Creal) + len(newC) < bsup:
            C = newC.union(Creal)
            bsup = len(C)

        # Sinon on branche à partir d'une arête (u,v) du nouveau graphe
        else:
            u,v = newG.aretes[0]
            pile += [ Node(newG, newC, u) , Node(newG, newC, v) ]

    return C, cpt


def bb_improved(G, approx=couplage):
    """
    Détermine un vertex-cover du graphe G en utilisant un algorithme
    de branch and bound amélioré.
    :param G: le graphe
    :return: C une couverture de G
    """
    if G.nb_aretes == 0: return set()

    C = set()
    u,v = G.aretes[0]
    pile = [ Node(G, {u}, u) , Node(G, {v}, v) ]
    
    bsup = -1
    cpt = 0

    while pile != []:
        curr = pile.pop()
        cpt += 1

        if type(curr.S) is list:
            # Si S est une liste de sommets :
            # - créer le graphe newG, obtenu en supprimant S du graphe courant.
            # - ajouter le sommets de S à la couverture

            # sup1 = [w for w in curr.S if curr.G.deg(w) > 1]
            newG = Graph.suppr_soms(curr.G, curr.S)
            newC = curr.C.union(curr.S)
        else:
            newG = Graph.suppr_som(curr.G, curr.S)
            newC = curr.C.union({curr.S})

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

        # Brancher à partir du sommet de degré maximum u,
        # et de la liste de ses sommets adjacents. 
        else:
            u = newG.som_degmax()
            adj_u = newG.som_adjacents(u)
            pile += [ Node(newG, newC, u) , Node(newG, newC, adj_u) ]

    return C, cpt