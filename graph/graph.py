from pickle import load
from os.path import splitext, exists
import networkx
from sknetwork.ranking import Closeness
from numpy import argmax
from multiprocessing import Pool
from itertools import islice
from typing import Generator

def chunks(l: list, n: int) -> Generator:
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(islice(l_c, n))
        if not x:
            return
        yield x

def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), G.order() // node_divisor))
    num_chunks = len(node_chunks)
    bt_sc = p.starmap(
        networkx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks,
        ),
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c

def eigenvector(G):
    eigenvector = networkx.eigenvector_centrality(G)
    max_eigenvector = max(eigenvector, key=eigenvector.get)
    print(f'Самый центральный по собственному значению: {max_eigenvector}')
    
def closeness(G, graph):
    sparse = networkx.to_scipy_sparse_matrix(G)
    keys = tuple(graph.keys())
    closeness = Closeness(method = 'approximate', n_jobs = 8)
    max_closeness = argmax(closeness.fit_transform(sparse))
    print(f'Самый центральный по близости: {keys[max_closeness]}')
    
def betweenness(G):
    betweenness = betweenness_centrality_parallel(G, 4)
    max_betweenness = max(betweenness, key=betweenness.get)
    print(f'Самый центральный по посредничеству: {max_betweenness}')

if __name__ == '__main__':
    filename = input('Введите название файла с рёбрами графа: ')
    with open(filename, 'rb') as file:
        graph = load(file)

    G = networkx.Graph()
    for start, nodes in graph.items():
        for end in nodes:
            G.add_edge(start, end)

    leaves = [node for node, degree in G.degree() if degree < 2]
    G.remove_nodes_from(leaves)
    print(f'Удалено {len(leaves)} листьев')
    print(f'В графе {G.number_of_nodes()} узлов и {G.number_of_edges()} рёбер')

    eigenvector(G)
    closeness(G, graph)
    betweenness(G)
