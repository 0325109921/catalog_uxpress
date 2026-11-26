class Direccion:
    def __init__ (self, numDireccion:int, calle:str, numero:str, colonia:str, cliente)->None:
        self._numDireccion=numDireccion
        self._calle=calle
        self._numero=numero
        self._colonia=colonia
        self._cliente=cliente

    def __str__(self):
        return f"| {self._numDireccion:<5} | {self._calle:<30} | {self._numero:<30} | {self._colonia:<30} | {self._cliente} |"
