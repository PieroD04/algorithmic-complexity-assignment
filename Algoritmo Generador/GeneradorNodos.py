import pandas as pd
import numpy as np

# Número total de nodos
num_total_nodos = 1600

# Definir la cantidad de cada tipo de dispositivo de la empresa
num_router_empresa = 10
num_switch_empresa = 55
num_servidores = 15
num_firewalls = 5
num_estaciones_trabajo = 100

# Definir tipos de dispositivos de clientes
num_router_cliente = 13
num_switch_cliente_por_router = 5  # 5 switches por router cliente
num_switch_cliente = num_router_cliente * num_switch_cliente_por_router  # Total switches de cliente
num_puntos_acceso = 30  # Solo para clientes

# Definir tipos de dispositivos finales de clientes
num_laptops = 700
num_celulares = 450
num_tablets = 100
num_computadores = 57  # Ajustado para mantener el total de nodos

# Verificar que la suma no exceda el número total de nodos
assert (num_router_empresa + num_switch_empresa + num_servidores + num_firewalls +
        num_estaciones_trabajo + num_router_cliente + num_switch_cliente +
        num_puntos_acceso + num_laptops + num_celulares + num_tablets + num_computadores) == num_total_nodos, "La suma de tipos de nodos no coincide con el número total de nodos."

# Crear listas para los tipos de nodos de la empresa
tipos_empresa = (
    ["router_empresa"] * num_router_empresa +
    ["switch_empresa"] * num_switch_empresa +
    ["servidor"] * num_servidores +
    ["firewall"] * num_firewalls +
    ["estacion_trabajo"] * num_estaciones_trabajo
)

# Crear routers y switches de clientes
tipos_cliente = []
nombres_cliente = []

for i in range(1, num_router_cliente + 1):
    # Añadir un router de cliente
    tipos_cliente.append("router_cliente")
    nombre_router = f"RouterCliente{i}"
    nombres_cliente.append(nombre_router)
    
    # Añadir 5 switches de cliente por router
    for j in range(1, num_switch_cliente_por_router + 1):
        tipos_cliente.append("switch_cliente")
        nombre_switch = f"SwitchCliente{i}_{j}"
        nombres_cliente.append(nombre_switch)

# Agregar puntos de acceso para clientes
tipos_cliente += ["punto_acceso"] * num_puntos_acceso
nombres_cliente += [f"PuntoAcceso{i+1}" for i in range(num_puntos_acceso)]

# Crear listas para los dispositivos finales de clientes
tipos_dispositivos_finales = (
    ["laptop"] * num_laptops +
    ["celular"] * num_celulares +
    ["tablet"] * num_tablets +
    ["computador_escritorio"] * num_computadores
)

# Combinar todos los tipos
tipos = tipos_empresa + tipos_cliente + tipos_dispositivos_finales

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
    if tipo in ["router_empresa", "router_cliente", "switch_empresa", "switch_cliente", "firewall", "servidor"]:
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
print("Archivo nodos2.csv generado con éxito.")
