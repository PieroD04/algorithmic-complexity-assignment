import pandas as pd
import numpy as np

# Número de nodos a generar
num_nodos = 1500

# Lista de tipos de nodos predeterminados
tipos_predeterminados = ["router", "switch", "computadora", "laptop", "servidor"]

# Generar IDs de nodos
ids = np.arange(1, num_nodos + 1)

# Generar tipos de nodos (router, switch, computadora, laptop, servidor) de manera aleatoria
tipos = np.random.choice(tipos_predeterminados, size=num_nodos)

# Generar nombres de nodos de acuerdo al tipo
nombres = []
for tipo in tipos:
    # Contar cuántos nodos de este tipo ya han sido generados
    count_tipo = (tipos == tipo).sum()
    nombre = f"{tipo}{(count_tipo - 1) // tipos_predeterminados.count(tipo) + 1}"
    nombres.append(nombre)

# Generar ancho de banda disponible (entre 10 Mbps y 1000 Mbps)
ancho_banda = np.random.randint(10, 1001, size=num_nodos)

# Generar latencia (entre 1 ms y 50 ms)
latencia = np.random.randint(1, 51, size=num_nodos)

# Crear el DataFrame de nodos
df_nodos = pd.DataFrame({
    "id": ids,
    "nombre": nombres,
    "tipo": tipos,
    "ancho_banda": ancho_banda,
    "latencia": latencia
})

# Guardar el DataFrame en un archivo CSV
df_nodos.to_csv("nodos.csv", index=False)
print("Archivo nodos.csv generado con éxito.")