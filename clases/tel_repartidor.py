class Tel_Repartidor:
    def __init__(self, repartidor: int, numero: int, numTel: str):
            self._repartidor = repartidor
            self._numero = numero
            self._numTel = numTel
    
    @staticmethod
    def encabezado():
        return f"| {'Rep.':<5} | {'No.':<5} | {'Telefono':<15} |"

    def __str__ (self):
        return f"| {self._repartidor:<5} | {self._numero:<5} | {self._numTel:<15} |"