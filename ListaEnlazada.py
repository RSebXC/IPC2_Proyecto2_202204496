from Nodo import Nodo


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
            lista += f"{actual.dato.nombre}, "  # Accede al atributo 'nombre' del dato del nodo
            actual = actual.siguiente
        return lista.rstrip(", ")
    
    def __iter__(self):
        actual = self.inicio
        while actual:
            yield actual.dato  # Devuelve el dato del nodo, no el nodo
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

    def obtener_letra_para_altura(self, altura):
        actual = self.inicio
        while actual:
            if isinstance(actual.dato, tuple) and len(actual.dato) == 2:
                valor_altura, letra = actual.dato
                if valor_altura == altura:
                    return letra
            actual = actual.siguiente
        return ""