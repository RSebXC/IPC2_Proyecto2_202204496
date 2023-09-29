import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox, filedialog

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.inicio = None

    def insertar_fin(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.inicio:
            self.inicio = nuevo_nodo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

class Dron:
    def __init__(self, nombre):
        self.nombre = nombre
        self.alturas = ListaEnlazada()

    def obtener_altura_letra(self, letra):
        altura_actual = self.alturas.inicio
        while altura_actual:
            if altura_actual.dato.letra == letra:
                return altura_actual.dato.altura
            altura_actual = altura_actual.siguiente
        return None


class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones, drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.drones = drones

    def encontrar_altura_letra(self, dron_nombre, letra):
        dron_actual = self.obtener_dron_por_nombre(dron_nombre)
        if dron_actual:
            return dron_actual.obtener_altura_letra(letra)
        return None

    def obtener_dron_por_nombre(self, nombre):
        dron_actual = self.drones.inicio
        while dron_actual:
            if dron_actual.dato.nombre == nombre:
                return dron_actual.dato
            dron_actual = dron_actual.siguiente
        return None


class Mensaje:
    def __init__(self, nombre, sistema_drones, instrucciones):
        self.nombre = nombre
        self.sistema_drones = sistema_drones
        self.instrucciones = instrucciones

class Instruccion:
    def __init__(self, dron, altura):
        self.dron = dron
        self.altura = altura

def cargar_datos(xml_string):
    drones = ListaEnlazada()
    sistemas_drones = ListaEnlazada()
    mensajes = ListaEnlazada()

    tree = ET.parse(xml_string)
    root = tree.getroot()

    # Leer los drones
    for dron_elem in root.findall('.//listaDrones/dron'):  
        nombre_dron = dron_elem.text
        drones.insertar_fin(Dron(nombre_dron, ListaEnlazada()))

    # Leer los sistemas de drones
    for sistema_elem in root.findall('.//listaSistemasDrones/sistemaDrones'): 
        nombre_sistema = sistema_elem.get('nombre')
        altura_maxima = int(sistema_elem.find('alturaMaxima').text)
        cantidad_drones = int(sistema_elem.find('cantidadDrones').text)
        drones_sistema = ListaEnlazada()

        for dron_elem in sistema_elem.findall('.//contenido/dron'):  
            nombre_dron = dron_elem.text
            alturas = dron_elem.find('../alturas') 
            drones_sistema.insertar_fin(Dron(nombre_dron, alturas))

        sistemas_drones.insertar_fin(SistemaDrones(nombre_sistema, altura_maxima, cantidad_drones, drones_sistema))

    # Leer los mensajes
    for mensaje_elem in root.findall('.//listaMensajes/Mensaje'): 
        nombre_mensaje = mensaje_elem.get('nombre')
        sistema_drones = mensaje_elem.find('sistemaDrones').text
        instrucciones = ListaEnlazada()

        for instruccion_elem in mensaje_elem.findall('.//instrucciones/instruccion'):  
            nombre_dron = instruccion_elem.get('dron')
            altura = int(instruccion_elem.text)
            instrucciones.insertar_fin(Instruccion(nombre_dron, altura))

        mensajes.insertar_fin(Mensaje(nombre_mensaje, sistema_drones, instrucciones))

    return drones, sistemas_drones, mensajes



class App:
    def __init__(self, master):
        self.drones = ListaEnlazada()
        self.sistemas_drones = ListaEnlazada()
        self.mensajes = ListaEnlazada()

        self.load_xml_btn = tk.Button(master, text='Cargar XML', command=self.cargar_xml)
        self.load_xml_btn.pack(pady=5)

        self.generate_instructions_btn = tk.Button(master, text='Generar Instrucciones', command=self.generar_instrucciones)
        self.generate_instructions_btn.pack(pady=5)

    def cargar_xml(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filepath:
            self.drones, self.sistemas_drones, self.mensajes = cargar_datos(filepath)  
            messagebox.showinfo("Carga exitosa", "Los datos se han cargado exitosamente")

    def mostrar_instrucciones_generadas(self, instrucciones_generadas):
        print("Instrucciones Generadas:")
        actual = instrucciones_generadas.inicio
        while actual:
            instruccion = actual.dato
            print(f"Dron {instruccion.dron} a {instruccion.altura} metros")
            actual = actual.siguiente

    def generar_instrucciones(self):
        instrucciones_generadas = self.generar_instrucciones_helper(self.drones, self.sistemas_drones, self.mensajes)
        self.mostrar_instrucciones_generadas(instrucciones_generadas)
        return instrucciones_generadas
    
    def generar_instrucciones_helper(self, drones, sistemas_drones, mensajes):
        instrucciones_generadas = ListaEnlazada()

        # Iterar a través de los mensajes
        actual = mensajes.inicio
        while actual:
            mensaje = actual.dato
            sistema_drones = None

            # Encontrar el sistema de drones asociado al mensaje
            sistema_actual = sistemas_drones.inicio
            while sistema_actual:
                if sistema_actual.dato.nombre == mensaje.sistema_drones:
                    sistema_drones = sistema_actual.dato
                    break
                sistema_actual = sistema_actual.siguiente

            if sistema_drones is None:
                # Manejar el caso donde el sistema de drones no fue encontrado
                print(f"Sistema de drones '{mensaje.sistema_drones}' no encontrado.")
            else:
                instruccion_actual = mensaje.instrucciones.inicio
                while instruccion_actual:
                    instruccion = instruccion_actual.dato
                    dron_actual = sistema_drones.drones.inicio

                    # Encontrar el dron asociado a la instrucción
                    while dron_actual:
                        if dron_actual.dato.nombre == instruccion.dron:
                            dron = dron_actual.dato
                            break
                        dron_actual = dron_actual.siguiente

                    if dron is None:
                        # Manejar el caso donde el dron no fue encontrado
                        print(f"Dron '{instruccion.dron}' no encontrado en el sistema '{sistema_drones.nombre}'.")
                    else:
                        # Encontrar la altura asociada a la letra de la instrucción
                        altura_letra = None
                        altura_actual = dron.alturas.inicio
                        while altura_actual:
                            if altura_actual.dato.letra == dron.caracter:
                                altura_letra = altura_actual.dato.altura
                                break
                            altura_actual = altura_actual.siguiente

                        if altura_letra is None:
                            # Manejar el caso donde la altura de la letra no fue encontrada
                            print(f"Altura de letra '{dron.caracter}' no encontrada para el dron '{dron.nombre}'.")
                        else:
                            # Calcular la altura final
                            altura_final = altura_letra + instruccion.altura

                            # Generar una nueva instrucción
                            nueva_instruccion = Instruccion(instruccion.dron, altura_final)

                            # Agregar la instrucción a la lista de instrucciones generadas
                            instrucciones_generadas.insertar_fin(nueva_instruccion)

                    instruccion_actual = instruccion_actual.siguiente

            actual = actual.siguiente

        return instrucciones_generadas




if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

