class Stock:
    def __init__ (self, sucursal:str, producto:str, cantStock:int, nombreProducto:str = None):
        self._sucursal=sucursal
        self._producto=producto
        self._cantStock=cantStock
        self._nombreProducto=nombreProducto # solo viene cuando el DAO hace JOIN con producto

    @staticmethod
    def encabezado():
        return f"| {'Suc.':<5} | {'SKU':<10} | {'Producto':<40} | {'Stock':<5} |"

    def __str__ (self):
        nombre = self._nombreProducto if self._nombreProducto else ""
        return f"| {self._sucursal:<5} | {self._producto:<10} | {nombre:<40} | {self._cantStock:<5} |"
