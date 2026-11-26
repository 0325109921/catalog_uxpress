class Ped_Prod:
    def __init__ (self, pedido, catalogo, producto, cantidad:int, precioUnitario:float, importe:float):
        self._pedido = pedido
        self._catalogo = catalogo
        self._producto = producto
        self._cantidad = cantidad
        self._precioUnitario = precioUnitario
        self._importe = importe

    @staticmethod
    def encabezado():
        return f"| {'Ped.':<5} | {'Cat.':<5} | {'SKU':<20} | {'Cant.':<5} | {'Precio':<10} | {'Importe':<10} |"

    def __str__ (self):
        return f"| {self._pedido:<5} | {self._catalogo:<5} | {self._producto:<20} | {self._cantidad:<5} | {self._precioUnitario:<10.2f} | {self._importe:<10.2f} |"