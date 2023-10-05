import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import filedialog
from tkinter import ttk
import graphviz
import tkinter.messagebox as messagebox
import os
import tkinter.simpledialog as simpledialog
from Nodo import Nodo
from ListaEnlazada import ListaEnlazada
from Dron import Dron
from SistemaDrones import SistemaDrones
from Mensaje import Mensaje
from Instruccion import Instruccion

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
        self.add_dron_btn.pack_forget() 

        archivo_menu = ttk.Combobox(self.navbar, values=["Sistema de Drones", "Mensajes", "Instrucciones"], style="Navbar.TCombobox")
        archivo_menu.set("Archivo")
        archivo_menu.pack(side=tk.LEFT, padx=10)
        archivo_menu.bind("<<ComboboxSelected>>", self.menu)

        self.generate_xml_btn = tk.Button(self.navbar, text='Generar XML', command=self.generar_xml)
        self.generate_xml_btn.pack(side='left', padx=10)

        self.help_btn = tk.Button(self.navbar, text='Ayuda', command=self.ayuda)
        self.help_btn.pack(side='left', padx=10)

        self.exit_btn = tk.Button(self.navbar, text='Salir', command=master.quit)
        self.exit_btn.pack(side='left', padx=10)

        self.graph_label = tk.Label(master, text='Aquí se mostrarán las gráficas', font=('Arial', 14))
        self.graph_label.pack(pady=20)

        self.add_dron_entry.pack_forget()
        self.add_dron_btn.pack_forget()


    def mostrar_agregar_dron(self):
        self.add_dron_entry.pack(side='left', padx=10)
        self.add_dron_btn.pack(side='left', padx=10)
        self.new_btn.config(command=self.ocultar_agregar_dron)
        self.new_btn.config(text='Cancelar')

    def ocultar_agregar_dron(self):
        self.add_dron_entry.pack_forget()
        self.add_dron_btn.pack_forget()
        self.new_btn.config(command=self.mostrar_agregar_dron)
        self.new_btn.config(text='Nuevo')

    def cargar_xml(self):
        filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filepath:
            self.drones, self.sistemas_drones, self.mensajes = cargar_datos(filepath)
            messagebox.showinfo("Carga exitosa", "Los datos se han cargado exitosamente")

    def generar_xml(self):
        root = ET.Element("respuesta")
        lista_mensajes = ET.SubElement(root, "listaMensajes")

        for mensaje in self.mensajes.obtener_mensajes():
            mensaje_elem = ET.SubElement(lista_mensajes, "mensaje", nombre=mensaje.nombre)
            sistema_drones_elem = ET.SubElement(mensaje_elem, "sistemaDrones")
            sistema_drones_elem.text = mensaje.sistema_drones

            tiempo_optimo_elem = ET.SubElement(mensaje_elem, "tiempoOptimo")
            tiempo_optimo_elem.text = str(self.tiempo_optimo(mensaje))  

            mensaje_recibido_elem = ET.SubElement(mensaje_elem, "mensajeRecibido")

            instrucciones_elem = ET.SubElement(mensaje_elem, "instrucciones")

            for instruccion in mensaje.instrucciones:
                tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo", valor=str(instruccion.altura))
                acciones_elem = ET.SubElement(tiempo_elem, "acciones")

                dron_elem = ET.SubElement(acciones_elem, "dron", nombre=instruccion.dron)

        ET.indent(root, space="  ")

        tree = ET.ElementTree(root)
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])

        if file_path:
            tree.write(file_path, xml_declaration=True, encoding="utf-8")
            messagebox.showinfo("XML Generado", f"El archivo XML ha sido generado correctamente en {file_path}")

    def ayuda(self):
        nombre = "Rodrigo Sebastian Castro Aguilar"
        carne = "202204496"
        curso = "Introduccion a la Programacion y Computacion 2"
        seccion = "A"
        mensaje = f"Nombre: {nombre}\nCarné: {carne}\nCurso: {curso}\nSección: {seccion}"
        messagebox.showinfo("Datos del Estudiante", mensaje)

    def listar_drones(self):
        nombres_drones = [dron.nombre for dron in self.drones]
        drones_ordenados = sorted(nombres_drones)
        messagebox.showinfo("Drones Ordenados", "\n".join(drones_ordenados))

    def listar_mensajes(self):
        nombres_mensajes = [mensaje.nombre for mensaje in self.mensajes.obtener_mensajes()]
        messagebox.showinfo("Mensajes", "\n".join(nombres_mensajes))

    def agregar_dron(self):
        nombre_dron = self.add_dron_entry.get()

        dron_existente = any(dron.nombre == nombre_dron for dron in self.drones.obtener_drones())

        if not dron_existente:
            nuevo_dron = Dron(nombre_dron)
            self.drones.insertar_fin(nuevo_dron)
            messagebox.showinfo("Dron agregado", f"Se ha agregado el dron '{nombre_dron}'")
        else:
            messagebox.showerror("Error", f"El dron '{nombre_dron}' ya existe")

    def menu(self, event):
        option = event.widget.get()
        if option == "Sistema de Drones":
            self.mostrar_sistemas_drones()
        elif option == "Mensajes":
            mensaje_elegido = self.prompt_choice("Selecciona un mensaje:", [mensaje.nombre for mensaje in self.mensajes.obtener_mensajes()])
            if mensaje_elegido:
                self.mostrar_instrucciones(mensaje_elegido)
        elif option == "Instrucciones":
            mensaje_elegido = self.prompt_choice("Selecciona un mensaje:", [mensaje.nombre for mensaje in self.mensajes.obtener_mensajes()])
            if mensaje_elegido:
                        self.generar_instrucciones( mensaje_elegido)
            else:
                messagebox.showerror("Error", "No se seleccionó un mensaje.")

    def mostrar_sistemas_drones(self):
        sistemas_drones_nombres = [sistema.nombre for sistema in self.sistemas_drones]
        selected_sistema = self.prompt_choice("Selecciona un sistema de drones:", sistemas_drones_nombres)
        if selected_sistema:
            sistema_drones = next((sistema for sistema in self.sistemas_drones if sistema.nombre == selected_sistema), None)
            if sistema_drones:
                self.generar_grafica_sistema_drones(sistema_drones)
            else:
                messagebox.showerror("Error", "No se encontró el sistema de drones seleccionado.")

    def mostrar_instrucciones(self, nombre_mensaje):
        mensaje = next((mensaje for mensaje in self.mensajes.obtener_mensajes() if mensaje.nombre == nombre_mensaje), None)
        if mensaje:
            instrucciones = mensaje.instrucciones
            tabla = "Instrucciones:\n"
            for instruccion in instrucciones:
                tabla += f"{instruccion.dron},{instruccion.altura}\n"
            messagebox.showinfo("Instrucciones del Mensaje", tabla)
        else:
            messagebox.showerror("Error", "No se encontró el mensaje seleccionado.")

    def prompt_choice(self, mensaje, opciones):
        """Muestra un cuadro de diálogo para que el usuario elija una opción."""
        return simpledialog.askstring("Selección", mensaje, initialvalue=opciones[0])

    def generar_grafica_sistema_drones(self, sistema_drones):
        dot_string = 'digraph G {\n'
        dot_string += sistema_drones.to_dot()
        dot_string += "}\n"
        with open("sistema_drones.dot", "w") as archivo:
            archivo.write(dot_string)
        os.system("dot -Tpng sistema_drones.dot -o sistema_drones.png")
        img = tk.PhotoImage(file='sistema_drones.png')
        self.graph_label.config(image=img)
        self.graph_label.image = img
    
    def generar_instrucciones(self, nombre_mensaje):
        mensaje = next((mensaje for mensaje in self.mensajes.obtener_mensajes() if mensaje.nombre == nombre_mensaje), None)
        if mensaje:
            lista_instrucciones = mensaje.instrucciones
            sistema_drones = next((sds for sds in self.sistemas_drones if sds.nombre == mensaje.sistema_drones), None)
            if sistema_drones:
                tiempo_total = 0
                for instruccion in lista_instrucciones:
                    dron = next((dron for dron in sistema_drones.drones if dron.nombre == instruccion.dron), None)
                    if dron:
                        dron.agregar_instruccion(instruccion.altura)
                        
                        tiempo_total += self.ejecutar_instruccion(dron, instruccion.altura,instruccion.dron)
                    else:
                        messagebox.showerror("Error", f"No se encontró el dron '{instruccion.dron}' en el sistema de drones.")
                        return
                messagebox.showinfo("Instrucciones Completadas", f"Todas las instrucciones se han completado en {tiempo_total} segundos.")
            else:
                messagebox.showerror("Error", "No se encontró el sistema de drones especificado en el mensaje.")
        else:
            messagebox.showerror("Error", "No se encontró el mensaje especificado.")


    def tiempo_optimo(self, mensaje):
        tiempo_optimo = 0
        timepo_actual = self.drones.inicio.dato.tiempo
        for instruccion in mensaje.instrucciones:
            dron = next((dron for dron in self.drones.obtener_drones() if dron.nombre == instruccion.dron), None)
            if dron:
                droninstru = instruccion.dron
                dron.tiempo += self.ejecutar_instruccion(dron, instruccion.altura,droninstru)
        for time in self.drones:
            tiempo_optimo = time.tiempo
            if tiempo_optimo > timepo_actual:
                timepo_actual = tiempo_optimo
        print(timepo_actual)
        return timepo_actual

    def ejecutar_instruccion(self, dron, altura_objetivo, dron_instruccion):
        tiempo = 0
        while dron.naltura != altura_objetivo:
            if dron.naltura < altura_objetivo:
                dron.naltura += 1
                tiempo += 1
                dron.movimientos.insertar_fin("subir")
                print(f"{dron.nombre} sube a la altura {dron.naltura}")
            elif dron.naltura > altura_objetivo:
                dron.naltura -= 1
                tiempo += 1
                dron.movimientos.insertar_fin("bajar")
                print(f"{dron.nombre} baja a la altura {dron.naltura}")
        
        if dron.naltura == altura_objetivo and dron.nombre == dron_instruccion:
            tiempo += 1
            dron.movimientos.insertar_fin("EmitirLuz")
            print(f"{dron.nombre} emitit la luz a la altura {dron.naltura}")
        elif dron.naltura == altura_objetivo:
            print(f"{dron.nombre} Esperar {dron.naltura}")
            tiempo +=1
        return tiempo

def cargar_datos(filepath):
    drones = ListaEnlazada()
    sistemas_drones = ListaEnlazada()
    mensajes = ListaEnlazada()

    tree = ET.parse(filepath)
    root = tree.getroot()

    for dron_elem in root.findall('.//listaDrones/dron'):
        nombre_dron = dron_elem.text
        nuevo_dron = Dron(nombre_dron)
        drones.insertar_fin(nuevo_dron)

    for sistema_elem in root.findall('.//listaSistemasDrones/sistemaDrones'):
        nombre_sistema = sistema_elem.get('nombre')
        altura_maxima = int(sistema_elem.find('alturaMaxima').text)
        cantidad_drones = int(sistema_elem.find('cantidadDrones').text)
        drones_sistema = ListaEnlazada()

        for contenido_elem in sistema_elem.findall('.//contenido'):
            nombre_dron = contenido_elem.find('dron').text
            alturas = ListaEnlazada()
            for altura_elem in contenido_elem.findall('.//alturas/altura'):
                valor_altura = int(altura_elem.get('valor'))
                letra = altura_elem.text
                alturas.insertar_fin((valor_altura, letra))
            dron = Dron(nombre_dron, alturas)
            drones_sistema.insertar_fin(dron)

        sistema_drones = SistemaDrones(nombre_sistema, altura_maxima, cantidad_drones, drones_sistema)
        sistemas_drones.insertar_fin(sistema_drones)

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
