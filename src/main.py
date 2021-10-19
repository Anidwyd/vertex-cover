# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from algos import *
import cProfile, pstats

def main():
    G = Graph.from_text('../test/exempleinstance.txt')
    # G = Graph.from_text('../test/12som.txt')
    G.show()
    # print("* algo couplage  :", couplage(G))
    # print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    print("* branch & bound :", branch_bound(G))
    print("* B & B improved :", bb_improved(G))


if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()