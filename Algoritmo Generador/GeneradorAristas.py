import pandas as pd
import numpy as np

# Cargar el DataFrame de nodos
df_nodos = pd.read_csv('nodos2.csv')

# Crear diccionarios para facilitar la búsqueda de tipos y atributos
id_tipo = dict(zip(df_nodos['id'], df_nodos['tipo']))
id_latencia = dict(zip(df_nodos['id'], df_nodos['latencia']))
id_ancho_banda = dict(zip(df_nodos['id'], df_nodos['ancho_banda']))

# Separar IDs por tipo
routers_empresa = df_nodos[df_nodos['tipo'] == 'router_empresa']['id'].tolist()
switches_empresa = df_nodos[df_nodos['tipo'] == 'switch_empresa']['id'].tolist()
firewalls = df_nodos[df_nodos['tipo'] == 'firewall']['id'].tolist()
servidores = df_nodos[df_nodos['tipo'] == 'servidor']['id'].tolist()
estaciones_trabajo = df_nodos[df_nodos['tipo'] == 'estacion_trabajo']['id'].tolist()

routers_cliente = df_nodos[df_nodos['tipo'] == 'router_cliente']['id'].tolist()
switches_cliente = df_nodos[df_nodos['tipo'] == 'switch_cliente']['id'].tolist()
puntos_acceso = df_nodos[df_nodos['tipo'] == 'punto_acceso']['id'].tolist()

laptops = df_nodos[df_nodos['tipo'] == 'laptop']['id'].tolist()
celulares = df_nodos[df_nodos['tipo'] == 'celular']['id'].tolist()
tablets = df_nodos[df_nodos['tipo'] == 'tablet']['id'].tolist()
computadores_escritorio = df_nodos[df_nodos['tipo'] == 'computador_escritorio']['id'].tolist()

# Agrupar dispositivos de clientes y trabajadores
dispositivos_clientes = {
    'laptop': laptops,
    'celular': celulares,
    'tablet': tablets,
    'computador_escritorio': computadores_escritorio
}

dispositivos_trabajadores = estaciones_trabajo  # Solo se conectan a switches_empresa

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

# 1. Conectar cada switch_empresa a exactamente un router_empresa
print("Conectando switches_empresa a routers_empresa...")
for switch in switches_empresa:
    if len(conexiones_vistas) >= max_aristas:
        break
    router = np.random.choice(routers_empresa)
    añadido = añadir_conexion(switch, router)
    if not añadido:
        print(f"No se pudo conectar el switch_empresa {switch} al router_empresa {router}.")

# 2. Conectar cada punto de acceso a exactamente un switch_cliente
print("Conectando puntos_acceso a switches_empresa...")
for pa in puntos_acceso:
    if len(conexiones_vistas) >= max_aristas:
        break
    switch = np.random.choice(switches_cliente)
    añadido = añadir_conexion(pa, switch)
    if not añadido:
        print(f"No se pudo conectar el punto_acceso {pa} al switch_empresa {switch}.")

# 3. Conectar cada router_cliente a sus 5 switches_cliente
print("Conectando routers_cliente a sus switches_cliente...")
router_cliente_switch_map = {}
switch_idx = 0
for router in routers_cliente:
    switches_asociados = switches_cliente[switch_idx:switch_idx + 5]
    router_cliente_switch_map[router] = switches_asociados
    switch_idx += 5
    for switch in switches_asociados:
        if len(conexiones_vistas) >= max_aristas:
            break
        añadido = añadir_conexion(router, switch)
        if not añadido:
            print(f"No se pudo conectar el router_cliente {router} al switch_cliente {switch}.")

# 3.1. Conectar routers_empresa a routers_cliente
print("Conectando routers_empresa a routers_cliente...")
for router_empresa in routers_empresa:
    if len(conexiones_vistas) >= max_aristas:
        break
    router_cliente = np.random.choice(routers_cliente)
    añadido = añadir_conexion(router_empresa, router_cliente)
    if not añadido:
        print(f"No se pudo conectar el router_empresa {router_empresa} al router_cliente {router_cliente}.")

# 4. Conectar dispositivos_trabajadores (estaciones_trabajo) a switches_empresa
print("Conectando estaciones_trabajo a switches_empresa...")
for est_trabajo in dispositivos_trabajadores:
    if len(conexiones_vistas) >= max_aristas:
        break
    switch = np.random.choice(switches_empresa)
    añadido = añadir_conexion(est_trabajo, switch)
    if not añadido:
        print(f"No se pudo conectar la estacion_trabajo {est_trabajo} al switch_empresa {switch}.")

# 5. Conectar celulares y tablets exclusivamente a puntos_acceso
print("Conectando laptops y celulares exclusivamente a puntos_acceso...")
for tipo in ['tablet', 'celular']:
    while dispositivos_clientes[tipo] and len(conexiones_vistas) < max_aristas:
        pa = np.random.choice(puntos_acceso)
        dispositivo = dispositivos_clientes[tipo].pop()
        añadido = añadir_conexion(pa, dispositivo)
        if not añadido:
            print(f"No se pudo conectar el dispositivo {dispositivo} al punto_acceso {pa}.")

# 6. Conectar computadores_escritorio a switches_cliente o puntos_acceso
print("Conectando computadores_escritorio o laptops a switches_cliente o puntos_acceso...")
for comput in computadores_escritorio.copy():  # Usar copy para evitar modificar la lista durante la iteración
    if len(conexiones_vistas) >= max_aristas:
        break
    # Decidir aleatoriamente si conectar a switch_cliente o punto_acceso
    if np.random.rand() < 0.5 and switches_cliente:
        switch = np.random.choice(switches_cliente)
        añadido = añadir_conexion(comput, switch)
        if añadido:
            computadores_escritorio.remove(comput)
        else:
            print(f"No se pudo conectar el computador_escritorio {comput} al switch_cliente {switch}.")
    elif puntos_acceso:
        pa = np.random.choice(puntos_acceso)
        añadido = añadir_conexion(comput, pa)
        if añadido:
            computadores_escritorio.remove(comput)
        else:
            print(f"No se pudo conectar el computador_escritorio {comput} al punto_acceso {pa}.")

for laptop in laptops.copy():  # Usar copy para evitar modificar la lista durante la iteración
    if len(conexiones_vistas) >= max_aristas:
        break
    # Decidir aleatoriamente si conectar a switch_cliente o punto_acceso
    if np.random.rand() < 0.5 and switches_cliente:
        switch = np.random.choice(switches_cliente)
        añadido = añadir_conexion(laptop, switch)
        if añadido:
            laptops.remove(laptop)
        else:
            print(f"No se pudo conectar la laptop {laptop} al switch_cliente {switch}.")
    elif puntos_acceso:
        pa = np.random.choice(puntos_acceso)
        añadido = añadir_conexion(laptop, pa)
        if añadido:
            laptops.remove(laptop)
        else:
            print(f"No se pudo conectar la laptop {laptop} al punto_acceso {pa}.")

# 7. Conectar firewalls a routers_empresa o switches_empresa
print("Conectando firewalls a routers_empresa o switches_empresa...")
for firewall in firewalls:
    if len(conexiones_vistas) >= max_aristas:
        break
    tipo_destino = np.random.choice(['router_empresa', 'switch_empresa'], p=[0.7, 0.3])
    if tipo_destino == 'router_empresa':
        destino = np.random.choice(routers_empresa)
    else:
        destino = np.random.choice(switches_empresa)
    añadido = añadir_conexion(firewall, destino)
    if not añadido:
        print(f"No se pudo conectar el firewall {firewall} al {tipo_destino} {destino}.")

# 8. Conectar servidores a switches_empresa
print("Conectando servidores a switches_empresa...")
for servidor in servidores:
    if len(conexiones_vistas) >= max_aristas:
        break
    num_conexiones = np.random.choice([1, 2], p=[0.95, 0.05])
    switches_conectados = np.random.choice(switches_empresa, size=min(num_conexiones, len(switches_empresa)), replace=False)
    for switch in switches_conectados:
        if len(conexiones_vistas) >= max_aristas:
            break
        añadir_conexion(servidor, switch)

# 9. Conectar routers_empresa entre sí para redundancia
print("Conectando routers_empresa entre sí para redundancia...")
for router in routers_empresa:
    if len(conexiones_vistas) >= max_aristas:
        break
    # Decidir cuántas conexiones a otros routers (1-2)
    num_conexiones = np.random.randint(1, 3)
    posibles_destinos = [r for r in routers_empresa if r != router]
    destinos = np.random.choice(posibles_destinos, size=min(num_conexiones, len(posibles_destinos)), replace=False)
    for dest in destinos:
        if len(conexiones_vistas) >= max_aristas:
            break
        añadir_conexion(router, dest)

# 10. Conexiones entre switches_empresa (poco comunes)
print("Conectando switches_empresa entre sí (poco comunes)...")
num_switch_switch_connections = min(len(switches_empresa) * 2, 100)  # Limitar a 100 conexiones switch-switch
for _ in range(num_switch_switch_connections):
    if len(conexiones_vistas) >= max_aristas:
        break
    origen, destino = np.random.choice(switches_empresa, size=2, replace=False)
    añadido = añadir_conexion(origen, destino)
    if not añadido:
        print(f"No se pudo conectar el switch_empresa {origen} al switch_empresa {destino}.")

# 11. Rellenar conexiones restantes de forma aleatoria respetando reglas
print("Rellenando conexiones restantes de forma aleatoria...")
while len(conexiones_vistas) < max_aristas:
    origen_id = np.random.choice(routers_empresa + switches_empresa + firewalls + servidores + puntos_acceso + routers_cliente + switches_cliente)
    destino_id = np.random.choice(routers_empresa + switches_empresa + firewalls + servidores + puntos_acceso + routers_cliente + switches_cliente)
    
    # Evitar conexiones con dispositivos finales de clientes
    if id_tipo.get(origen_id) in ["laptop", "celular", "tablet", "computador_escritorio"]:
        continue
    if id_tipo.get(destino_id) in ["laptop", "celular", "tablet", "computador_escritorio"]:
        continue
    
    # Evitar conexiones no permitidas
    tipo_origen = id_tipo.get(origen_id)
    tipo_destino = id_tipo.get(destino_id)
    
    conexiones_validas = False
    if tipo_origen == 'switch_empresa' and tipo_destino in ["router_empresa", "firewall", "servidor", "switch_empresa", "punto_acceso"]:
        conexiones_validas = True
    elif tipo_origen == 'router_empresa' and tipo_destino in ["router_empresa", "switch_empresa", "firewall"]:
        conexiones_validas = True
    elif tipo_origen == 'firewall' and tipo_destino in ["router_empresa", "switch_empresa"]:
        conexiones_validas = True
    elif tipo_origen == 'servidor' and tipo_destino in ["switch_empresa"]:
        conexiones_validas = True
    elif tipo_origen == 'punto_acceso' and tipo_destino in ["switch_cliente"]:
        conexiones_validas = True
    elif tipo_origen == 'router_cliente' and tipo_destino in ["switch_cliente"]:
        conexiones_validas = True
    elif tipo_origen == 'switch_cliente' and tipo_destino in ["router_cliente", "switch_cliente", "laptop", "celular", "tablet", "computador_escritorio"]:
        conexiones_validas = True
    
    if conexiones_validas:
        añadido = añadir_conexion(origen_id, destino_id)
        if añadido:
            continue
    # Si no es válido o ya existe, intentar otra conexión
    continue

# 12. Asegurar que todos los dispositivos tengan al menos una conexión
print("Asegurando que todos los dispositivos tengan al menos una conexión...")
# Crear conjuntos de nodos conectados
nodos_conectados = set(origen_ids).union(set(destino_ids))

# Encontrar nodos sin conexiones
nodos_sin_conexion = set(df_nodos['id']) - nodos_conectados

for nodo in nodos_sin_conexion:
    if len(conexiones_vistas) >= max_aristas:
        print(f"Se ha alcanzado el máximo de aristas. No se pudo conectar el nodo {nodo}.")
        break
    tipo_nodo = id_tipo.get(nodo)
    if tipo_nodo in ['router_empresa', 'switch_empresa', 'router_cliente', 'switch_cliente', 'firewall', 'servidor', 'punto_acceso']:
        # Conectar a otro nodo del mismo tipo preferiblemente
        posibles_destinos = []
        if tipo_nodo == 'router_empresa':
            posibles_destinos = [r for r in routers_empresa if r != nodo]
        elif tipo_nodo == 'switch_empresa':
            posibles_destinos = [s for s in switches_empresa if s != nodo]
        elif tipo_nodo == 'router_cliente':
            posibles_destinos = [r for r in routers_cliente if r != nodo]
        elif tipo_nodo == 'switch_cliente':
            posibles_destinos = [s for s in switches_cliente if s != nodo]
        elif tipo_nodo == 'firewall':
            posibles_destinos = routers_empresa + switches_empresa
        elif tipo_nodo == 'servidor':
            posibles_destinos = switches_empresa
        elif tipo_nodo == 'punto_acceso':
            posibles_destinos = switches_empresa
        
        if posibles_destinos:
            destino = np.random.choice(posibles_destinos)
            añadido = añadir_conexion(nodo, destino)
            if not añadido:
                print(f"No se pudo conectar el nodo {nodo} al nodo {destino}.")
    elif tipo_nodo in ['laptop', 'celular', 'tablet']:
        # Deben conectarse a puntos_acceso
        if puntos_acceso:
            pa = np.random.choice(puntos_acceso)
            añadido = añadir_conexion(nodo, pa)
            if añadido:
                dispositivos_clientes[tipo_nodo].append(nodo)  # Reasignar si es necesario
            else:
                print(f"No se pudo conectar el dispositivo {nodo} al punto_acceso {pa}.")
    elif tipo_nodo == 'computador_escritorio':
        # Puede conectarse a switches_cliente o puntos_acceso
        if switches_cliente and np.random.rand() < 0.5:
            switch = np.random.choice(switches_cliente)
            añadido = añadir_conexion(nodo, switch)
            if añadido:
                computadores_escritorio.append(nodo)
                continue
        if puntos_acceso:
            pa = np.random.choice(puntos_acceso)
            añadido = añadir_conexion(nodo, pa)
            if añadido:
                computadores_escritorio.append(nodo)

# Crear el DataFrame con las conexiones generadas
df_conexiones = pd.DataFrame({
    'origen_id': origen_ids,
    'destino_id': destino_ids,
    'costo': costos
})

# Guardar el DataFrame en un archivo CSV
df_conexiones.to_csv('aristas2.csv', index=False)
print("Archivo aristas2.csv generado con éxito.")