# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from algos import *

def main():
    # G = Graph.from_text('../test/exempleinstance.txt')
    G = Graph.from_text('../test/bound.txt')
    G.show()
    # print("* algo couplage  :", couplage(G))
    # print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    print("* branch & bound :", branch_bound(G, verbose=True))
    print("* branch & bound2:", branch_bound2(G, verbose=True))

if __name__ == '__main__':
    main()