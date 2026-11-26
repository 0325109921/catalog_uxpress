class Vendedor:
    def __init__ (self, numEmpleado:int, nombrePila:str, primerApell:str, segundoApell:str, dirCalle:str, dirNumero:str, dirColonia:str, sucursal, activo:bool = True) -> None:
        self._numEmpleado = numEmpleado
        self._nombrePila = nombrePila
        self._primerApell = primerApell
        self._segundoApell = segundoApell
        self._dirCalle = dirCalle
        self._dirNumero = dirNumero
        self._dirColonia = dirColonia
        self._activo = activo
        self._sucursal = sucursal

    @staticmethod
    def encabezado() -> str:
        return f"| {'Num':<5} | {'Nombre':<40} | {'Primer apellido':<30} | {'Segundo apellido':<30} | {'Calle':<30} | {'Numero':<30} | {'Colonia':<30} | {'Estado':<9} | {'Suc.':<5} |"

    def __str__(self) -> str:
        segundo = self._segundoApell if self._segundoApell else "" # segundoApell puede ser NULL
        if self._activo == 1:
            activo = "Activo"
        else:
            activo="No activo"
        return f"| {self._numEmpleado:<5} | {self._nombrePila:<40} | {self._primerApell:<30} | {segundo:<30} | {self._dirCalle:<30} | {self._dirNumero:<30} | {self._dirColonia:<30} | {activo:<9} | {self._sucursal:<5} |"
