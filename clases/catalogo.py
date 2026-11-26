class Catalogo:
    def __init__ (self, numCatalogo:int, nombre:str, vigenciaInicio:str, vigenciaFin:str, sucursal)->None:
        self._numCatalogo = numCatalogo
        self._nombre = nombre
        self._vigenciaInicio = vigenciaInicio
        self._vigenciaFin = vigenciaFin
        self._sucursal = sucursal

    @staticmethod
    def encabezado():
        return f"| {'Num':<5} | {'Nombre':<100} | {'Inicio':<10} | {'Fin':<10} | {'Suc.':<5} |"

    def __str__(self):
        fin = str(self._vigenciaFin) if self._vigenciaFin else "Sin fin" # vigenciaFin puede ser NULL
        return f"| {self._numCatalogo:<5} | {self._nombre:<100} | {str(self._vigenciaInicio):<10} | {fin:<10} | {self._sucursal:<5} |"