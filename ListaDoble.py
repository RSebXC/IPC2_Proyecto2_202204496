class ListaDoble():
    def __init__(self):
        self.inicio = None
        self.fin = None
        
    def inicializar(self):
        self.inicio = None
        self.fin = None

    def mostrar(self):
        actual = self.inicio
        aux = ''
        while actual != None:
            aux += actual.imprimir()
            actual = actual.siguiente
        return aux

    def mostrar_inverso(self):
        actual = self.fin
        while actual != None:
            actual.imprimir()
            actual = actual.anterior
        print("--------------")

    def insertarFin(self, objeto):
        if self.inicio == None:
            self.inicio = objeto
            self.fin = objeto
        else:
            self.fin.siguiente = objeto
            objeto.anterior = self.fin
            self.fin = objeto

    def insertarInicio(self, objeto):
        if self.inicio == None:
            self.inicio = objeto
            self.fin = objeto
        else:
            self.inicio.anterior = objeto
            objeto.siguiente = self.inicio
            self.inicio = objeto
            
    def insertarOrdenadoPorId(self, objeto):
        if self.inicio == None:
            self.inicio = objeto
            self.fin = objeto
        else:
            if objeto.id < self.inicio.id:
                self.insertarInicio(objeto)
            elif objeto.id > self.fin.id:
                self.insertarFin(objeto)
            else:
                aux = self.inicio
                while aux != None:
                    if objeto.id < aux.id:
                        objeto.siguiente = aux
                        objeto.anterior = aux.anterior
                        aux.anterior.siguiente = objeto
                        aux.anterior = objeto
                        break
                    aux = aux.siguiente
                    

    def eliminar(self, id):
        aux = self.inicio
        while aux != None:
            if aux.id == id:
                #si es el primero
                if aux.anterior == None:
                    self.inicio = aux.siguiente
                    self.inicio.anterior = None
                #si es el ultimo
                elif aux.siguiente == None:
                    self.fin = aux.anterior
                    self.fin.siguiente = None
                #si es uno intermedio
                else:
                    aux.anterior.siguiente = aux.siguiente
                    aux.siguiente.anterior = aux.anterior
                return True
            aux = aux.siguiente
        return False
    
    
    def actualizar (self, id, nuevo_nombre):
        #sin perder la referencia
        aux = self.inicio
        while aux != None:
            if aux.id == id:
                aux.nombre = nuevo_nombre
                return True
            aux = aux.siguiente
        return False
    
    
    def buscar_por_id(self, id):
        actual = self.inicio
        while actual:
            if actual.id == id:
                return actual
            actual = actual.siguiente
        return None
    
    
    def escribirXML(self):
        cadena = '<?xml version="1.0" encoding="UTF-8"?>\n'
        cadena += '<elementos>\n'
        actual = self.inicio
        while actual:
            aux = actual.to_xml()
            cadena += aux
            actual = actual.siguiente
        cadena += '</elementos>\n'
        with open("elementosNuevo.xml", "w") as archivo:
            archivo.write(cadena)
        print("¡Archivo XML generado!")