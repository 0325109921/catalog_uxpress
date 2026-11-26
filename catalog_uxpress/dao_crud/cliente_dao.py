import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from clases.cliente import Cliente

class ClienteDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, cliente: Cliente):
        consulta = "INSERT INTO cliente (numCliente, nombrePila, primerApell, segundoApell) VALUES (%s, %s, %s, %s)"
        self._cursor.execute(consulta, (cliente._numCliente, cliente._nombrePila, cliente._primerApell, cliente._segundoApell))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numCliente, nombrePila, primerApell, segundoApell FROM cliente")
        return[Cliente(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_nombre(self, numCliente, nombre):
        consulta = "UPDATE cliente SET nombrePila = %s WHERE numCliente = %s"
        self._cursor.execute(consulta,(nombre, numCliente))
        self._conexion.commit()

    def actualizar_primer_apell(self, numCliente, primerApell):
        consulta = "UPDATE cliente SET primerApell = %s WHERE numCliente = %s"
        self._cursor.execute(consulta, (primerApell, numCliente))
        self._conexion.commit()

    def actualizar_segundo_apell(self, numCliente, segundoApell):
        consulta = "UPDATE cliente SET segundoApell = %s WHERE numCliente = %s"
        self._cursor.execute(consulta, (segundoApell, numCliente))
        self._conexion.commit()

    def eliminar(self, numCliente):
        consulta = "DELETE FROM cliente WHERE numCliente = %s"
        self._cursor.execute(consulta, (numCliente,))
        self._conexion.commit()