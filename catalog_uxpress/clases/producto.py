class Producto:
    def __init__ (self, SKU:str, nombre: str, descripcion:str) -> None:
        self._SKU = SKU
        self._nombre = nombre
        self._descripcion = descripcion

    def __str__(self)->str:
        return f"| {self._SKU:<10} | {self._nombre:<40} | {self._descripcion:<60} |"