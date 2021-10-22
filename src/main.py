"""
VERTEX COVER SOLVER
-------------------

Canitrot Julien
Dubreuil Jules
"""

# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

import sys
from graph import Graph
from algos import *

def main():

    filename = sys.argv[1] if len(sys.argv) == 2 else '12som.txt'

    G = Graph.from_text('../data/graphs' + filename)

    # G = Graph.random(int(sys.argv[1]), float(sys.argv[2]))
    G.show()
    print("* algo couplage  :", couplage(G))
    print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    print("* branch & bound :", branch_bound(G))
    print("* B & B improved :", bb_improved(G))
    print("* B & B improved2:", bb_improved2(G))

if __name__ == '__main__':
    main()