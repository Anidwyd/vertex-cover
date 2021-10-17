from copy import deepcopy
from math import ceil, sqrt

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

def branch(G, C=set()):

    if G.nb_aretes > 0:
        # Choisir une arete {u,v} qui n'a pas encore été traitée
        for u in G.sommets:
            
            adj_u = G.adjacences[u]
            if not adj_u: continue

            # Générer le graphe formé à partir de G en supprimant u,
            # et le vertex cover contenant u
            G_u = deepcopy(G)
            G_u.suppr_som(u)
            Cu = branch(G_u, C.union({u}))
            
            for v in adj_u:
                # Générer le graphe formé à partir de G en supprimant v,
                # et le vertex cover contenant v 
                G_v = deepcopy(G)
                G_v.suppr_som(v)
                Cv = branch(G_v, C.union({v}))

                # C prend la valeur du plus petit vertex cover trouvé
                C = Cu if len(Cu) < len(Cv) else Cv

    return C

def branch_bound(G, C=set(), verbose=False):

    delta = G.degmax()

    if delta == 0: return C

    n = G.nb_sommets
    m = G.nb_aretes

    b1 = ceil(m*1.0 / delta)
    b2 = len(couplage(G))/2   # M contient un ensemble de sommets et pas d'aretes
    b3 = (2*n-1 - sqrt((2*n -1)**2 - 8*m)) / 2.0

    binf = max(b1, max(b2, b3))

    if len(C) < binf:


        # Choisir une arete {u,v} qui n'a pas encore été traitée
        for u in G.sommets:
            
            adj_u = G.adjacences[u]
            if not adj_u: continue

            # Générer le graphe formé à partir de G en supprimant u
            # et le vertex cover contenant u
            G_u = deepcopy(G)
            G_u.suppr_som(u)
            Cu = branch(G_u, C.union({u}))
            
            for v in adj_u:
                # Générer le graphe formé à partir de G en supprimant v,
                # et le vertex cover contenant v 
                G_v = deepcopy(G)
                G_v.suppr_som(v)
                Cv = branch_bound(G_v, C.union({v}))

                # C prend la valeur du plus petit vertex cover trouvé
                C = Cu if len(Cu) < len(Cv) else Cv

    return C

def branch_bound2(G, C=set(), verbose=False):

    delta = G.degmax()

    if delta == 0: return C

    n = G.nb_sommets
    m = G.nb_aretes

    b1 = ceil(m*1.0 / delta)
    b2 = len(couplage(G))/2
    b3 = (2*n-1 - sqrt((2*n -1)**2 - 8*m)) / 2.0

    binf = max(b1, max(b2, b3))

    if len(C) < binf:
        # Choisir une arete {u,v} qui n'a pas encore été traitée
        for u in G.sommets:
            
            adj_u = G.adjacences[u]
            if not adj_u: continue

            # Générer le graphe formé à partir de G en supprimant u
            # et le vertex cover contenant u
            G_u = deepcopy(G)
            G_u.suppr_som(u)
            Cu = branch(G_u, C.union({u}))

            # Générer le graphe formé à partir de G en supprimant tous les voisins de u,
            # et le vertex cover contenant v 
            G_v = deepcopy(G)
            G_v.suppr_soms(adj_u)
            Cv = branch_bound2(G_v, C.union(adj_u))

            # C prend la valeur du plus petit vertex cover trouvé
            C = Cu if len(Cu) < len(Cv) else Cv

    return C