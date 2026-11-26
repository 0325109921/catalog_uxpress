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

    @staticmethod
    def encabezado():
        return f"| {'Num':<5} | {'Fecha':<19} | {'Cant.':<5} | {'Subtotal':<11} | {'IVA':<11} | {'Total':<11} | {'Cat.':<5} | {'Vend.':<5} | {'Edo.':<5} | {'Ent.':<5} | {'Cli.':<5} |"

    def __str__ (self):
        entrega = self._entrega if self._entrega is not None else "-"
        return f"| {self._numPedido:<5} | {str(self._fecha):<19} | {self._cantArticulos:<5} | ${self._subtotal:<10.2f} | ${self._IVA:<10.2f} | ${self._total:<10.2f} | {self._catalogo:<5} | {self._vendedor:<5} | {self._estadoPedido:<5} | {entrega:<5} | {self._cliente:<5} |"
