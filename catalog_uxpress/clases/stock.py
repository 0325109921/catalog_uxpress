class Stock:
    def __init__ (self, sucursal:str, producto:str, cantStock:int):
        self._sucursal=sucursal
        self._producto=producto
        self._cantStock=cantStock

    def __str__ (self):
        return f"| {self._sucursal:<5} | {self._producto:<20} | {self._cantStock:<5} |"