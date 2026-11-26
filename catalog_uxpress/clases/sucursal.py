class Sucursal:
    def __init__ (self, codigoSucursal:str, nombre:str, dirCalle:str, dirNumero:str, dirColonia:str)->None:
        self._codigoSucursal = codigoSucursal
        self._nombre = nombre
        self._dirCalle = dirCalle
        self._dirNumero = dirNumero
        self._dirColonia = dirColonia

    def __str__(self)->str:
        return f"| {self._codigoSucursal:<5} | {self._nombre:<30} | {self._dirCalle:<30} | {self._dirNumero:<30} | {self._dirColonia:<30} |"



