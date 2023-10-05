class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones, drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.drones = drones

    def obtener_letra_para_altura(self, altura):
        letra = ""
        for dron in self.drones:
            letra_o_numero = dron.alturas.obtener_letra_para_altura(altura)
            if letra_o_numero:
                letra = letra_o_numero
                break
        return letra

    def to_dot(self):
        dot_string = f'"{self.nombre}" [label=<<TABLE BORDER="1" CELLSPACING="0" CELLPADDING="8">'
        dot_string += f'<TR><TD colspan="{self.cantidad_drones + 1}">{self.nombre}</TD></TR>'
        dot_string += '<TR><TD>Altura</TD>'
        for dron in self.drones:
            dot_string += f'<TD>{dron.nombre}</TD>'
        dot_string += '</TR>'

        for altura in range(1, self.altura_maxima + 1):
            dot_string += f'<TR><TD>{altura}</TD>'
            for dron in self.drones:
                letra_o_numero = dron.alturas.obtener_letra_para_altura(altura)
                
                dot_string += f'<TD>{letra_o_numero}</TD>'  # Include the letter or number in the cell
            dot_string += '</TR>'

        dot_string += '</TABLE>>, shape=plaintext];'
        return dot_string