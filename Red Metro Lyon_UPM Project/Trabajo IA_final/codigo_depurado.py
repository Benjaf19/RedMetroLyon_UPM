import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import random
import folium
from typing import List
from scipy.spatial import distance
from datetime import datetime


# Función para determinar la frecuencia de los metros segun sea hora pico o no
def obtener_frecuencia_metro(hora_usuario: str) -> int:
    h_inic_mañana, h_fin_mañana = "07:00", "09:00"
    h_inic_tarde, h_fin_tarde = "16:00", "19:00"

    if verificar_rango_hora(hora_usuario, h_inic_mañana, h_fin_mañana) or verificar_rango_hora(hora_usuario,
                                                                                               h_inic_tarde,
                                                                                               h_fin_tarde):
        return random.choice(range(1, 4))  # COMENTARIO: elige aleatoriamente un número entre 1, 2 y 3.
    else:
        return random.choice(range(4, 7))  # COMENTARIO: elige aleatoriamente un número entre 4, 5 y 6.


# Verifica si la hora seleccionada pertenece a un rango dado
def verificar_rango_hora(hora_usuario: str, hora_inicio: str, hora_fin: str) -> bool:
    hora_obj = datetime.strptime(hora_usuario,
                                 '%H:%M')  # COMENTARIO: strptime: "string parse time", convierte la hora_usuario en objeto datetime, después hace lo mismo para hora_inicio y hora_fin
    hora_inic_obj, hora_fin_obj = map(lambda x: datetime.strptime(x, '%H:%M'), [hora_inicio, hora_fin])
    return hora_inic_obj <= hora_obj <= hora_fin_obj


def validar_estaciones(estacion_de_origen, estacion_de_destino):
    if estacion_de_origen not in graph.nodes or estacion_de_destino not in graph.nodes:
        print("Una o ambas estaciones no existen en el grafo. Verifica los nombres e inténtalo de nuevo.")
        exit()
    elif estacion_de_origen == estacion_de_destino:
        print("Ambas estaciones son la misma. Verifica los nombres e inténtalo de nuevo.")
        exit()


# Función para crear el grafo con las estaciones como nodo y sus conexiones como aristas
def construir_grafo_estaciones() -> nx.Graph:
    graph = nx.Graph()
    # Por cada fila en el dataframe (df) de estaciones asigna su nombre, coordenadas y color
    for _, estacion in estaciones_df.iterrows():
        nombre = estacion['nombre']
        coord = (estacion['coord_este'], estacion['coord_norte'])
        color = estacion['color']
        url_maps = estacion['url_maps']
        url_wiki = estacion['url_wiki']
        graph.add_node(nombre, nombre=nombre, coord=coord, color=color, url_maps=url_maps, url_wiki=url_wiki)

    # COMENTARIO: La _ se utliza para indicar que no utilizamos el índice ya que iterrows() devuelve un par de valores, el indice y una serie con los datos de la fila

    # Por cada fila en el df de aristas asigna sus estacion origen y destino, su distancia tiempo y color
    for _, arista in aristas_df.iterrows():
        estacion_origen, estacion_destino = arista['estacion_origen'], arista['estacion_destino']
        distancia, tiempo, color = arista['distancia'], arista['tiempo'], arista['color']
        graph.add_edge(estacion_origen, estacion_destino, distancia=distancia, tiempo=tiempo, color=color)

    return graph


def heuristica_distancia_euclidiana(nodo_actual: str, objetivo: str) -> float:
    coord1, coord2 = graph.nodes[nodo_actual]['coord'], graph.nodes[objetivo]['coord']
    return distance.euclidean(coord1, coord2)


def heuristica_tiempo(nodo_actual: str, objetivo: str) -> float:
    coord1, coord2 = graph.nodes[nodo_actual]['coord'], graph.nodes[objetivo]['coord']
    distancia = distance.euclidean(coord1, coord2)  # COMENTARIO: metros

    max_speeds = {'red': 70.8, 'blue': 51, 'yellow': 26.13, 'green': 52.68}  # COMENTARIO: km/h

    try:
        # Obtener el color del nodo actual
        color_actual = graph[nodo_actual][objetivo]['color']
    except KeyError:
        color_actual = 'default'

    # Si el color no se encuentra la velocidad por defecto se establece en 80
    velocidad_maxima_mpm = max_speeds.get(color_actual, 80)

    tiempo_estimado = distancia / (
                velocidad_maxima_mpm * 1000 / 60)  # COMENTARIO: velocidad máxima se convierte a metros/minutos para devolver minutos en tiempo estimado
    return tiempo_estimado


def ejecutar_a_estrella(grafo: nx.Graph, inicio: str, objetivo: str, heuristica: float, funcion_costo: str):
    # Utilizar A* para encontrar el camino más corto
    camino = nx.astar_path(grafo, inicio, objetivo, heuristic=heuristica, weight=funcion_costo)
    total, colores_visitados = 0, set()

    # Costo total y los colores visitados a lo largo del camino
    for i in range(len(camino) - 1):
        edge = (camino[i], camino[i + 1])
        total += grafo[edge[0]][edge[1]][funcion_costo]
        colores_visitados.add(grafo[edge[0]][edge[1]]['color'])

    return camino, total, colores_visitados


# Función para crear la ruta que debe seguir el usuario
def imprimir_ruta(camino: List[str]):
    # Verifica si hay un camino disponible
    if not camino:
        print("No hay camino disponible entre las estaciones de origen y destino.")
        return

    estacion_actual, color_actual = camino[0], graph[camino[0]][camino[1]]['color']
    primera_estacion_color = estacion_actual
    informacion_ruta = []

    for i in range(1, len(camino)):

        estacion_siguiente = camino[i]
        color_siguiente = graph[estacion_actual][estacion_siguiente]['color']

        # Compara el color actual con el siguiente
        if color_actual != color_siguiente:
            ultima_estacion_color = estacion_actual
            linea, color = lineas_dict.get(color_actual, ('Desconocida',
                                                          color_actual))  # COMENTARIO: Si color_actual está en el diccionario, devuelve el valor correspondiente, si no está en el diccionario, devuelve ('Desconocida', color_actual) como valor predeterminado.
            informacion_ruta.append(
                f"    - Usa la línea {linea} ({color}) y ve desde {primera_estacion_color} a {ultima_estacion_color}")
            primera_estacion_color = estacion_actual

        # Actualiza las estaciones y colores
        estacion_actual, color_actual = estacion_siguiente, color_siguiente

    ultima_estacion_color = estacion_actual
    linea, color = lineas_dict.get(color_actual, ('Desconocida', color_actual))
    informacion_ruta.append(
        f" Usa la línea {linea} ({color}) y ve desde {primera_estacion_color} a {ultima_estacion_color} LLEGASTE!!!")

    return informacion_ruta


# Función para visualizar el grafo
def visualizar_grafo(graph: nx.Graph):
    pos = nx.get_node_attributes(graph, 'coord')
    estaciones_id = dict(zip(estaciones_df['nombre'], estaciones_df['Id']))
    node_colors = [data["color"] if data["color"] != "blue" else "skyblue" for _, data in graph.nodes(data=True)]
    edge_colors = list(nx.get_edge_attributes(graph, 'color').values())
    font_size = 7

    nx.draw(graph, pos=pos, labels=estaciones_id, node_color=node_colors, with_labels=True, font_size=font_size,
            font_color="black",
            font_weight="bold", node_size=100)

    nx.draw_networkx_edges(graph, pos=pos, edge_color=edge_colors)

    edge_labels = nx.get_edge_attributes(graph, 'id')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=font_size, font_color="red")

    plt.show()


# Leer datos desde archivos
estaciones_df = pd.read_excel("C:\\Users\\benja\\Downloads\\Trabajo IA_final\\Trabajo IA_final\\estaciones.xlsx")
aristas_df = pd.read_excel("C:\\Users\\benja\\Downloads\\Trabajo IA_final\\Trabajo IA_final\\aristas.xlsx")

graph = construir_grafo_estaciones()

# Calcular heurística de tiempo y distancia
lineas_dict = {'red': ('A', 'roja'), 'blue': ('B', 'azul'), 'orange': ('C', 'amarilla'), 'green': ('D', 'verde')}