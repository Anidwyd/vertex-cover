# ============================ #
# ------- VERTEX COVER ------- #
# ============================ #

from graph import Graph
from problems import *

def main():
    G = Graph.from_text('test/solo2.txt')
    # G = Graph.random(4, .5)
    G.show()
    print("* algo couplage    :", couplage(G))
    print("* algo glouton     :", glouton(G))
    print("* branch & reduce  :", branch(G))

if __name__ == '__main__':
    main()