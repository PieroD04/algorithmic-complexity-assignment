import networkx as nx
import matplotlib.pyplot as plt
import csv
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
node_colors = [color_map[node_types[node]] for node in G.nodes]

# Dibujar el grafo
plt.figure(figsize=(10, 10))

# Usar un layout que acomode los nodos
pos = nx.spring_layout(G, k=0.15, iterations=20)   

# Dibujar los nodos y las aristas
nx.draw(G, pos, node_size=10, node_color=node_colors, edge_color='gray', with_labels=False)

# Añadir el título en coordenadas específicas
plt.text(0.00, 1.123, "Infraestructura de la red empresarial", fontsize=15, ha='center')

# Crear la leyenda para los colores
legend_handles = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]
plt.legend(handles=legend_handles, loc='upper right', title="Tipos de nodos")

# Mostrar el grafo
plt.show()