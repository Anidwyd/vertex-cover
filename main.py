# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from algos import *

def main():
    G = Graph.from_text('test/exempleinstance.txt')
    G.show()
    print("* algo couplage   :", couplage(G))
    print("* algo glouton    :", glouton(G))
    print("* branch & reduce :", branch(G))

if __name__ == '__main__':
    main()