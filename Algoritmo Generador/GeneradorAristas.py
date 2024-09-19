import numpy as np
import time
import pandas as pd

# Supongamos que df_nodos es un DataFrame con los nodos
df_nodos = pd.read_csv('nodos.csv')

num_nodos = len(df_nodos)

# Parámetros para la generación de conexiones
max_aristas = 3000  # Limitar el número máximo de conexiones

# Crear un conjunto para almacenar conexiones ya vistas
conexiones_vistas = set()

# Listas para almacenar los datos de las aristas
origen_ids = []
destino_ids = []
costos = []

# Garantizar que al menos un nodo tenga al menos una conexión
nodo_conectado = np.random.randint(1, num_nodos + 1)

# Generar al menos una conexión para el nodo garantizado
while len(conexiones_vistas) < max_aristas:
    origen_id = np.random.randint(1, num_nodos + 1)
    destino_id = np.random.randint(1, num_nodos + 1)
    costo = np.random.randint(1, 101)

    # Asegurarse de que no se conecte un nodo consigo mismo y que la conexión no se repita
    if origen_id != destino_id and (origen_id, destino_id) not in conexiones_vistas:
        origen_ids.append(origen_id)
        destino_ids.append(destino_id)
        costos.append(costo)
        conexiones_vistas.add((origen_id, destino_id))

        # Introducir un breve tiempo de espera
        time.sleep(0.01)

# Crear un DataFrame con las conexiones generadas
df_conexiones = pd.DataFrame({
    'origen_id': origen_ids,
    'destino_id': destino_ids,
    'costo': costos
})

# Guardar el DataFrame en un archivo CSV
print("Guardando aristas en 'aristas.csv'")
df_conexiones.to_csv('aristas.csv', index=False)