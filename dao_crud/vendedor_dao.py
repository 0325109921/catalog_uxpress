import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.vendedor import Vendedor

class VendedorDAO:
    def __init__(self,conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, vendedor: Vendedor):
        # numEmpleado es AUTO_INCREMENT: no se inserta, la BD lo asigna y se recupera con lastrowid
        consulta = "INSERT INTO vendedor (nombrePila, primerApell, segundoApell, dirCalle, dirNumero, dirColonia, sucursal, activo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (vendedor._nombrePila, vendedor._primerApell, vendedor._segundoApell, vendedor._dirCalle, vendedor._dirNumero, vendedor._dirColonia, vendedor._sucursal, vendedor._activo))
        self._conexion.commit()
        vendedor._numEmpleado = self._cursor.lastrowid
        return vendedor._numEmpleado

    def consultar_todas(self, sucursal=None):
        consulta = "SELECT numEmpleado, nombrePila, primerApell, segundoApell, dirCalle, dirNumero, dirColonia, sucursal, activo FROM vendedor"
        parametros = ()
        if sucursal is not None:      # filtra por sucursal cuando se indica una
            consulta += " WHERE sucursal = %s"
            parametros = (sucursal,)
        self._cursor.execute(consulta + " ORDER BY numEmpleado", parametros)
        return[Vendedor(*fila) for fila in self._cursor.fetchall()]

    def actualizar_nombre(self, numEmpleado, nombre):
        consulta = "UPDATE vendedor SET nombrePila = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (nombre, numEmpleado))
        self._conexion.commit()

    def actualizar_primer_apell(self, numEmpleado, primerApell):
        consulta = "UPDATE vendedor SET primerApell = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (primerApell, numEmpleado))
        self._conexion.commit()

    def actualizar_segundo_apell(self, numEmpleado, segundoApell):
        consulta = "UPDATE vendedor SET segundoApell = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (segundoApell, numEmpleado))
        self._conexion.commit()

    def actualizar_dir_calle(self, numEmpleado, dirCalle):
        consulta = "UPDATE vendedor SET dirCalle = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (dirCalle, numEmpleado))
        self._conexion.commit()

    def actualizar_dir_numero(self, numEmpleado, dirNumero):
        consulta = "UPDATE vendedor SET dirNumero = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (dirNumero, numEmpleado))
        self._conexion.commit()

    def actualizar_dir_colonia(self, numEmpleado, dirColonia):
        consulta = "UPDATE vendedor SET dirColonia = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (dirColonia, numEmpleado))
        self._conexion.commit()

    def actualizar_sucursal(self, numEmpleado, sucursal):
        consulta = "UPDATE vendedor SET sucursal = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (sucursal, numEmpleado))
        self._conexion.commit()

    def actualizar_estado(self, numEmpleado, activo):
        consulta = "UPDATE vendedor SET activo = %s WHERE numEmpleado = %s"
        self._cursor.execute(consulta,(activo, numEmpleado))
        self._conexion.commit()

    def eliminar(self, numEmpleado):
        consulta = "DELETE FROM vendedor WHERE numEmpleado = %s"
        self._cursor.execute(consulta, (numEmpleado,))
        self._conexion.commit()

    def consultar_dato(self, numEmpleado: int, nombre_campo: str):
        self._cursor.execute( f"SELECT {nombre_campo} FROM vendedor WHERE numEmpleado = %s", (numEmpleado,),)
        fila = self._cursor.fetchone()
        return fila[0] if fila else None

    def nombre_vendedor(self, numEmpleado: int):
        self._cursor.execute( f"SELECT CONCAT_WS(' ', nombrePila, primerApell, segundoApell) FROM vendedor WHERE numEmpleado = %s", (numEmpleado,),)
        fila = self._cursor.fetchone()
        return fila[0] if fila else None