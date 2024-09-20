import numpy as np
import pandas as pd
import time

# Cargar el DataFrame de nodos
df_nodos = pd.read_csv('nodos2.csv')

# Crear diccionarios para facilitar la búsqueda de tipos y atributos
id_tipo = dict(zip(df_nodos['id'], df_nodos['tipo']))
id_latencia = dict(zip(df_nodos['id'], df_nodos['latencia']))
id_ancho_banda = dict(zip(df_nodos['id'], df_nodos['ancho_banda']))

# Separar IDs por tipo
routers = df_nodos[df_nodos['tipo'] == 'router']['id'].tolist()
switches = df_nodos[df_nodos['tipo'] == 'switch']['id'].tolist()
firewalls = df_nodos[df_nodos['tipo'] == 'firewall']['id'].tolist()
servidores = df_nodos[df_nodos['tipo'] == 'servidor']['id'].tolist()
puntos_acceso = df_nodos[df_nodos['tipo'] == 'punto_acceso']['id'].tolist()
estaciones_trabajo = df_nodos[df_nodos['tipo'] == 'estacion_trabajo']['id'].tolist()
laptops = df_nodos[df_nodos['tipo'] == 'laptop']['id'].tolist()
celulares = df_nodos[df_nodos['tipo'] == 'celular']['id'].tolist()
tablets = df_nodos[df_nodos['tipo'] == 'tablet']['id'].tolist()
computador_escritorio = df_nodos[df_nodos['tipo'] == 'computador_escritorio']['id'].tolist()

# Agrupar dispositivos de clientes
dispositivos_clientes = laptops + celulares + tablets + computador_escritorio

# Parámetros para la generación de conexiones
max_aristas = 5000  # Ajustar según necesidad
conexiones_vistas = set()

origen_ids = []
destino_ids = []
costos = []

# Constantes para la fórmula de costo
ALPHA = 1
BETA = 1000

# Función para calcular el costo basado en latencia y ancho de banda
def calcular_costo(origen, destino):
    latencia_origen = id_latencia.get(origen, 1)
    latencia_destino = id_latencia.get(destino, 1)
    ancho_banda_origen = id_ancho_banda.get(origen, 10)
    ancho_banda_destino = id_ancho_banda.get(destino, 10)
    
    latencia_total = latencia_origen + latencia_destino
    ancho_banda_min = min(ancho_banda_origen, ancho_banda_destino)
    
    # Evitar división por cero
    if ancho_banda_min == 0:
        ancho_banda_min = 1
    
    costo = ALPHA * latencia_total + BETA / ancho_banda_min
    
    # Normalizar el costo a un rango de 1 a 100
    # Supongamos que el costo máximo esperado es aproximadamente 100
    # Ajusta los factores ALPHA y BETA si es necesario
    costo_normalizado = min(int(costo), 100)
    
    return costo_normalizado

# Función para añadir conexión si es válida
def añadir_conexion(origen, destino):
    if origen != destino and (origen, destino) not in conexiones_vistas and (destino, origen) not in conexiones_vistas:
        costo = calcular_costo(origen, destino)
        origen_ids.append(origen)
        destino_ids.append(destino)
        costos.append(costo)  
        conexiones_vistas.add((origen, destino))
        return True
    return False

# 1. Conectar dispositivos de clientes a switches o puntos de acceso
for cliente in dispositivos_clientes:
    # Definir tipo de cliente para decidir la conexión
    tipo_cliente = id_tipo.get(cliente, 'otro_cliente')
    if tipo_cliente in ["celular", "tablet", "computador_escritorio"]:
        # Probabilidad de conexión a puntos de acceso
        if np.random.rand() < 0.7 and len(puntos_acceso) > 0:
            num_conexiones = np.random.choice([1, 2], p=[0.9, 0.1])
            puntos_conectados = np.random.choice(puntos_acceso, size=min(num_conexiones, len(puntos_acceso)), replace=False)
            for pa in puntos_conectados:
                if len(conexiones_vistas) >= max_aristas:
                    break
                añadir_conexion(cliente, pa)
        else:
            # Conectar a switches
            num_conexiones = np.random.choice([1, 2], p=[0.95, 0.05])
            switches_conectados = np.random.choice(switches, size=min(num_conexiones, len(switches)), replace=False)
            for switch in switches_conectados:
                if len(conexiones_vistas) >= max_aristas:
                    break
                añadir_conexion(cliente, switch)
    else:
        # Laptops y otros se conectan principalmente a switches
        num_conexiones = np.random.choice([1, 2], p=[0.95, 0.05])
        switches_conectados = np.random.choice(switches, size=min(num_conexiones, len(switches)), replace=False)
        for switch in switches_conectados:
            if len(conexiones_vistas) >= max_aristas:
                break
            añadir_conexion(cliente, switch)
    if len(conexiones_vistas) >= max_aristas:
        break

# 2. Conectar switches a routers, firewalls, servidores y otros switches
for switch in switches:
    # Cada switch se conecta a al menos dos routers/firewalls/servidores
    posibles_destinos = routers + firewalls + servidores + switches
    posibles_destinos = [dest for dest in posibles_destinos if dest != switch]
    num_conexiones = np.random.randint(2, 5)  # Cada switch se conecta a 2-4 dispositivos de nivel superior
    destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
    for dest in destinos:
        if len(conexiones_vistas) >= max_aristas:
            break
        añadir_conexion(switch, dest)
    if len(conexiones_vistas) >= max_aristas:
        break

# 3. Conectar routers entre sí (opcional para redundancia)
for router in routers:
    posibles_destinos = [r for r in routers if r != router]
    if len(posibles_destinos) > 0:
        num_conexiones = np.random.randint(1, 3)  # Cada router se conecta a 1-2 otros routers
        destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
        for dest in destinos:
            if len(conexiones_vistas) >= max_aristas:
                break
            añadir_conexion(router, dest)
    if len(conexiones_vistas) >= max_aristas:
        break

# 4. Conectar firewalls a routers o switches
for firewall in firewalls:
    posibles_destinos = routers + switches
    if len(posibles_destinos) > 0:
        num_conexiones = np.random.randint(1, 3)
        destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
        for dest in destinos:
            if len(conexiones_vistas) >= max_aristas:
                break
            añadir_conexion(firewall, dest)
    if len(conexiones_vistas) >= max_aristas:
        break

# 5. Conectar servidores a switches
for servidor in servidores:
    posibles_destinos = switches
    if len(posibles_destinos) > 0:
        num_conexiones = np.random.randint(1, 3)
        destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
        for dest in destinos:
            if len(conexiones_vistas) >= max_aristas:
                break
            añadir_conexion(servidor, dest)
    if len(conexiones_vistas) >= max_aristas:
        break

# 6. Conectar puntos de acceso a switches
for pa in puntos_acceso:
    posibles_destinos = switches
    if len(posibles_destinos) > 0:
        num_conexiones = np.random.randint(1, 3)
        destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
        for dest in destinos:
            if len(conexiones_vistas) >= max_aristas:
                break
            añadir_conexion(pa, dest)
    if len(conexiones_vistas) >= max_aristas:
        break

# 7. Conectar estaciones de trabajo a switches
for est_trabajo in estaciones_trabajo:
    num_conexiones = np.random.choice([1, 2], p=[0.95, 0.05])
    switches_conectados = np.random.choice(switches, size=min(num_conexiones, len(switches)), replace=False)
    for switch in switches_conectados:
        if len(conexiones_vistas) >= max_aristas:
            break
        añadir_conexion(est_trabajo, switch)
    if len(conexiones_vistas) >= max_aristas:
        break

# 8. Rellenar conexiones hasta alcanzar max_aristas de forma aleatoria respetando reglas
while len(conexiones_vistas) < max_aristas:
    origen_id = np.random.choice(switches + routers + firewalls + servidores + puntos_acceso)
    destino_id = np.random.choice(switches + routers + firewalls + servidores + puntos_acceso)
    
    # Evitar conexiones con dispositivos de clientes
    if id_tipo.get(origen_id) in ["laptop", "celular", "tablet", "computador_escritorio"]:
        continue
    if id_tipo.get(destino_id) in ["laptop", "celular", "tablet", "computador_escritorio"]:
        continue
    
    # Evitar conexiones no permitidas
    tipo_origen = id_tipo.get(origen_id)
    tipo_destino = id_tipo.get(destino_id)
    
    conexiones_validas = False
    if tipo_origen == 'switch' and tipo_destino in ["router", "firewall", "servidor", "switch", "punto_acceso"]:
        conexiones_validas = True
    elif tipo_origen == 'router' and tipo_destino in ["router", "switch", "firewall"]:
        conexiones_validas = True
    elif tipo_origen == 'firewall' and tipo_destino in ["router", "switch"]:
        conexiones_validas = True
    elif tipo_origen == 'servidor' and tipo_destino in ["switch"]:
        conexiones_validas = True
    elif tipo_origen == 'punto_acceso' and tipo_destino in ["switch"]:
        conexiones_validas = True
    
    if conexiones_validas:
        añadido = añadir_conexion(origen_id, destino_id)
        if añadido:
            continue
    # Si no es válido o ya existe, intentar otra conexión
    continue

# Crear el DataFrame con las conexiones generadas
df_conexiones = pd.DataFrame({
    'origen_id': origen_ids,
    'destino_id': destino_ids,
    'costo': costos
})

# Guardar el DataFrame en un archivo CSV
df_conexiones.to_csv('aristas2.csv', index=False)
print("Archivo aristas2.csv generado con éxito.")
