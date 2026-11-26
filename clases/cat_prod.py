class Cat_Prod:
    def __init__ (self, catalogo, producto, precio:float):
        self._catalogo = catalogo
        self._producto = producto
        self._precio = precio

    @staticmethod
    def encabezado():
        return f"| {'Cat.':<5} | {'SKU':<20} | {'Precio':<10} |"

    def __str__ (self):
        return f"| {self._catalogo:<5} | {self._producto:<20} | {self._precio:<10.2f} |"