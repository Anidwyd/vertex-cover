# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from algos import *

def main():
    G = Graph.from_text('../test/exempleinstance.txt')
    G.show()
    print("* algo couplage  :", couplage(G))
    print("* algo glouton   :", glouton(G))
    print("* branch         :", branch(G))
    print("* branch & bound :", branch_bound(G))
    print("* branch & bound2:", branch_bound2(G))

if __name__ == '__main__':
    main()