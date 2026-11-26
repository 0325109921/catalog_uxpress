import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.repartidor import Repartidor

class RepartidorDAO:
    def __init__(self,conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()
    def agregar(self, repartidor: Repartidor):
        consulta = "INSERT INTO repartidor (numRepartidor, nombrePila, primerApell, segundoApell, dirCalle, dirNumero, dirColonia, activo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (repartidor._numRepartidor, repartidor._nombrePila, repartidor._primerApell, repartidor._segundoApell, repartidor._dirCalle, repartidor._dirNumero, repartidor._dirColonia, repartidor._activo))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numRepartidor, nombrePila, primerApell, segundoApell, dirCalle, dirNumero, dirColonia, activo FROM repartidor")
        return[Repartidor(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_estado(self, numRepartidor, activo):
        consulta = "UPDATE repartidor SET activo = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (activo, numRepartidor))
        self._conexion.commit()

    def actualizar_nombre(self, numRepartidor, nombre):
        consulta = "UPDATE repartidor SET nombrePila = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (nombre, numRepartidor))
        self._conexion.commit()

    def actualizar_primer_apell(self, numRepartidor, primerApell):
        consulta = "UPDATE repartidor SET primerApell = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta,(primerApell, numRepartidor))
        self._conexion.commit()

    def actualizar_segundo_apell(self,numRepartidor, segundoApell):
        consulta = "UPDATE repartidor SET segundoApell = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (segundoApell, numRepartidor))
        self._conexion.commit()

    def actualizar_dir_calle(self, numRepartidor, dirCalle):
        consulta = "UPDATE repartidor SET dirCalle = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (dirCalle, numRepartidor))
        self._conexion.commit()

    def actualizar_dir_numero(self, numRepartidor, dirNumero):
        consulta = "UPDATE repartidor SET dirNumero = %s WHERE numRepartidor =%s"
        self._cursor.execute(consulta, (dirNumero, numRepartidor))
        self._conexion.commit()

    def actualizar_dir_colonia(self, numRepartidor, dirColonia):
        consulta = "UPDATE repartidor SET dirColonia = %s WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (dirColonia, numRepartidor))
        self._conexion.commit()

    def eliminar(self, numRepartidor):
        consulta = "DELETE FROM repartidor WHERE numRepartidor = %s"
        self._cursor.execute(consulta, (numRepartidor,))
        self._conexion.commit()
