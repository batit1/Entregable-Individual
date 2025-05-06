import networkx as nx
import matplotlib.pyplot as plt
import random

def crear_red(n_nodos=15, probabilidad_conexion=0.4):
    G = nx.Graph()
    for i in range(n_nodos):
        G.add_node(i)
    for i in range(n_nodos):
        for j in range(i + 1, n_nodos):
            if random.random() < probabilidad_conexion:
                G.add_edge(i, j)
    return G

def simular_propagacion(G, nodo_inicial):
    tiempos = {}
    visitados = []

    tiempos[nodo_inicial] = 0
    visitados.append(nodo_inicial)
    cola = [nodo_inicial]

    while len(cola) > 0:
        actual = cola.pop(0)
        for vecino in G.neighbors(actual):
            if vecino not in visitados:
                tiempos[vecino] = tiempos[actual] + 1
                visitados.append(vecino)
                cola.append(vecino)

    for nodo in G.nodes():
        if nodo not in tiempos:
            tiempos[nodo] = -1

    return tiempos

def visualizar_propagacion(G, tiempos):
    posiciones = nx.spring_layout(G, seed=42)  

    tiempos_validos = [t for t in tiempos.values() if t >= 0]
    if not tiempos_validos:
        print("Ningún nodo recibió la información.")
        return

    max_tiempo = max(tiempos_validos)
    colores = []

    for nodo in G.nodes():
        tiempo = tiempos[nodo]
        if tiempo == -1:
            colores.append(1.0)  
        else:
            colores.append(tiempo / max_tiempo if max_tiempo > 0 else 0.0)

    nx.draw(G, posiciones, with_labels=True, node_color=colores, cmap=plt.cm.viridis, node_size=700)
    plt.title("Simulación de Propagación de Información")
    plt.show()

def main():
    red = crear_red(n_nodos=15, probabilidad_conexion=0.4)
    nodo_inicial = random.choice(list(red.nodes()))
    print("Nodo que inicia la propagación:", nodo_inicial)

    tiempos = simular_propagacion(red, nodo_inicial)
    print("Tiempos de llegada de la información:", tiempos)

    visualizar_propagacion(red, tiempos)

main()
