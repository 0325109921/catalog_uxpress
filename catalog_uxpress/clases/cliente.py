class Cliente:
    def __init__ (self, numCliente:int, nombrePila:str, primerApell:str, segundoApell:str)->None:
        self._numCliente=numCliente
        self._nombrePila=nombrePila
        self._primerApell=primerApell
        self._segundoApell=segundoApell

    def __str__(self)->str:
        return f"| {self._numCliente:<5} | {self._nombrePila:<40} | {self._primerApell:<30} | {self._segundoApell:<30} |"
