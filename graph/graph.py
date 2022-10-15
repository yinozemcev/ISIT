import json
import networkx

with open('result.txt') as file:
    edges = json.loads(file.read())

G = networkx.Graph()
G.add_edges_from(edges)
networkx.write_gexf(G, 'result.gexf')

posrednichestvo = networkx.betweenness_centrality(G)
blizost = networkx.closeness_centrality(G)
sobstvenniy = networkx.eigenvector_centrality(G)

user_id = int(input('Введите ID пользователя для которого нужна центральность: '))
print(f'Центральность по посредничеству: {posrednichestvo[user_id]}')
print(f'Центральность по близости: {blizost[user_id]}')
print(f'Центральность по собственному значению: {sobstvenniy[user_id]}')

