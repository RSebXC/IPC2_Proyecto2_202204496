from ListaEnlazada import ListaEnlazada


class Dron:
    def __init__(self, nombre, alturas=None):
        self.nombre = nombre
        self.alturas = alturas or ListaEnlazada()
        self.instrucciones = ListaEnlazada()
        self.naltura = 0
        self.instrccionactual = None
        self.movimientos = ListaEnlazada()
        self.tiempo = 0

    def agregar_altura(self, valor_altura, letra):
        self.alturas.insertar_fin((valor_altura, letra))

    def obtener_letra_para_altura(self, altura):
        return self.alturas.obtener_letra_para_altura(altura)
    def asignar (self):
        self.instruccionactual = self.instrucciones.inicio
    def realizar_instruccion(self):
        if self.instruccionactual:
            if int(self.instruccionactual.dato) == int(self.naltura):
                print("encender")
                
                self.instrccionactual = self.instrccionactual.siguiente
                return True
            elif int(self.instruccionactual.dato) > int(self.naltura):
                self.naltura += 1
                print("subir")
                return False
            return False
        return False
    
    def agregar_instruccion(self, altura_objetivo):
        self.instrucciones.insertar_fin(altura_objetivo)