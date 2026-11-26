class Repartidor:
    def __init__(self, numRepartidor:int, nombrePila:str, primerApell:str, segundoApell:str, dirCalle:str, dirNumero:str, dirColonia:str, activo:bool = True) -> None:
        self._numRepartidor = numRepartidor
        self._nombrePila = nombrePila
        self._primerApell = primerApell
        self._segundoApell = segundoApell
        self._dirCalle = dirCalle
        self._dirNumero = dirNumero
        self._dirColonia = dirColonia
        self._activo = activo

    def __str__(self)->str:

        if self._activo == 1:
            activo = "Activo"
        else:
            activo = "No activo"

        return f"| {self._numRepartidor:<5} | {self._nombrePila:<40} | {self._primerApell:<30} | {self._segundoApell:<30} | {self._dirCalle:<30} | {self._dirNumero:<30} | {self._dirColonia:<30} | {activo:<9} |"
