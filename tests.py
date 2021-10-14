# ============================ #
# -------- TEST ALGOS -------- #
# ============================ #

from graph import Graph
from problems import *

def main():
    # TODO: n et p en arguments
    n = 4
    p = .5
    G = Graph.random(n, p, 'G')
    G.show()
    print("* algo couplage    :", couplage(G))
    print("* algo glouton     :", glouton(G))
    print("* branch & reduce  :", branch(G))

if __name__ == '__main__':
    main()