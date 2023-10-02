import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox, filedialog
from graphviz import Digraph
from tkinter import PhotoImage
import os

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.inicio = None
    
    def insertar_fin(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo_nodo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_lista(self):
        lista = ""
        actual = self.inicio
        while actual:
            lista += f"{actual.dato}, "
            actual = actual.siguiente
        return lista.rstrip(", ")
    
    def __iter__(self):
        actual = self.inicio
        while actual:
            yield actual  # Utiliza 'yield' para generar los nodos uno por uno
            actual = actual.siguiente

    def obtener_mensajes(self):
        actual = self.inicio
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def obtener_drones(self):
        actual = self.inicio
        while actual:
            yield actual.dato
            actual = actual.siguiente


class Dron:
    def __init__(self, nombre, alturas=None):
        self.nombre = nombre
        self.alturas = alturas or ListaEnlazada()


class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones, drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.drones = drones


class Mensaje:
    def __init__(self, nombre, sistema_drones, instrucciones):
        self.nombre = nombre
        self.sistema_drones = sistema_drones
        self.instrucciones = instrucciones


class Instruccion:
    def __init__(self, dron, altura):
        self.dron = dron
        self.altura = altura


class App:
    def __init__(self, master):
        # Barra de navegación
        self.navbar = tk.Frame(master)
        self.navbar.pack(fill='x', pady=10)

        self.load_xml_btn = tk.Button(self.navbar, text='Cargar XML', command=self.cargar_xml)
        self.load_xml_btn.pack(side='left', padx=10, pady=5)

        self.list_drones_btn = tk.Button(self.navbar, text='Listar Drones', command=self.listar_drones)
        self.list_drones_btn.pack(side='left', padx=10, pady=5)

        self.list_mensajes_btn = tk.Button(self.navbar, text='Listar Mensajes', command=self.listar_mensajes)
        self.list_mensajes_btn.pack(side='left', padx=10, pady=5)

        self.new_btn = tk.Button(self.navbar, text='Nuevo', command=self.mostrar_agregar_dron)
        self.new_btn.pack(side='left', padx=10)

        self.add_dron_entry = tk.Entry(self.navbar, width=20)
        self.add_dron_entry.pack(side='left', padx=10)
        self.add_dron_btn = tk.Button(self.navbar, text='Agregar Dron', command=self.agregar_dron)
        self.add_dron_btn.pack(side='left', padx=10)
        self.add_dron_btn.pack_forget()  # Ocultar el botón por defecto

        opciones = ['Sistema de Drones', 'Mensajes', 'Instrucciones']
        self.option_var = tk.StringVar()
        self.option_var.set(opciones[0])  # Valor predeterminado
        self.option_menu = tk.OptionMenu(self.navbar, self.option_var, *opciones)
        self.option_menu.pack(side='left', padx=10)

        self.sistema_drones_var = tk.StringVar()
        self.sistema_drones_combobox = tk.OptionMenu(self.navbar, self.sistema_drones_var, '')
        self.sistema_drones_combobox.pack(side='left', padx=10)
        self.sistema_drones_var.set('Seleccionar Sistema de Drones')


        self.generate_xml_btn = tk.Button(self.navbar, text='Generar XML', command=self.generar_xml)
        self.generate_xml_btn.pack(side='left', padx=10)

        self.help_btn = tk.Button(self.navbar, text='Ayuda', command=self.mostrar_ayuda)
        self.help_btn.pack(side='left', padx=10)

        self.exit_btn = tk.Button(self.navbar, text='Salir', command=master.quit)
        self.exit_btn.pack(side='left', padx=10)

        self.graph_label = tk.Label(master, text='Aquí se mostrarán las gráficas', font=('Arial', 14))
        self.graph_label.pack(pady=20)

        self.add_dron_entry.pack_forget()
        self.add_dron_btn.pack_forget()


    def mostrar_agregar_dron(self):
        # Mostrar el botón de agregar dron y el entry correspondiente
        self.add_dron_entry.pack(side='left', padx=10)
        self.add_dron_btn.pack(side='left', padx=10)
        self.new_btn.config(command=self.ocultar_agregar_dron)  # Cambiar la función del botón a ocultar_agregar_dron
        self.new_btn.config(text='Cancelar')

    def ocultar_agregar_dron(self):
        # Ocultar el botón de agregar dron y el entry correspondiente
        self.add_dron_entry.pack_forget()
        self.add_dron_btn.pack_forget()
        self.new_btn.config(command=self.mostrar_agregar_dron)  # Cambiar la función del botón a mostrar_agregar_dron
        self.new_btn.config(text='Nuevo')

    def cargar_xml(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filepath:
            self.drones, self.sistemas_drones, self.mensajes = cargar_datos(filepath)
            messagebox.showinfo("Carga exitosa", "Los datos se han cargado exitosamente")
            self.actualizar_combo_box_sistemas_drones()

    def actualizar_combo_box_sistemas_drones(self):
        nombres_sistemas_drones = [sistema_dron.nombre for sistema_dron in self.sistemas_drones.obtener_drones()]
        menu = self.sistema_drones_combobox['menu']
        menu.delete(0, 'end')  # Limpiar las opciones anteriores del combo box
        for nombre_sistema in nombres_sistemas_drones:
            menu.add_command(label=nombre_sistema, command=tk._setit(self.sistema_drones_var, nombre_sistema))

    def mostrar_grafica_sistema(self):
        selected_system = self.sistema_drones_var.get()
        sistema_drones_seleccionado = next((sistema_dron for sistema_dron in self.sistemas_drones.obtener_drones() if sistema_dron.nombre == selected_system), None)

        if sistema_drones_seleccionado:
            dot_file_path = self.generar_dot_file(sistema_drones_seleccionado)
            self.mostrar_grafica(dot_file_path)
        else:
            messagebox.showerror("Error", "No se encontró el sistema de drones seleccionado.")


    def mostrar_grafica(self, dot_file_path):
        try:
            # Genera la imagen desde el archivo .dot
            dot_image_path = dot_file_path.replace('.dot', '.png')
            dot_command = f'dot -Tpng {dot_file_path} -o {dot_image_path}'
            os.system(dot_command)
            
            # Muestra la imagen en el label
            imagen = PhotoImage(file=dot_image_path)
            self.graph_label.config(image=imagen)
            self.graph_label.image = imagen  # Mantén una referencia para evitar que la imagen se destruya
            self.graph_label.update()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la gráfica: {str(e)}")


    def generar_xml(self):
        # Lógica para generar XML
        pass

    def mostrar_ayuda(self):
        # Lógica para mostrar ayuda
        pass

    def listar_drones(self):
        # Crear una lista de nombres de drones
        nombres_drones = [dron.dato.nombre for dron in self.drones]
        
        # Ordenar la lista de nombres de drones
        drones_ordenados = sorted(nombres_drones)
        
        # Mostrar los drones ordenados
        messagebox.showinfo("Drones Ordenados", "\n".join(drones_ordenados))

    def generar_dot_file(self, sistema_drones):
        dot = Digraph(comment='Drones por Altura')
        dot.attr(rankdir='LR')  # Dirección de izquierda a derecha

        for dron in sistema_drones.drones.obtener_drones():
            dot.node(dron.nombre, dron.nombre)  # Cada dron es un nodo

            # Conectar el dron con sus alturas
            for altura, letra in dron.alturas.obtener_lista():
                dot.node(f'Altura{altura}', f'Altura {altura}: {letra}')
                dot.edge(dron.nombre, f'Altura{altura}')

        dot_file_path = 'drones_por_altura'
        try:
            dot.render(dot_file_path, format='png', cleanup=True)  # Renderizar como imagen PNG
            print("Archivo .dot generado exitosamente en:", dot_file_path)
        except Exception as e:
            print("Error al generar el archivo .dot:", str(e))
            dot_file_path = None  # Establecer dot_file_path como None en caso de error

        return dot_file_path




    def listar_mensajes(self):
        # Crear una lista de nombres de los mensajes
        nombres_mensajes = [mensaje.nombre for mensaje in self.mensajes.obtener_mensajes()]
        messagebox.showinfo("Mensajes", "\n".join(nombres_mensajes))


    def agregar_dron(self):
        nombre_dron = self.add_dron_entry.get()

        # Verificar si el dron ya existe
        dron_existente = any(dron.nombre == nombre_dron for dron in self.drones.obtener_drones())

        if not dron_existente:
            nuevo_dron = Dron(nombre_dron)
            self.drones.insertar_fin(nuevo_dron)
            messagebox.showinfo("Dron agregado", f"Se ha agregado el dron '{nombre_dron}'")
        else:
            messagebox.showerror("Error", f"El dron '{nombre_dron}' ya existe")



def cargar_datos(filepath):
    drones = ListaEnlazada()
    sistemas_drones = ListaEnlazada()
    mensajes = ListaEnlazada()
    print(filepath)

    tree = ET.parse(filepath)
    root = tree.getroot()

    # Cargar drones
    for dron_elem in root.findall('.//listaDrones/dron'):
        nombre_dron = dron_elem.text
        nuevo_dron = Dron(nombre_dron)
        drones.insertar_fin(nuevo_dron)

    # Cargar sistemas de drones
    for sistema_elem in root.findall('.//listaSistemasDrones/sistemaDrones'):
        nombre_sistema = sistema_elem.get('nombre')
        altura_maxima = int(sistema_elem.find('alturaMaxima').text)
        cantidad_drones = int(sistema_elem.find('cantidadDrones').text)
        drones_sistema = ListaEnlazada()

        for dron_elem in sistema_elem.findall('.//contenido/dron'):
            nombre_dron = dron_elem.text
            alturas = ListaEnlazada()
            for altura_elem in dron_elem.findall('.//alturas/altura'):
                valor_altura = int(altura_elem.get('valor'))
                letra = altura_elem.text
                alturas.insertar_fin((valor_altura, letra))
            dron = Dron(nombre_dron, alturas)
            drones_sistema.insertar_fin(dron)

        sistema_drones = SistemaDrones(nombre_sistema, altura_maxima, cantidad_drones, drones_sistema)
        sistemas_drones.insertar_fin(sistema_drones)

    # Cargar mensajes
    for mensaje_elem in root.findall('.//listaMensajes/Mensaje'):
        nombre_mensaje = mensaje_elem.get('nombre')
        sistema_drones_nombre = mensaje_elem.find('sistemaDrones').text
        instrucciones = ListaEnlazada()

        for instruccion_elem in mensaje_elem.findall('.//instrucciones/instruccion'):
            nombre_dron = instruccion_elem.get('dron')
            altura = int(instruccion_elem.text)
            instruccion = Instruccion(nombre_dron, altura)
            instrucciones.insertar_fin(instruccion)

        mensaje = Mensaje(nombre_mensaje, sistema_drones_nombre, instrucciones)
        mensajes.insertar_fin(mensaje)

    return drones, sistemas_drones, mensajes



if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()