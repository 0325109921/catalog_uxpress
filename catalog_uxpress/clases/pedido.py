class Pedido:
    def __init__ (self, numPedido:int, fecha:str, cantArticulos:int, subtotal:float, IVA:float, total:float, catalogo, vendedor, estadoPedido, entrega, cliente) -> None:
        self._numPedido = numPedido
        self._fecha = fecha
        self._cantArticulos = cantArticulos
        self._subtotal = subtotal
        self._IVA = IVA
        self._total = total
        self._catalogo = catalogo
        self._vendedor = vendedor
        self._estadoPedido = estadoPedido
        self._entrega = entrega
        self._cliente = cliente

    def __str__ (self):
        return f"| {self._numPedido:<5} | {str(self._fecha):<10} | {self._cantArticulos:<5} | ${self._subtotal:<10.2f} | ${self._IVA:<10.2f} | ${self._total:<10.2f} | {self._catalogo} | {self._vendedor} | {self._estadoPedido} | {self._entrega} | {self._cliente}"
