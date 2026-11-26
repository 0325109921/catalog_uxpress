class Estado_Entrega:
    def __init__ (self, codigo:str, descripcion:str) -> None:
        self._codigo = codigo
        self._descripcion = descripcion

    def __str__(self)->str:
        return f"| {self._codigo:<5} | {self._descripcion:<50} |"
