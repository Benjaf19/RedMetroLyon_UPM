from flask import Flask, render_template, request, jsonify
import json
import re
import random
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance
import pandas as pd
from datetime import datetime
import subprocess

from codigo_depurado import imprimir_ruta, ejecutar_a_estrella, heuristica_tiempo, heuristica_distancia_euclidiana, \
    construir_grafo_estaciones, obtener_frecuencia_metro, validar_estaciones

app = Flask(__name__)

# Definir el rango de horas permitido
hora_minima = datetime.strptime("05:00", "%H:%M").time()
hora_maxima = datetime.strptime("00:30", "%H:%M").time()

@app.route('/')
def index():
    return render_template('index1.html')


# Función para guardar el camino en un archivo
def guardar_camino(camino, archivo):
    with open(archivo, 'w') as file:
        file.write(camino)

@app.route('/redireccionar', methods=['POST'])
def redireccionar():
    estacion_origen = request.form['estacion_origen']
    estacion_destino = request.form['estacion_destino']
    hora = request.form['hora']
    metodo=request.form['metodo']
    # Convertir la cadena de hora a un objeto datetime.time
    hora_obj = datetime.strptime(hora, "%H:%M").time()
    subprocess.Popen(["python", "Trabajo IA_final\\muffin.py"])

    # Puedes redirigir a otra página o simplemente mostrar un mensaje de éxito
   
    # Verificar si la hora está dentro del rango permitido
    if hora_obj < hora_minima and hora_obj > hora_maxima:
        mensaje_error = "La hora ingresada no está dentro del rango permitido (desde las 5:00 AM hasta las 12:00 AM)."
        return render_template('index1.html', mensaje_error=mensaje_error)


    frase = f"ESTACIÓN ORIGEN: {estacion_origen}, ESTACIÓN DESTINO: {estacion_destino}, HORA: {hora}, METODO: {metodo}"

    resultados = procesar_datos(estacion_origen, estacion_destino, hora)
    if resultados is None:
        mensaje_error = "Una o ambas estaciones no existen en el grafo. Verifica los nombres e inténtalo de nuevo."
        return render_template('index1.html', mensaje_error=mensaje_error)

    camino_tiempo, camino_distancia, tiempo_total, distancia_total, colores_tiempo, colores_distancia, \
        distancia_en_camino_tiempo, tiempo_en_camino_distancia, frecuencia = procesar_datos(estacion_origen,
                                                                                            estacion_destino, hora)

    if (camino_tiempo == camino_distancia or distancia_en_camino_tiempo <= distancia_total) and metodo!='d':
        ruta = ". ".join(imprimir_ruta(camino_tiempo))
        camino = ", ".join(
            camino_tiempo)  # COMENTARIO: La lista camino_tiempo la une en una cadena separando cada elemento por ", "
        tiempo_final = tiempo_total + frecuencia*len(colores_tiempo)

        # Guardar el camino en un archivo
        guardar_camino(camino, 'camino.txt')

        distancia_final = f"{distancia_en_camino_tiempo / 1000:.2f}" # COMENTARIO: ":.2f" especificación de formato que indica que se deben mostrar dos decimales después del punto decimal (.2f).
        return render_template('seccion3.html', camino=camino, ruta=ruta, tiempo=tiempo_final,
                               distancia=distancia_final, texto=frase,estacion_destino=estacion_destino,estacion_origen=estacion_origen,hora=hora)
    else:
        ruta = ". ".join(imprimir_ruta(camino_distancia))
        camino = ", ".join(camino_distancia)
        distancia_final = f"{distancia_total / 1000:.2f}"
        tiempo_final = tiempo_en_camino_distancia + frecuencia*len(colores_distancia)

        # Guardar el camino en un archivo
        guardar_camino(camino, 'camino.txt')

        return render_template('seccion4.html', camino=camino, ruta=ruta, tiempo=tiempo_final,
                               distancia=distancia_final, texto=frase,estacion_destino=estacion_destino,estacion_origen=estacion_origen,hora=hora)


@app.route('/seccion1', methods=['POST'])
def seccion1():
    return render_template('seccion1.html')


@app.route('/seccion2', methods=['POST'])
def seccion2():
    return render_template('seccion2.html')


def procesar_datos(estacion_origen, estacion_destino, hora):
    hora_usuario = hora
    frecuencia = obtener_frecuencia_metro(hora_usuario)
    lineas_dict = {'red': ('A', 'roja'), 'blue': ('B', 'azul'), 'orange': ('C', 'amarilla'), 'green': ('D', 'verde')}

    estacion_de_origen = estacion_origen
    estacion_de_destino = estacion_destino

    # validar_estaciones(estacion_de_origen, estacion_de_destino)
    graph = construir_grafo_estaciones()
    if estacion_origen not in graph.nodes or estacion_destino not in graph.nodes or estacion_origen == estacion_destino:
        return None

    camino_tiempo, tiempo_total, colores_tiempo = ejecutar_a_estrella(graph, estacion_de_origen, estacion_de_destino,
                                                                      heuristica_tiempo, 'tiempo')
    camino_distancia, distancia_total, colores_distancia = ejecutar_a_estrella(graph, estacion_de_origen,
                                                                               estacion_de_destino,
                                                                               heuristica_distancia_euclidiana,
                                                                               'distancia')
    tiempo_en_camino_distancia = sum(
        graph[camino_distancia[i]][camino_distancia[i + 1]]['tiempo'] for i in range(len(camino_distancia) - 1))
    distancia_en_camino_tiempo = sum(
        graph[camino_tiempo[i]][camino_tiempo[i + 1]]['distancia'] for i in range(len(camino_tiempo) - 1))

    return camino_tiempo, camino_distancia, tiempo_total, distancia_total, colores_tiempo, colores_distancia, distancia_en_camino_tiempo, tiempo_en_camino_distancia, frecuencia




if __name__ == '__main__':
    app.run(debug=True)
