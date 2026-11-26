class Pago:
    def __init__ (self, numTransaccion:int, concepto:str, fecha:str, monto:float, numeroPago:int, saldo:float, pedido, cliente) -> None:
        self._numTransaccion = numTransaccion
        self._concepto = concepto
        self._fecha = fecha
        self._monto = monto
        self._numeroPago = numeroPago
        self._saldo = saldo
        self._pedido = pedido
        self._cliente = cliente

    def __str__ (self):
        return f"| {self._numTransaccion:<5} | {self._concepto:<100} | {str(self._fecha):19} | {self._monto:<10.2f} | {self._numeroPago:<5} | {self._saldo:<10.2f} | {self._pedido} | {self._cliente} |"