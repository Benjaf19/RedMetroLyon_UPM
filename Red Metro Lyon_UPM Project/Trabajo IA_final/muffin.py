from kivy.animation import Animation
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.core.window import Window
import random
import pandas as pd

def leer_camino_desde_archivo():
    camino = None
    try:
        with open('camino.txt', 'r') as file:
            camino = file.read()
    except FileNotFoundError:
        print("El archivo 'camino.txt' no se encontró.")
    return camino

class Station(Widget):
    def __init__(self, pos, color, **kwargs):
        super(Station, self).__init__(**kwargs)
        self.size=(20, 20)
        self.color = color

        with self.canvas:
            [c1, c2, c3] = color_assignment(color)
            size = self.size
            if self.color != "grey":
                animate = Animation(opacity=1, duration=.5)
                for i in range(0, 5):
                    animate += Animation(opacity=0.25, duration=.5)
                    animate += Animation(opacity=1, duration=.5)

                animate.bind()
                animate.start(self)

            self.circle = Ellipse(pos=(pos[0]-size[0]/2, pos[1]-size[1]/2), size=size, color=Color(c1, c2, c3))
            size =(self.size[0]*14.5/20, self.size[1]*14.5/20)
            [w1, w2, w3]=[233/255, 233/255, 233/255]
            self.circle = Ellipse(pos=(pos[0]-size[0]/2, pos[1]-size[1]/2), size=size, color=Color(w1, w2, w3))
            size =(self.size[0]*.5, self.size[1]*.5)
            self.circle = Ellipse(pos=(pos[0]-size[0]/2, pos[1]-size[1]/2), size=size, color=Color(c1, c2, c3))
            self.bind(pos=self.update_circle_position)

    def update_circle_position(self, instance, value):
        # Actualizar la posición del círculo cuando cambia la posición del widget
        self.circle.pos = self.pos

class Building(Widget):
    def __init__(self, **kwargs):
        super(Building, self).__init__(**kwargs)

        with self.canvas:
            self.pos=(random.randint(10, 50), random.randint(10, 50))
            pos=self.pos
            while pos[0]<1100:
                width = random.randint(5, 15)
                while pos[1]<900-random.randint(10, 50):
                    size=(width, random.randint(5, 15))
                    if random.randint(0, 9) == 6:
                        self.circle = Rectangle(pos=pos, size=size, color=Color(0.8, 0.8, 0.8, 0))
                    else:
                        self.circle = Rectangle(pos=pos, size=size, color=Color(0.8, 0.8, 0.8, 1))
                    pos=(pos[0], pos[1] + size[1]+3)
                pos=(pos[0]+width + 3, random.randint(10, 50))

class Rhone(Widget):
    def __init__(self, **kwargs):
        super(Rhone, self).__init__(**kwargs)

        with self.canvas:
            points_rhone = [230, 0, 220, 40, 200, 100, 250, 400, 333, 450, 375, 650, 375, 900, 400, 1200]
            Line(points=points_rhone, width=17,
                 color=Color(233/255, 233/255, 233/255), cap="round", joint="round")
            Line(points=points_rhone, width=10,
                 color=Color(0.75, .75,  1), cap="round", joint="round")

    def update_circle_position(self, instance, value):
        # Actualizar la posición del círculo cuando cambia la posición del widget
        self.circle.pos = self.pos


class Trip(Widget):
    def __init__(self, origin, end, color, shaded=True, width=2, **kwargs):
        super(Trip, self).__init__(**kwargs)
        self.size=(20, 20)
        self.color=color
        self.origin=origin
        self.end=end
        self.shaded=shaded

        with self.canvas:
            width = 5 if shaded else 2
            if self.color != "grey":
                animate = Animation(opacity=1, duration=.5)
                for i in range(0, 5):
                    animate += Animation(opacity=0.25, duration=.5)
                    animate += Animation(opacity=1, duration=.5)
                animate.bind()
                animate.start(self)

            c1, c2, c3 = color_assignment(self.color, self.shaded)
            points=self.origin + self.end
            self.circle = Line(points=points, width=width, color=Color(c1, c2, c3), cap="round", joint="round")

def ajuste_coordenadas(par):
    return (par[1] - 4.80)*8000 + 50, (par[0] - 45.70)*10000

def color_assignment(color, shaded=False):
    if color == "green":
        [c1, c2, c3] = [0.2, 1, 0.2]
    if color == "blue":
        [c1, c2, c3] = [0.2, 0.2, 0.8]
    if color == "red":
        [c1, c2, c3] = [1, 0.2, 0.2]
    if color == "orange":
        [c1, c2, c3] = [0.75, 0.75, 0.2]
    if color == "grey":
        [c1, c2, c3] = [0.6, 0.6, 0.6]
    if color == "gray":
        [c1, c2, c3] = [248/255, 0.2, 199/255]
    if shaded:
        c1 -= 0.15
        c2 -= 0.15
        c3 -= 0.15
    return [c1, c2, c3]

def ajuste_nombre(nombre):
    if nombre=="Place Guichard Bourse du Travail":
        return "Place Guichard"
    elif nombre=="Hôtel de Ville Louis Pradel":
        return "Hôtel de Ville"
    elif nombre=="Vieux Lyon Cathédrale St. Jean":
        return "Cathédrale St. Jean"
    elif nombre=="République Villeurbanne":
        return "R. Villeurbanne"
    else:
        return nombre

class MyApp(App):
    def __init__(self, camino, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.camino=camino

    def build(self):
        Window.clearcolor = (233/255, 233/255, 233/255)
        estaciones_df = pd.read_excel("C:\\Users\\benja\\Downloads\\Trabajo IA_final\\Trabajo IA_final\\estaciones2.xlsx")
        mapeo=Label(text="LYON MeTRO", color=(0.2, 0.2, 0.2, 0), font_size=50,
                     outline_color=(0, 0, 0, 0), outline_width=3)
        mapeo.add_widget(Building())
        mapeo.add_widget(Rhone())
        trace_color = None
        trace_coord = None
        trace_nombre=None

        #TODO: camino es una variable local.
        texto = leer_camino_desde_archivo()
        # Dividir el texto en líneas
        lineas = texto.splitlines()

        # Dividir cada línea en estaciones usando ","
        camino = [linea.strip() for linea in lineas[0].split(',')]

        # camino = ["Oullins Gare", "Stade de Gerland", "Debourg", "Place Jean Jaurès",
        #           "Jean Macé", "Saxe Gambetta", "Guillotière", "Bellecour", "Cordeliers",
        #           "Hôtel de Ville Louis Pradel", "Croix-Paquet", "Croix-Rousse", "Henon", "Cuire"]

        for _, estacion in estaciones_df.iterrows():
            nombre =estacion["nombre"]
            color = estacion['color']
            coord = ajuste_coordenadas((float(estacion['coord_norte']), float(estacion['coord_este'])))
            if color==trace_color or color == "gray" or trace_color=="gray":
                if color == "gray":
                    color = trace_color
                if (nombre in camino and trace_nombre in camino) or (nombre in camino and nombre==camino[-1]):
                    mapeo.add_widget(Trip(trace_coord, coord, color))
                    mapeo.add_widget(Trip(trace_coord, coord, color, shaded=False))
                else:
                    mapeo.add_widget(Trip(trace_coord, coord, "grey"))
                    mapeo.add_widget(Trip(trace_coord, coord, "grey", shaded=False))
            trace_color=color
            trace_coord=coord
            trace_nombre=nombre

        #bucle para las estaciones
        k=0
        for _, estacion in estaciones_df.iterrows():
            nombre = estacion["nombre"]
            color = estacion["color"]
            coord = ajuste_coordenadas((float(estacion["coord_norte"]), float(estacion["coord_este"])))
            label_coord = (coord[0] - 47, coord[1] - 70) if ((color=="red") and k%2==0) or nombre=="Vaulx-en-Velin La Soie" \
                else (coord[0] - 47, coord[1] - 30)
            k+=1
            if nombre not in camino:
                mapeo.add_widget(Station(pos=(coord), color="grey"))
                mapeo.add_widget(Label(text=ajuste_nombre(estacion["nombre"]), color=(233 / 255, 233 / 255, 233 / 255),
                                        outline_color=color_assignment(color="grey", shaded=True),
                                        outline_width=2, italic=True, font_size=15, pos=label_coord))
            else:
                mapeo.add_widget(Station(pos=(coord), color=color))
                mapeo.add_widget(Label(text=ajuste_nombre(estacion["nombre"]), color=(233 / 255, 233 / 255, 233 / 255),
                                        outline_color=color_assignment(color, shaded=True),
                                        outline_width=2, italic=True, font_size=15, pos=label_coord))
        return mapeo

if __name__ == '__main__':
    
    # ["Oullins Gare", "Stade de Gerland", "Debourg", "Place Jean Jaurès",
    #           "Jean Macé", "Saxe Gambetta", "Guillotière", "Bellecour", "Cordeliers",
    #           "Hôtel de Ville Louis Pradel", "Croix-Paquet", "Croix-Rousse", "Henon", "Cuire"]
    texto = leer_camino_desde_archivo()
    # Dividir el texto en líneas
    lineas = texto.splitlines()

    # Dividir cada línea en estaciones usando ","
    camino = [linea.strip() for linea in lineas[0].split(',')]  # Aquí deberías definir el camino que deseas utilizar
    app = MyApp(camino)
    app.build()  # Llamar al método build antes de run
    app.run()