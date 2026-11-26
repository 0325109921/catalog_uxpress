import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.estado_entrega import Estado_Entrega

class Estado_EntregaDAO:
    def __init__(self,conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, estado_entrega: Estado_Entrega):
        consulta = "INSERT INTO estado_entrega (codigo, descripcion) VALUES( %s, %s)"
        self._cursor.execute(consulta, (estado_entrega._codigo, estado_entrega._descripcion))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT codigo, descripcion FROM estado_entrega")
        return[Estado_Entrega(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_descripcion(self, codigo, nueva_descripcion):
        consulta = "UPDATE estado_entrega SET descripcion = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (nueva_descripcion, codigo))
        self._conexion.commit()

    def eliminar(self, codigo):
        consulta = "DELETE FROM estado_entrega WHERE codigo=%s"
        self._cursor.execute(consulta, (codigo,))
        self._conexion.commit()
