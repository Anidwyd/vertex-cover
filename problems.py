from copy import deepcopy

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

def branch(G, pile=list()):
    
    if G.nb_aretes <= 0: return set()

    C = set(G.sommets)

    for u in G.sommets:
        for v in G.adjacences[u]:
            Cu = set()
            Cv = set()

            G_u = deepcopy(G)
            G_u.suppr_som(u)
            Cu.add(u)
            # pile.append(G_u.sommets)
            Cu.update(branch(G_u, pile))
            # pile.pop()
            
            G_v = deepcopy(G)
            G_v.suppr_som(v)
            Cv.add(v)
            # pile.append(G_v.sommets)
            Cv.update(branch(G_u, pile))
            # pile.pop()

            if min(len(Cu),len(Cv)) < len(C):
                C = Cu if len(Cu) < len(Cv) else Cv

    return C