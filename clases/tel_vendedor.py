class Tel_Vendedor:
    def __init__(self, vendedor: int, numero: int, numTel: str):
            self._vendedor = vendedor
            self._numero = numero
            self._numTel = numTel
    
    @staticmethod
    def encabezado():
        return f"| {'Emp.':<5} | {'No.':<5} | {'Telefono':<15} |"

    def __str__ (self):
        return f"| {self._vendedor:<5} | {self._numero:<5} | {self._numTel:<15} |"