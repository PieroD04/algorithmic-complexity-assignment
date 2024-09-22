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

# Seleccionar un router_empresa aleatorio
routers_empresa = [node for node in G.nodes if node_types[node] == 'router_empresa']
router_empresa = random.choice(routers_empresa)

# Seleccionar un router_cliente adyacente
adyacent_clients = [n for n in G.neighbors(router_empresa) if node_types[n] == 'router_cliente']
if adyacent_clients:
    router_cliente = random.choice(adyacent_clients)
else:
    raise Exception("No hay router_cliente adyacente al router_empresa.")

# Elegir el número de switches a obtener
num_switches = 3  # Cambia este valor según lo que necesites

# Seleccionar switches_empresa adyacentes al router_empresa
adyacent_switch_empresa = [n for n in G.neighbors(router_empresa) if node_types[n] == 'switch_empresa']
switch_empresa_list = random.sample(adyacent_switch_empresa, min(num_switches, len(adyacent_switch_empresa))) if adyacent_switch_empresa else []
if not switch_empresa_list:
    raise Exception("No hay suficientes switch_empresa adyacentes al router_empresa.")

# Seleccionar switches_cliente adyacentes al router_cliente
adyacent_switch_cliente = [n for n in G.neighbors(router_cliente) if node_types[n] == 'switch_cliente']
switch_cliente_list = random.sample(adyacent_switch_cliente, min(num_switches, len(adyacent_switch_cliente))) if adyacent_switch_cliente else []
if not switch_cliente_list:
    raise Exception("No hay suficientes switch_cliente adyacentes al router_cliente.")

# Crear el subgrafo comenzando desde router_empresa y router_cliente
subgrafo_nodes = {router_empresa, router_cliente}
subgrafo_nodes.update(switch_empresa_list)
subgrafo_nodes.update(switch_cliente_list)

# Obtener nodos adicionales de tipo específico
tipos_adicionales = ['estacion_trabajo', 'laptop', 'celular', 'tablet', 'computador_escritorio']
for switch in switch_empresa_list + switch_cliente_list:
    for tipo in tipos_adicionales:
        adicionales = [n for n in G.neighbors(switch) if node_types[n] == tipo]
        subgrafo_nodes.update(adicionales)

# Limitar a 50 nodos si hay más
if len(subgrafo_nodes) > 50:
    subgrafo_nodes = set(random.sample(subgrafo_nodes, 50))

# Crear el subgrafo final
subgrafo = G.subgraph(subgrafo_nodes)

# Asignar colores a los tipos de nodos
color_map = {
    'router_empresa': 'red',     
    'switch_empresa': 'orange',    
    'router_cliente': 'yellow',  
    'switch_cliente': 'green',    
    'servidor': 'blue',           
    'firewall': 'black',            
    'punto_acceso': 'purple',       
    'estacion_trabajo': 'pink',     
    'laptop': 'teal',           
    'celular': 'teal',          
    'tablet': 'teal',           
    'computador_escritorio': 'teal'  
}

# Crear una lista de colores para los nodos
node_colors = [color_map[node_types[node]] for node in subgrafo.nodes]

# Dibujar el subgrafo
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(subgrafo, k=0.5, iterations=100)
nx.draw(subgrafo, pos, node_size=300, node_color=node_colors, edge_color='gray', with_labels=True, font_size=8, font_color='black')

# Añadir el título
plt.title('Grafo Muestral', fontsize=15)

# Crear la leyenda para los colores
legend_handles = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]
plt.legend(handles=legend_handles, loc='upper right', title="Tipos de nodos")

# Mostrar el subgrafo
plt.savefig("grafo_muestral.png")
plt.show()