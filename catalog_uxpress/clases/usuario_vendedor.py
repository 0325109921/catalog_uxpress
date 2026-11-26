class Usuario_Vendedor:
    def __init__(self, usuario: int, vendedor: int) -> None:
        self._usuario = usuario
        self._vendedor = vendedor

    def __str__(self) -> str:
        return f"| {self._usuario:<5} | {self._vendedor:<5} |"