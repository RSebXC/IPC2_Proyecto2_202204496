from Nodo import Nodo
from ListaSimple import ListaSimple

class Elemento(Nodo):
    def __init__(self, nombre, id, cols, rows):
        super().__init__()
        self.nombre = nombre
        self.id = id
        self.cols = cols
        self.rows = rows
        self.items = ListaSimple()
        
    def imprimir(self):
        return f'Elemento --- Nombre: {self.nombre}, ID: {self.id}\n'
        
        
    def to_dot(self):
        # Nodo principal del elemento
        nodo_id = f'elemento_{self.id}'
        cadena = f'"{nodo_id}" [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\n'

        # Añadiendo encabezados de columnas
        cadena += '<TR><TD>Titulo</TD>'
        for c in range(1, self.cols + 1):
            cadena += f'<TD>{c}</TD>'
        cadena += '</TR>\n'

        # Añadiendo filas con índices y elementos
        for r in range(1, self.rows + 1):
            cadena += f'<TR><TD>{r}</TD>'
            for c in range(1, self.cols + 1):
                item = self.get_item(r, c)
                cadena += f'<TD>{item.text if item else "-"}</TD>'
            cadena += '</TR>\n'

        # Cerrando etiqueta de tabla y nodo
        cadena += '</TABLE>>, shape=plain];\n'

        return cadena


        
        
    def showItemsConsole(self):
        for r in range(1, self.rows + 1):
            for c in range (1, self.cols + 1):
                item = self.get_item(r, c)
                if item:
                    print(item.text, end="\t")
                else:
                    print("-", end="\t")
            print()
            
            
    def to_xml(self): 
        cadena = f'<elemento nombre="{self.nombre}" id="{self.id}" cols="{self.cols}" rows="{self.rows}">\n'
        actual = self.items.inicio
        while actual:
            cadena += f'\t<item row="{actual.row}" col="{actual.col}">{actual.text}</item>\n'
            actual = actual.siguiente
        cadena += "</elemento>\n"
        return cadena
    
    
    def get_item(self, row, col):
        actual = self.items.inicio
        while actual: 
            if actual.row == row and actual.col == col:
                return actual
            actual = actual.siguiente
        return None