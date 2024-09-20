import pandas as pd
import numpy as np

# Número total de nodos
num_total_nodos = 1500

# Definir la cantidad de cada tipo de dispositivo de la empresa
num_routers = 5
num_switches = 50
num_servidores = 20
num_firewalls = 10
num_puntos_acceso = 30
num_estaciones_trabajo = 100

# Definir tipos de dispositivos de clientes y sus cantidades
num_laptops = 700
num_celulares = 450
num_tablets = 120
num_computadores = 15  # Total: 700 + 450 + 120 + 15 = 1285

# Verificar que la suma no exceda el número total de nodos
assert (num_routers + num_switches + num_servidores + num_firewalls +
        num_puntos_acceso + num_estaciones_trabajo +
        num_laptops + num_celulares + num_tablets + num_computadores) <= num_total_nodos, "La suma de tipos de nodos excede el número total de nodos."

# Calcular el número restante de nodos si es necesario
num_restantes = num_total_nodos - (
    num_routers + num_switches + num_servidores + num_firewalls +
    num_puntos_acceso + num_estaciones_trabajo +
    num_laptops + num_celulares + num_tablets + num_computadores
)

if num_restantes > 0:
    num_computadores += num_restantes  # Añadir al último tipo

# Crear listas para los tipos de nodos
tipos_empresa = (
    ["router"] * num_routers +
    ["switch"] * num_switches +
    ["servidor"] * num_servidores +
    ["firewall"] * num_firewalls +
    ["punto_acceso"] * num_puntos_acceso +
    ["estacion_trabajo"] * num_estaciones_trabajo
)

tipos_clientes = (
    ["laptop"] * num_laptops +
    ["celular"] * num_celulares +
    ["tablet"] * num_tablets +
    ["computador_escritorio"] * num_computadores
)

# Combinar tipos
tipos = tipos_empresa + tipos_clientes

# Verificar que la suma sea correcta
assert len(tipos) == num_total_nodos, "La suma de tipos de nodos no coincide con el número total de nodos."

# Generar IDs de nodos
ids = np.arange(1, num_total_nodos + 1)

# Generar nombres de nodos de acuerdo al tipo
contador_tipos = {}
nombres = []
for tipo in tipos:
    if tipo not in contador_tipos:
        contador_tipos[tipo] = 1
    else:
        contador_tipos[tipo] += 1
    nombre = f"{tipo.capitalize()}{contador_tipos[tipo]}"
    nombres.append(nombre)

# Generar ancho de banda disponible (entre 10 Mbps y 1000 Mbps)
# Los dispositivos de la empresa tienen mayor ancho de banda
ancho_banda = []
for tipo in tipos:
    if tipo in ["router", "switch", "firewall", "servidor"]:
        ancho_banda.append(np.random.randint(100, 1001))  # 100 Mbps a 1000 Mbps
    elif tipo == "punto_acceso":
        ancho_banda.append(np.random.randint(50, 501))    # 50 Mbps a 500 Mbps
    elif tipo in ["estacion_trabajo", "laptop", "celular", "tablet", "computador_escritorio"]:
        ancho_banda.append(np.random.randint(10, 101))    # 10 Mbps a 100 Mbps
    else:
        ancho_banda.append(np.random.randint(10, 101))    # Por defecto

# Generar latencia (entre 1 ms y 50 ms)
latencia = np.random.randint(1, 51, size=num_total_nodos)

# Crear el DataFrame de nodos
df_nodos = pd.DataFrame({
    "id": ids,
    "nombre": nombres,
    "tipo": tipos,
    "ancho_banda": ancho_banda,
    "latencia": latencia
})

# Guardar el DataFrame en un archivo CSV
df_nodos.to_csv("nodos2.csv", index=False)
print("Archivo nodos.csv generado con éxito.")