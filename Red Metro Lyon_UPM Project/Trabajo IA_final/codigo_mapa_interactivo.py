import networkx as nx
import pandas as pd
import folium
from codigo_depurado import construir_grafo_estaciones




# Lectura de los nodos y aristas desde excel
estaciones_df = pd.read_excel("estaciones.xlsx")
aristas_df = pd.read_excel("aristas.xlsx")


# Creación del grafo con la función contruir_grafo_estaciones() de código final
graph = construir_grafo_estaciones()


def crear_mapa_interactivo(graph: nx.Graph):
   mapa = folium.Map(location=[45.74846, 4.84671], zoom_start=12)




   for nodo, estacion in graph.nodes(data=True):
       popup_content = (f'<strong>Estación:</strong> {estacion["nombre"]}<br><a href="{estacion["url_wiki"]}" target="_blank">Más información</a>'
                        f'<br><a href="{estacion["url_maps"]}" target="_blank">Google Maps</a>')




       folium.Marker([estacion["coord"][1], estacion["coord"][0]],
                     popup=folium.Popup(popup_content, max_width=300),
                     tooltip=estacion["nombre"],
                     icon=folium.Icon(color=estacion["color"])).add_to(mapa)




   for edge in graph.edges(data=True):
       estacion_origen, estacion_destino, data = edge
       coord_origen = (graph.nodes[estacion_origen]["coord"][1], graph.nodes[estacion_origen]["coord"][0])
       coord_destino = (graph.nodes[estacion_destino]["coord"][1], graph.nodes[estacion_destino]["coord"][0])
       folium.PolyLine([coord_origen, coord_destino],
                       color=data["color"],
                       weight=4,
                       opacity=1.0,
                       tooltip=f'Distancia: {data["distancia"]}, Tiempo: {data["tiempo"]}').add_to(mapa)




   mapa.save('static/mapa/mapa_interactivo.html')

crear_mapa_interactivo(graph)
