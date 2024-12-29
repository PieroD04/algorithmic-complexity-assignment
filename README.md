# DataPathway

This project aims to optimize traffic flow in a data network using a graph-based approach. It compares the performance of two algorithms, **Kruskal** and **Prim**, for constructing a **Minimum Spanning Tree (MST)**, and implements a solution to optimize data transmission and reduce congestion in the network.

## Team Members

- Delgado Corrales, Piero Gonzalo
- Paredes Puente, Sebastián Roberto
- Valverde Mozo, Andre Gabriel

## Description

This project was carried out in a group for the course **CC76 - Algorithmic Complexity**. For the project, a real dataset with over 3.5 million network flows was used, where IP addresses were modeled as nodes and traffic interactions between them as edges in the graph. The resulting network represents the connections between devices and the volume of data transferred between them.

### Objectives
1. Compare the Kruskal and Prim algorithms in constructing a Minimum Spanning Tree (MST).
2. Optimize data transmission to reduce congestion and improve bandwidth efficiency in the network.
3. Minimize operational costs by identifying the most efficient routes for data transfer.
4. Visualize the graphs with original data and the minimum spanning trees.

## Algorithms Implemented

### Kruskal
The **Kruskal** algorithm was implemented to construct a Minimum Spanning Tree (MST) by finding the most economical connections between nodes and minimizing unnecessary bandwidth usage. This algorithm is efficient for sparse networks, where nodes have few direct connections.

### Prim
The **Prim** algorithm was also implemented and compared to Kruskal. Unlike Kruskal, Prim grows the MST by adding one node at a time, always choosing the node closest to the MST being formed. This approach is suitable for dense networks, where most nodes are connected.

Both algorithms were evaluated based on efficiency, time complexity, and effectiveness in optimizing network traffic.

## Project Structure

- `scripts/`: Algorithms like Kruskal and Prim used in the project.
- `static/`: Style files and images for visualization in the web page.
- `templates/`: HTML files for the structure of the web page.

## Requirements

- Python 3.x
- Required libraries:
    - `networkx`
    - `matplotlib`
    - `flask`
    - `pandas`
    - `scipy`

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/usuario/proyecto-optimizacion-trafico.git
    cd proyecto-optimizacion-trafico
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the project:

    ```bash
    python main.py
    ```