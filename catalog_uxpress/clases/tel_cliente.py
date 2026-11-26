class Tel_Cliente:
    def __init__(self, cliente: int, numero: int, numTel: str):
        self._cliente = cliente
        self._numero = numero
        self._numTel = numTel

    def __str__ (self):
        return f"| {self._cliente:<5} | {self._numero:<5} {self._numTel:<15} |"