class Entrega:
    def __init__ (self, codigo:int, fechaEntrega:str, entregaConfirmada:bool, estadoEntrega:str, sucursal:str, repartidor:int, direccion:int) -> None:
        self._codigo = codigo
        self._fechaEntrega = fechaEntrega
        self._entregaConfirmada = entregaConfirmada
        self._estadoEntrega = estadoEntrega
        self._sucursal = sucursal
        self._repartidor = repartidor
        self._direccion = direccion

    @staticmethod
    def encabezado() -> str:
        return f"| {'Cod.':<5} | {'Fecha':<10} | {'Confirmacion':<21} | {'Edo.':<5} | {'Suc.':<5} | {'Rep.':<5} | {'Dir.':<5} |"

    def __str__(self) -> str:

        if self._entregaConfirmada == 1:
            entrega = "Entrega confirmada"
        else:
            entrega = "Entrega no confirmada"

        repartidor = self._repartidor if self._repartidor is not None else "-" # repartidor puede ser NULL

        return f"| {self._codigo:<5} | {str(self._fechaEntrega):<10} | {entrega:<21} | {self._estadoEntrega:<5} | {self._sucursal:<5} | {repartidor:<5} | {self._direccion:<5} |"