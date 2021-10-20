# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

import sys
from graph import Graph
from algos import *
import cProfile, pstats

def main():

    # filename = sys.argv[1] if len(sys.argv) == 2 else '12som.txt'

    # G = Graph.from_text('../data/' + filename)

    G = Graph.random(int(sys.argv[1]), float(sys.argv[2]))
    # G.show()
    # print("* algo couplage  :", couplage(G))
    # print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    # print("* branch & bound :", branch_bound(G))
    # print("* B & B improved :", bb_improved(G))
    # print("* B & B improved2:", bb_improved2(G))

if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()