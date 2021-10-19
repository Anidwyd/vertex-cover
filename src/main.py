# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from algos import *

def main():
    G = Graph.from_text('../test/exempleinstance.txt')
    G.show()
    # print("* algo couplage  :", couplage(G))
    # print("* algo glouton   :", glouton(G))
    # print("* branch           :", branch(G))
    # print("* branch & bound :", branch_bound(G, verbose=True))
    # print("* branch & bound2  :", branch_bound2(G, verbose=True))
    print("* branch_it         :", branch_it(G))
    print("* branch & bound_it :", branch_bound_it(G))
    print("* branch & bound_it2:", branch_bound_it2(G))

if __name__ == '__main__':
    main()