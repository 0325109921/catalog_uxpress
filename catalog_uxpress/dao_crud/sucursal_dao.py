import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.sucursal import Sucursal

class SucursalDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, sucursal: Sucursal):
        consulta = "INSERT INTO sucursal (codigoSucursal, nombre, dirCalle, dirNumero, dirColonia) VALUES (%s, %s, %s, %s, %s)"
        self._cursor.execute(consulta, (sucursal._codigoSucursal, sucursal._nombre, sucursal._dirCalle, sucursal._dirNumero, sucursal._dirColonia))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT codigoSucursal, nombre, dirCalle, dirNumero, dirColonia FROM sucursal")
        return [Sucursal(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_nombre(self, codigoSucursal, nombre):
        consulta = "UPDATE sucursal SET nombre = %s WHERE codigoSucursal = %s"
        self._cursor.execute(consulta, (nombre, codigoSucursal))
        self._conexion.commit()

    def actualizar_dir_calle(self, codigoSucursal, dirCalle):
        consulta = "UPDATE sucursal SET dirCalle = %s WHERE codigoSucursal = %s"
        self._cursor.execute(consulta, (dirCalle, codigoSucursal))
        self._conexion.commit()

    def actualizar_dir_numero(self, codigoSucursal, dirNumero):
        consulta = "UPDATE sucursal SET dirNumero = %s WHERE codigoSucursal = %s"
        self._cursor.execute(consulta, (dirNumero, codigoSucursal))
        self._conexion.commit()

    def actualizar_dir_colonia(self, codigoSucursal, dirColonia):
            consulta = "UPDATE sucursal SET dirColonia = %s WHERE codigoSucursal = %s"
            self._cursor.execute(consulta, (dirColonia, codigoSucursal))
            self._conexion.commit()

    def eliminar(self, codigoSucursal):
        consulta = "DELETE FROM sucursal WHERE codigoSucursal = %s"
        self._cursor.execute(consulta, (codigoSucursal,))
        self._conexion.commit()