# DataPathway

Este proyecto tiene como objetivo optimizar el flujo de tráfico en una red de datos utilizando un enfoque basado en grafos. Se compara el rendimiento de dos algoritmos, **Kruskal** y **Prim**, para la construcción de un **Árbol de Expansión Mínima (MST)**, y se implementa una solución para optimizar la transmisión de datos y reducir la congestión en la red.

## Integrantes

- Delgado Corrales, Piero Gonzalo
- Paredes Puente, Sebastián Roberto
- Valverde Mozo, Andre Gabriel

## Descripción

Se trabajó en un grupo para el curso **CC76 - Complejidad Algorítmica**. Para el proyecto, se utilizó un conjunto de datos real con más de 3.5 millones de flujos de red, donde las direcciones IP se modelaron como nodos y las interacciones de tráfico entre ellas como aristas del grafo. La red resultante representa las conexiones entre dispositivos de la red y el volumen de datos transferidos entre ellos.

### Objetivos
1. Comparar los algoritmos de Kruskal y Prim en la construcción de un Árbol de Expansión Mínima (MST).
2. Optimizar la transmisión de datos para reducir la congestión y mejorar la eficiencia del uso del ancho de banda en la red.
3. Minimizar los costos operativos mediante la identificación de las rutas más eficientes para la transferencia de datos.
4. Visualizar graficamente los grafos con datos originales y árboles de expansión mínima.

## Algoritmos Implementados

### Kruskal
El algoritmo de **Kruskal** fue implementado para construir un Árbol de Expansión Mínima (MST) buscando las conexiones más económicas entre nodos y minimizando el uso de ancho de banda innecesario. Este algoritmo es eficiente para redes dispersas, donde los nodos tienen pocas conexiones directas.

### Prim
El algoritmo de **Prim** también fue implementado y comparado con Kruskal. A diferencia de Kruskal, Prim crece el MST agregando un nodo a la vez, eligiendo siempre el nodo más cercano al MST en formación. Este enfoque es adecuado para redes densas, donde la mayoría de los nodos están conectados.

Ambos algoritmos fueron evaluados en función de la eficiencia, la complejidad temporal y la efectividad en la optimización del tráfico de red.

## Estructura del Proyecto

- `scripts/`: Algoritmos como Kruskal y Prim del proyecto.
- `static/`: Archivos de estilos e imagenes para su visualización en la página web.
- `templates/`: Archivos html con la estructura de la página web.

## Requisitos

- Python 3.x
- Bibliotecas necesarias:
    - `networkx`
    - `matplotlib`
    - `flask`
    - `pandas`
    - `scipy`

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/usuario/proyecto-optimizacion-trafico.git
    cd proyecto-optimizacion-trafico
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta el proyecto:

    ```bash
    python main.py
    ```


