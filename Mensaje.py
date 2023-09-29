from ListaSimple import ListaSimple


class Mensaje:
    def __init__(self, nombre, sistema_drones):
        self.nombre = nombre
        self.sistema_drones = sistema_drones
        self.instrucciones = ListaSimple()