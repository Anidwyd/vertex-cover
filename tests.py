# ============================ #
# -------- TEST ALGOS -------- #
# ============================ #

import sys
from graph import Graph
from algos import *

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python3 tests.py <n> <p>")
        exit(1)

    n = int(sys.argv[1])
    p = float(sys.argv[2])
    G = Graph.random(n, p, 'G')

    G.show()
    print("* algo couplage  :", couplage(G))
    print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    print("* branch & bound :", branch_bound(G))

if __name__ == '__main__':
    main()