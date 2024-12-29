import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import time

class GraphWithKruskal:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []  # Aquí almacenaremos el MST
        i, e, tot_weight = 0, 0, 0

        # Ordenar los bordes por peso
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # Crear subconjuntos independientes para cada vértice
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Número de aristas en el MST será igual a V-1
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # Si no forman un ciclo, incluirlos en el MST
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        return result

def kruskal(df, selected_area='Todos'):
    matplotlib.use('Agg')
    
    if selected_area != 'Todos':
        filtered_df = df[(df['Source.Area'] == selected_area) | (df['Destination.Area'] == selected_area)]
    else:
        filtered_df = df

    nodes = pd.concat([filtered_df['Source.IP'], filtered_df['Destination.IP']]).unique()
    g = GraphWithKruskal(len(nodes))
    
    node_map = {node: idx for idx, node in enumerate(nodes)}

    for _, row in filtered_df.iterrows():
        u = node_map[row['Source.IP']]
        v = node_map[row['Destination.IP']]
        w = row['Flow.Bytes.s']
        g.add_edge(u, v, w)

    start_time = time.time()
    mst_result = g.kruskal()
    algorithm_time = time.time() - start_time

    G = nx.Graph()

    for u, v, weight in mst_result:
        G.add_edge(nodes[u], nodes[v], weight=weight)

    print("Grafo con Kruskal")
    print(G)

    area_colors = {
        'Área Académica': 'blue',
        'Administración': 'green',
        'Residencias Estudiantiles': 'yellow',
        'Biblioteca': 'purple',
        'Cafetería': 'red',
        'Externa': 'gray'
    }

    for node in G.nodes():
        area = df[df['Source.IP'] == node]['Source.Area'].values[0]
        G.nodes[node]['color'] = area_colors.get(area, 'black')

    start_time = time.time()

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, k=0.3)
    node_colors = [data['color'] for _, data in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='orange', alpha=0.5)

    for area, color in area_colors.items():
        plt.scatter([], [], color=color, label=area)

    plt.legend(
        loc='upper right',
        fontsize=8,
        markerscale=1.5,
        borderpad=0.5,
        labelspacing=0.5,
        handlelength=1.2
    )
    plt.tight_layout(pad=2.0)

    plt.savefig('static/images/kruskal.png')
    plt.close()

    drawing_time = time.time() - start_time

    return G.number_of_edges(), algorithm_time, drawing_time, 'static/images/kruskal.png'