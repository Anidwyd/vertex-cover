# ============================ #
# -------- TEST ALGOS -------- #
# ============================ #

import sys
from graph import Graph
from algos import *
import cProfile, pstats

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python3 tests.py <n> <p>")
        exit(1)

    n = int(sys.argv[1])
    p = float(sys.argv[2])
    G = Graph.random(n, p, 'G')

    G.show()
    # print("* algo couplage  :", couplage(G))
    # print("* algo glouton   :", glouton(G))
    # print("* branch_it         :", branch_it(G))
    # print("* branch & bound it :", branch_bound_it(G))
    print("* branch & bound it2:", branch_bound_it2(G))

if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()