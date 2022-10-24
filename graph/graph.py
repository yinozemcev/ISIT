import pickle
import networkx
import matplotlib.pyplot as plt

filename = input('Введите название файла с рёбрами графа: ')
with open(filename, 'rb') as file:
    edges = pickle.load(file)

G = networkx.Graph()
G.add_edges_from(edges)
networkx.write_gexf(G, filename[:-7] + '.gexf')

betweenness = networkx.betweenness_centrality(G)
closeness = networkx.closeness_centrality(G)
eigenvector = networkx.eigenvector_centrality(G)

max_betweenness = max(betweenness, key=betweenness.get)
max_closeness = max(closeness, key=closeness.get)
max_eigenvector = max(eigenvector, key=eigenvector.get)
print(f'Самый центральный по посредничеству: {max_betweenness}')
print(f'Самый центральный по близости: {max_closeness}')
print(f'Самый центральный по собственному значению: {max_eigenvector}')

