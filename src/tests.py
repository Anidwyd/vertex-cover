# ============================ #
# -------- TEST ALGOS -------- #
# ============================ #

from math import nan
from graph import Graph
from algos import *
import matplotlib.pyplot as plt

import pandas as pd

import time
import csv

Nrep = 20
location = '../test/'

def get_plot(filename, title, columns=[], ylabel="temps de calcul (s)", xlim=None, ylim=None, xscale=None, yscale=None):
    filename = location + filename
    data = pd.read_csv(filename, index_col=0)
    
    index = data.index.name

    mean = data.groupby(index).mean()
    std = data.groupby(index).std()

    columns = set(mean).intersection(set(columns)) if columns else mean

    for col in columns:
        mean[col].plot()
        plt.fill_between(mean.index, mean[col]-std[col], mean[col]+std[col], alpha=.2)
    
    if xlim != None: plt.xlim(0, xlim)
    if ylim != None: plt.ylim(0, ylim)

    if xscale: plt.xscale(xscale)
    if yscale: plt.yscale(yscale)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    # plt.savefig('../data/img/' + filename.replace('.csv','') + '.png')

# ==== TEMPS EN FONCTION DE P ==== #

def compare_time_fp(filename, algos, n):
    filename = location + filename

    with open(filename+'_tp.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(['p'] + [algo.__name__ for algo in algos])

        for p in range(1, 101, 10):

            for _ in range(Nrep):
                G = Graph.random(n, p/100)

                row = [p/100]
                for algo in algos:
                    start = time.time()
                    algo(G)
                    row.append(time.time() - start)

                writer.writerow(row)

# ==== TEMPS ET NB NOEUDS EN FONCTION DE N ==== #

def compare_branch(filename, algos, l_nmax):
    filename = location + filename
    nb_algos = len(algos)

    Nmax = max(l_nmax)
    step = Nmax//20

    time_rows = [['n'] + [algo.__name__ for algo in algos]]
    node_rows = time_rows[:]

    for n in range(step, Nmax+1, step):
        p = 1/sqrt(n)

        for _ in range(Nrep):
            G = Graph.random(n, p)

            trow = [n]
            nrow = [n]

            for i in range(nb_algos):
                if n <= l_nmax[i]:
                    start = time.time()
                    nnode = algos[i](G)[1]

                    time_taken = time.time() - start

                    trow.append(time_taken)
                    nrow.append(nnode)
                    
                else:
                    trow.append(nan)
                    nrow.append(nan)

            time_rows.append(trow)
            node_rows.append(nrow)
        
    with open(filename+'_tn.csv', 'w', newline='') as fn:
        csv.writer(fn).writerows(time_rows)

    with open(filename+'_nodes.csv', 'w', newline='') as f:
        csv.writer(f).writerows(node_rows)

    compare_time_fp(filename, algos, 20)


# ==== TEMPS ET QUALITE EN FONCTION DE N ==== #

def compare_approx(filename, Nmax, algos, algo_opt=None):
    filename = location + filename
    nb_algos = len(algos)

    step = Nmax//10

    rows = [['n'] + [algo.__name__ for algo in algos]]
    avg_quality = [0] * (nb_algos+1)

    for n in range(step, Nmax+1, step):
        p = 1/sqrt(n)

        for _ in range(Nrep):
            G = Graph.random(n, p)

            if algo_opt != None:
                optimal = len(algo_opt(G)[0])
                avg_quality[-1] += optimal

            row = [n]
            for i in range(nb_algos):
                if algo_opt == None:
                    start = time.time()
                    algos[i](G)
                    row.append(time.time() - start)
                else:
                    approx = len(algos[i](G))
                    row.append(2. - approx / optimal)
                    avg_quality[i] += approx

            rows.append(row)
    
    with open(filename+'_tn.csv', 'w', newline='') as fn:
        csv.writer(fn).writerows(rows)

    if algo_opt != None:
        return [100 * (2 - avg_quality[i] / avg_quality[-1]) for i in range(nb_algos)]

    compare_time_fp(filename, algos, 100)


def main():
    # =========== COMPARAISON COUPLAGE / GLOUTON =========== #
    # compare_approx('approx', 1000, [couplage, glouton])
    # quality = compare_approx('quality', 150, [couplage, glouton], bb_improved2)
    # print('couplage :', quality[0])
    # print('glouton  :', quality[1])
    
    get_plot('approx_tn.csv', 'temps de calcul en fonction de n', yscale='log')
    get_plot('approx_tp.csv', 'temps de calcul en fonction de p', yscale='log')
    get_plot('quality_tn.csv', "qualité d'approximation en fonction de n", ylabel='quality')

    # =========== COMPARAISON B & B ============ #
    # compare_branch('branch_base', [branch, branch_bound], [24, 36])
    # compare_branch('branch', [bb_improved, bb_improved2], [100, 100])
    # compare_time_fp('branch2', [branch, branch_bound, bb_improved, bb_improved2], 20)
    
    get_plot('branch_tn.csv', 'temps de calcul en fonction de n', ylim=12, columns=['bb_improved','bb_improved2'])
    get_plot('branch_tp.csv', 'temps de calcul en fonction de p', columns=['bb_improved','bb_improved2'])
    get_plot('branch_base_tn.csv', 'temps de calcul en fonction de n', xlim=33, ylim=6, yscale='log')
    get_plot('branch_nodes.csv', 'nombre de noeuds en fonction de n', ylabel='nodes', ylim=10**6, yscale='log')
    

if __name__ == '__main__':
    main()