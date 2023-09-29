from ListaSimple import ListaSimple


class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.drones = ListaSimple()