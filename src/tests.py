# ============================ #
# -------- TEST ALGOS -------- #
# ============================ #

# from _typeshed import WriteableBuffer
from os import WIFCONTINUED
import sys
from graph import Graph
from algos import *
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np

import time
import csv


# def get_plot_done(filename):
#     location = '../test/'
#     filename = location + filename

#     n = []
#     tc = []
#     tg = []

#     with open (filename, 'r') as csvfile:
#         plots = csv.reader(csvfile)
        
#         for row in plots:
#             n.append(row[0])
#             tc.append(row[1])
#             tg.append(row[2])

#     plt.title('TEST')
#     plt.axis('scaled')
#     plt.xlabel(n[0])
#     plt.ylabel('temps(s)')
    
#     plt.plot(n[1:], tc[1:], 'r--', n[1:], tg[1:], 'r--')
    
#     plt.legend([tc[0], tg[0]])
#     plt.show()

Nrep = 10

def compare_time_fp(filename, Nmax, algos):
    with open(filename+'_tp.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(['p'] + [algo.__name__ for algo in algos])

        n = Nmax // 4

        for p in range(1, 101, 10):

            row = [0] * len(algos)
            for _ in range(Nrep):
                G = Graph.random(n, p/100)

                for i in range(len(algos)):
                    start = time.time()
                    algos[i](G)
                    row[i] += time.time() - start

            writer.writerow([p/100] + [tn/Nrep for tn in row])


def compare_branch(filename, Nmax, algos):
    location = '../test/'
    filename = location + filename

    step = Nmax//10

    time_rows = [['n'] + [algo.__name__ for algo in algos]]
    node_rows = time_rows[:]

    for n in range(step, Nmax+1, step):
        p = 1/sqrt(n)

        for _ in range(Nrep):
            G = Graph.random(n, p)

            trow = [0] * len(algos)
            nrow = trow[:]

            for i in range(len(algos)):
                start = time.time()
                nnode = algos[i](G)[1]

                trow[i] += time.time() - start
                nrow[i] += nnode

        time_rows.append([n] + [tn/Nrep for tn in trow])
        node_rows.append([n] + [nn/Nrep for nn in nrow])
        
    with open(filename+'_tn.csv', 'w', newline='') as fn:
        csv.writer(fn).writerows(time_rows)

    with open(filename+'_nodes.csv', 'w', newline='') as f:
        csv.writer(f).writerows(node_rows)

    compare_time_fp(filename, Nmax, algos)


def compare_approx(filename, Nmax, algos, algo_opt):
    location = '../test/'
    filename = location + filename
    nb_algos = len(algos)

    step = Nmax//10

    rows = [['n'] + [algo.__name__ for algo in algos]]

    quality = [0] * nb_algos
    optimal = 0

    for n in range(step, Nmax+1, step):
        p = 1/sqrt(n)

        for _ in range(Nrep):
            G = Graph.random(n, p)
            optimal += len(algo_opt(G)[0])

            row = [0] * nb_algos

            for i in range(nb_algos):
                start = time.time()
                approx = algos[i](G)
                row[i] += time.time() - start
                quality[i] += len(approx)

        rows.append([n] + [tn/Nrep for tn in row])
        
    with open(filename+'_tn.csv', 'w', newline='') as fn:
        csv.writer(fn).writerows(rows)

    compare_time_fp(filename, Nmax, algos)

    return [100 * (2 - approx/optimal) for approx in quality]


def main():
    # =========== COMPARAISON COUPLAGE / GLOUTON =========== #
    quality = compare_approx('approx', 100, [couplage, glouton], bb_improved2)
    print('couplage :', quality[0])
    print('glouton  :', quality[1])

    # =========== COMPARAISON B & B ============ #
    compare_branch('branch', 25, [branch, branch_bound, bb_improved, bb_improved2])
    compare_branch('branch_bound', 35, [branch_bound, bb_improved, bb_improved2])
    compare_branch('branch_improved', 150, [bb_improved, bb_improved2])


if __name__ == '__main__':
    main()