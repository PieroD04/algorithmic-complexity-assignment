import pandas as pd
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import time

def create_graph(df, selected_area):
    matplotlib.use('Agg')
    G = nx.Graph()

    area_colors = {
        'Área Académica': 'blue',
        'Administración': 'green',
        'Residencias Estudiantiles': 'yellow',
        'Biblioteca': 'purple',
        'Cafetería': 'red',
        'Externa': 'gray'
    }

    if selected_area != 'Todos': 
        filtered_df = df[(df['Source.Area'] == selected_area) | (df['Destination.Area'] == selected_area)]
    else:
        filtered_df = df

    for _, row in filtered_df.iterrows():
        src = row['Source.IP']
        dest = row['Destination.IP']
        weight = row['Flow.Bytes.s']
        src_area = row['Source.Area']
        dest_area = row['Destination.Area']

        if pd.notna(weight) and isinstance(weight, (int, float)):
            G.add_node(src, area=src_area, color=area_colors.get(src_area, 'black'))
            G.add_node(dest, area=dest_area, color=area_colors.get(dest_area, 'black'))
            G.add_edge(src, dest, weight=weight)

    print("Grafo original")
    print(G)

    start_time = time.time()
    node_colors = [data['color'] for _, data in G.nodes(data=True)]
    pos = nx.spring_layout(G, k=0.3)

    plt.figure(figsize=(12, 10))
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

    plt.savefig('static/images/graph.png', dpi=1000)
    plt.close()

    drawing_time = time.time() - start_time
    return G.number_of_edges(), drawing_time, 'static/images/graph.png'