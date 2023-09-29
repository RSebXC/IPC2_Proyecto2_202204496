import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, simpledialog
from graphviz import Digraph  # Asegúrate de tener instalada esta librería (pip install graphviz)

# Clases para representar un Dron, SistemaDrones, Mensaje e Instruccion
class Dron:
    def __init__(self, nombre):
        self.nombre = nombre
        self.altura = 0
        self.siguiente_dron = None

class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.primer_dron = None

    def agregar_dron(self, nombre):
        nuevo_dron = Dron(nombre)
        if not self.primer_dron:
            self.primer_dron = nuevo_dron
        else:
            ultimo_dron = self.primer_dron
            while ultimo_dron.siguiente_dron:
                ultimo_dron = ultimo_dron.siguiente_dron
            ultimo_dron.siguiente_dron = nuevo_dron

class Mensaje:
    def __init__(self, nombre, sistema_drones):
        self.nombre = nombre
        self.sistema_drones = sistema_drones
        self.primer_instruccion = None

    def agregar_instruccion(self, dron, altura):
        nueva_instruccion = Instruccion(dron, altura)
        if not self.primer_instruccion:
            self.primer_instruccion = nueva_instruccion
        else:
            ultima_instruccion = self.primer_instruccion
            while ultima_instruccion.siguiente_instruccion:
                ultima_instruccion = ultima_instruccion.siguiente_instruccion
            ultima_instruccion.siguiente_instruccion = nueva_instruccion

class Instruccion:
    def __init__(self, dron, altura):
        self.dron = dron
        self.altura = altura
        self.siguiente_instruccion = None

# Clase principal de la aplicación
class DroneMessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Messaging App")

        # Variables para almacenar datos
        self.drones = []
        self.sistemas_drones = []
        self.mensajes = []

        # Barra de navegación (navbar)
        self.navbar_frame = tk.Frame(root)
        self.navbar_frame.pack(fill=tk.X)

        # Botón "Cargar archivo"
        cargar_archivo_button = tk.Button(self.navbar_frame, text="Cargar archivo", command=self.cargar_archivo)
        cargar_archivo_button.pack(side=tk.LEFT)

        # Botón "Generar archivo"
        generar_archivo_button = tk.Button(self.navbar_frame, text="Generar archivo", command=self.generar_archivo)
        generar_archivo_button.pack(side=tk.LEFT)

        # Botón "Gestión de drones"
        gestion_drones_button = tk.Button(self.navbar_frame, text="Gestión de drones", command=self.gestion_drones)
        gestion_drones_button.pack(side=tk.LEFT)

        # Botón "Generar Instrucciones"
        generar_instrucciones_button = tk.Button(self.navbar_frame, text="Generar Instrucciones", command=self.generar_instrucciones)
        generar_instrucciones_button.pack(side=tk.LEFT)

        # Cuerpo principal
        self.cuerpo_frame = tk.Frame(root)
        self.cuerpo_frame.pack(fill=tk.BOTH, expand=True)

    def cargar_archivo(self):
        # Lógica para cargar un archivo XML
        self.file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if self.file_path:
            # Procesar el archivo XML aquí
            self.procesar_archivo_xml(self.file_path)

    def procesar_archivo_xml(self, file_path):
        try:
            # Parsear el archivo XML
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Resetear datos almacenados
            self.drones = []
            self.sistemas_drones = []
            self.mensajes = []

            # Leer los drones
            for dron_elem in root.findall('.//listaDrones/dron'):
                self.drones.append(dron_elem.text)

            # Leer los sistemas de drones
            for sistema_elem in root.findall('.//listaSistemasDrones/sistemaDrones'):
                nombre_sis = sistema_elem.get('nombre')
                altura_max = int(sistema_elem.find('alturaMaxima').text)
                cantidad_drones = int(sistema_elem.find('cantidadDrones').text)
                nuevo_sistema = SistemaDrones(nombre_sis, altura_max, cantidad_drones)

                for contenido_elem in sistema_elem.findall('contenido'):
                    dron = contenido_elem.find('dron').text
                    alturas = contenido_elem.find('alturas')
                    for altura_elem in alturas.findall('altura'):
                        alt = altura_elem.get('valor')
                        caracter = altura_elem.text
                        nuevo_dron = Dron(dron)
                        nuevo_dron.altura = int(alt)
                        nuevo_dron.caracter = caracter
                        nuevo_sistema.agregar_dron(nuevo_dron)

                self.sistemas_drones.append(nuevo_sistema)

            # Leer los mensajes
            for mensaje_elem in root.findall('.//listaMensajes/Mensaje'):
                nombre_mensaje = mensaje_elem.get('nombre')
                sistema_mensaje = mensaje_elem.find('sistemaDrones').text
                nuevo_mensaje = Mensaje(nombre_mensaje, sistema_mensaje)

                instrucciones_elem = mensaje_elem.find('instrucciones')
                for instruccion_elem in instrucciones_elem.findall('instruccion'):
                    dron = instruccion_elem.get('dron')
                    altura = int(instruccion_elem.text)
                    nuevo_mensaje.agregar_instruccion(dron, altura)

                self.mensajes.append(nuevo_mensaje)

            print("Archivo XML cargado y procesado con éxito.")

        except ET.ParseError:
            print("Error al parsear el archivo XML.")
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")

    def generar_archivo(self):
        # Lógica para generar un archivo XML de salida
        # Debes implementar esta función
        pass

    def gestion_drones(self):
        # Lógica para la gestión de drones
        # Debes implementar esta función
        pass

    def generar_instrucciones(self):
        if not self.file_path:
            print("No se ha cargado ningún archivo.")
            return

        # Obtener el nombre del mensaje a través de un cuadro de diálogo
        mensaje_nombre = simpledialog.askstring("Nombre de Mensaje", "Ingrese el nombre del mensaje:")

        if mensaje_nombre:
            # Buscar el mensaje por nombre
            mensaje = None
            for msg in self.mensajes:
                if msg.nombre == mensaje_nombre:
                    mensaje = msg
                    break

            if mensaje:
                # Calcular el tiempo óptimo
                tiempo_optimo = 0
                instruccion_actual = mensaje.primer_instruccion
                while instruccion_actual:
                    # Subir o bajar demora 1 segundo
                    tiempo_optimo += 1
                    # Encender la luz demora 1 segundo
                    tiempo_optimo += 1
                    instruccion_actual = instruccion_actual.siguiente_instruccion

                # Generar el archivo de instrucciones
                self.generar_archivo_instrucciones(mensaje, tiempo_optimo)

            else:
                print(f"No se encontró un mensaje con el nombre '{mensaje_nombre}'.")

    def generar_archivo_instrucciones(self, mensaje, tiempo_optimo):
        # Crear un archivo XML para las instrucciones
        respuesta = ET.Element("respuesta")
        lista_mensajes = ET.SubElement(respuesta, "listaMensajes")
        mensaje_elem = ET.SubElement(lista_mensajes, "mensaje")
        mensaje_elem.set("nombre", mensaje.nombre)

        sistema_drones_elem = ET.SubElement(mensaje_elem, "sistemaDrones")
        sistema_drones_elem.text = mensaje.sistema_drones

        tiempo_optimo_elem = ET.SubElement(mensaje_elem, "tiempoOptimo")
        tiempo_optimo_elem.text = str(tiempo_optimo)

        mensaje_recibido = ""
        instruccion_actual = mensaje.primer_instruccion
        while instruccion_actual:
            mensaje_recibido += instruccion_actual.dron
            instruccion_actual = instruccion_actual.siguiente_instruccion

        mensaje_recibido_elem = ET.SubElement(mensaje_elem, "mensajeRecibido")
        mensaje_recibido_elem.text = mensaje_recibido

        instrucciones_elem = ET.SubElement(mensaje_elem, "instrucciones")
        tiempo = 1
        instruccion_actual = mensaje.primer_instruccion
        while instruccion_actual:
            tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo")
            tiempo_elem.set("valor", str(tiempo))

            acciones_elem = ET.SubElement(tiempo_elem, "acciones")
            dron_elem = ET.SubElement(acciones_elem, "dron")
            dron_elem.set("nombre", instruccion_actual.dron)
            if tiempo % 2 == 1:
                dron_elem.text = "Subir"
            else:
                dron_elem.text = "EmitirLuz"

            tiempo += 1
            instruccion_actual = instruccion_actual.siguiente_instruccion

        # Generar el archivo XML
        instrucciones_tree = ET.ElementTree(respuesta)
        instrucciones_tree.write("instrucciones.xml")

        print(f"Archivo de instrucciones para el mensaje '{mensaje.nombre}' generado con éxito.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DroneMessagingApp(root)
    root.mainloop()
