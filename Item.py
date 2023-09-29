from Nodo import Nodo

class Item(Nodo):
    def __init__(self, row, col, text):
        super().__init__()
        self.row = row
        self.col = col
        self.text = text
        
    
    def imprimir(self):
        print(f'     Row: {self.row}, Col: {self.col}, Text: {self.text}')