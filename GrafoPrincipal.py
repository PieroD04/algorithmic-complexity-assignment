import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# Cargar los datos de nodos y aristas
df_nodos = pd.read_csv('Algoritmo Generador/nodos2.csv')
df_aristas = pd.read_csv('Algoritmo Generador/aristas2.csv')

# Crear un grafo vacío
G = nx.Graph()

# Añadir nodos al grafo con sus atributos
for _, row in df_nodos.iterrows():
    G.add_node(row['id'],
               nombre=row['nombre'],
               tipo=row['tipo'],
               ancho_banda=row['ancho_banda'],
               latencia=row['latencia'])

# Añadir aristas al grafo con sus atributos
for _, row in df_aristas.iterrows():
    G.add_edge(row['origen_id'], row['destino_id'], costo=row['costo'])

print(f"Grafo creado con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")

# Definir colores para cada tipo de nodo
color_map = {
    'router_empresa': 'red',     
    'switch_empresa': 'orange',    
    'router_cliente': 'yellow',  
    'switch_cliente': 'green',    
    'servidor': 'blue',           
    'firewall': 'black',            
    'punto_acceso': 'purple',       
    'estacion_trabajo': 'pink',     
    'laptop': 'teal',           # Color compartido
    'celular': 'teal',          # Color compartido
    'tablet': 'teal',           # Color compartido
    'computador_escritorio': 'teal'  # Color compartido
}

# Asignar colores a los nodos basados en su tipo
node_colors = [color_map.get(G.nodes[n]['tipo'], '#000000') for n in G.nodes()]

# Configurar el tamaño de la figura
plt.figure(figsize=(20, 20))

# Elegir un layout que maneje bien grafos grandes
# Nota: Este proceso puede ser lento para grafos muy grandes
print("Calculando el layout del grafo. Esto puede tardar unos minutos...")
pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)  # Ajusta 'k' según necesidad

print("Dibujando el grafo...")
# Dibujar los nodos
nx.draw_networkx_nodes(G, pos, node_size=50, node_color=node_colors, alpha=0.7)

# Dibujar las aristas
nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)

# Opcional: No dibujar etiquetas para mantener la claridad
# nx.draw_networkx_labels(G, pos, font_size=8)

# Crear leyenda personalizada
legend_elements = [mpatches.Patch(color=color, label=tipo.capitalize()) for tipo, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper right', fontsize='x-small')

plt.title("Infraestructura de Red Empresarial", fontsize=20)
plt.axis('off')  # Ocultar los ejes
plt.show()
plt.savefig("grafo_principal.png")