# ============================ #
# ======= VERTEX COVER ======= #
# ============================ #

from graph import Graph

def main():
    G = Graph.from_text('test/solo2.txt')
    # G = Graph.random(4, .5)
    G.show()
    print(G.couplage())
    print(G.glouton())
    print(G.branch())

if __name__ == '__main__':
    main()