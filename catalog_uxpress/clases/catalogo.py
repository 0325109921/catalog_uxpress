class Catalogo:
    def __init__ (self, numCatalogo:int, nombre:str, vigenciaInicio:str, vigenciaFin:str, sucursal)->None:
        self._numCatalogo = numCatalogo
        self._nombre = nombre
        self._vigenciaInicio = vigenciaInicio
        self._vigenciaFin = vigenciaFin
        self._sucursal = sucursal

    def __str__(self):
        return f"| {self._numCatalogo:<5} | {self._nombre:<100} | {str(self._vigenciaInicio):<10} | {str(self._vigenciaFin):<10} | {self._sucursal} |"