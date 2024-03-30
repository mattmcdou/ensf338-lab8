import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
edges_with_weights = [(1, 6, {'weight': 3}), (1, 7, {'weight': 2}), (2, 3, {'weight': 5}), 
                      (2, 4, {'weight': 1}), (4, 7, {'weight': 4}), (4, 9, {'weight': 7}), 
                      (5, 6, {'weight': 6}), (7, 8, {'weight': 3}), (4, 1, {'weight': 8})]

G.add_edges_from(edges_with_weights)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Original Graph")
plt.show()

def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def kruskal(graph):
    result = []
    parent = {}
    rank = {}
    
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    
    for node in graph.nodes():
        parent[node] = node
        rank[node] = 0
    
    for edge in edges:
        u, v, weight = edge
        u_parent = find(parent, u)
        v_parent = find(parent, v)
        
        if u_parent != v_parent:
            result.append((u, v, weight['weight']))
            union(parent, rank, u_parent, v_parent)
    
    return result

# Applying Kruskal's algorithm on the provided graph
mst_edges = kruskal(G)

# Drawing the graph with MST edges highlighted
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold')
nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Minimum Spanning Tree")
plt.show()
