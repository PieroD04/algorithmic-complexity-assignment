import networkx as nx
import matplotlib.pyplot as plt
import csv
import random
import matplotlib.patches as mpatches

# Crear un grafo vacío
G = nx.Graph()

# Diccionario para almacenar el tipo de cada nodo
node_types = {}

# Leer nodos desde nodos2.csv
with open('Algoritmo Generador/nodos2.csv', newline='') as csvfile:
    nodos_reader = csv.reader(csvfile)
    next(nodos_reader)  # Saltar la fila de encabezado
    for row in nodos_reader:
        node_id = int(row[0])
        node_type = row[2]
        G.add_node(node_id)
        node_types[node_id] = node_type

# Leer aristas desde aristas2.csv
with open('Algoritmo Generador/aristas2.csv', newline='') as csvfile:
    aristas_reader = csv.reader(csvfile)
    next(aristas_reader)  # Saltar la fila de encabezado
    for row in aristas_reader:
        n1, n2 = int(row[0]), int(row[1])
        if n1 != n2:  # Evitar loops
            G.add_edge(n1, n2)

# Seleccionar aleatoriamente 50 aristas y asegurarse de que el grafo sea conexo
edges = list(G.edges)
selected_edges = []
if len(edges) > 50:
    selected_edges = random.sample(edges, 50)
    G_muestral = nx.Graph()
    G_muestral.add_edges_from(selected_edges)

    # Asegurarse de que el grafo sea conexo
    if not nx.is_connected(G_muestral):
        # Conectar componentes desconectados
        components = list(nx.connected_components(G_muestral))
        while len(components) > 1:
            comp1 = components.pop()
            comp2 = components.pop()
            node1 = random.choice(list(comp1))
            node2 = random.choice(list(comp2))
            G_muestral.add_edge(node1, node2)
            selected_edges.append((node1, node2))
            components = list(nx.connected_components(G_muestral))
else:
    G_muestral = G
    selected_edges = edges

# Guardar las aristas seleccionadas en un archivo CSV
with open('aristas_muestral.csv', 'w', newline='') as csvfile:
    aristas_writer = csv.writer(csvfile)
    aristas_writer.writerow(['Nodo1', 'Nodo2'])
    for edge in selected_edges:
        aristas_writer.writerow(edge)

# Asignar colores a los tipos de nodos
color_map = {
    'switch': 'blue',
    'laptop': 'green',
    'router': 'red',
    'computador_escritorio': 'purple',
    'servidor': 'orange',
    'firewall': 'yellow',
    'punto_acceso': 'cyan',
    'estacion_trabajo': 'magenta',
    'celular': 'brown',
    'tablet': 'pink'
}

# Crear una lista de colores para los nodos
node_colors = [color_map[node_types[node]] for node in G_muestral.nodes]

# Dibujar el grafo
plt.figure(figsize=(12, 12))

# Usar un layout que acomode los nodos y los separe más
pos = nx.spring_layout(G_muestral, k=0.5, iterations=100)

# Dibujar los nodos y las aristas
nx.draw(G_muestral, pos, node_size=300, node_color=node_colors, edge_color='gray', with_labels=True, font_size=8, font_color='black')

# Añadir el título en coordenadas específicas
plt.text(0.00, 1.123, "Grafo Muestral de la red empresarial", fontsize=15, ha='center')

# Crear la leyenda para los colores
legend_handles = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]
plt.legend(handles=legend_handles, loc='upper right', title="Tipos de nodos")

# Mostrar el grafo
plt.savefig("grafo_muestral.png")