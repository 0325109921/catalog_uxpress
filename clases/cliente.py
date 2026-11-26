class Cliente:
    def __init__ (self, numCliente:int, nombrePila:str, primerApell:str, segundoApell:str)->None:
        self._numCliente=numCliente
        self._nombrePila=nombrePila
        self._primerApell=primerApell
        self._segundoApell=segundoApell

    @staticmethod
    def encabezado()->str:
        return f"| {'Num':<5} | {'Nombre':<40} | {'Primer apellido':<30} | {'Segundo apellido':<30} |"

    def __str__(self)->str:
        segundo = self._segundoApell if self._segundoApell else "" # segundoApell puede ser NULL
        return f"| {self._numCliente:<5} | {self._nombrePila:<40} | {self._primerApell:<30} | {segundo:<30} |"
