from pickle import load
from os.path import splitext, exists
import networkx

filename = input('Введите название файла с рёбрами графа: ')
with open(filename, 'rb') as file:
    graph = load(file)

G = networkx.Graph()
for start, nodes in graph.items():
    for end in nodes:
        G.add_edge(start, end)

gexf_name = splitext(filename)[0] + '.gexf'
if not exists(gexf_name):
    networkx.write_gexf(G, gexf_name)

eigenvector = networkx.eigenvector_centrality(G)
max_eigenvector = max(eigenvector, key=eigenvector.get)
print(f'Самый центральный по собственному значению: {max_eigenvector}')

closeness = networkx.closeness_centrality(G)
max_closeness = max(closeness, key=closeness.get)
print(f'Самый центральный по близости: {max_closeness}')

betweenness = networkx.betweenness_centrality(G)
max_betweenness = max(betweenness, key=betweenness.get)
print(f'Самый центральный по посредничеству: {max_betweenness}')



