import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.estado_pedido import Estado_Pedido

class Estado_PedidoDAO:
    def __init__(self,conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self,estado_pedido: Estado_Pedido):
        consulta = "INSERT INTO estado_pedido (codigo, descripcion) VALUES (%s, %s)"
        self._cursor.execute(consulta, (estado_pedido._codigo, estado_pedido._descripcion))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT codigo, descripcion FROM estado_pedido")
        return[Estado_Pedido(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_descripcion(self, codigo, nueva_descripcion):
        consulta = "UPDATE estado_pedido SET descripcion = %s WHERE codigo = %s"
        self._cursor.execute(consulta,(nueva_descripcion, codigo))
        self._conexion.commit()

    def eliminar(self, codigo):
        consulta = "DELETE FROM estado_pedido WHERE codigo = %s"
        self._cursor.execute(consulta,(codigo,))
        self._conexion.commit()