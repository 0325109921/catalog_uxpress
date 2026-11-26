from clases.pago import Pago

class PagoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, pago: Pago):
        consulta = "INSERT INTO pago (numTransaccion, concepto, fecha, monto, numeroPago, saldo, pedido, cliente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (pago._numTransaccion, pago._concepto, pago._fecha, pago._monto, pago._numeroPago, pago._saldo, pago._pedido, pago._cliente))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numTransaccion, concepto, fecha, monto, numeroPago, saldo, pedido, cliente FROM pago")
        return[Pago(*fila) for fila in self._cursor.fetchall()]

    def actualizar_concepto(self, numTransaccion, concepto):
        consulta = "UPDATE pago SET concepto = %s WHERE numTransaccion = %s"
        self._cursor.execute(consulta,(concepto, numTransaccion))
        self._conexion.commit()

    def actualizar_fecha(self, numTransaccion, fecha):
        consulta = "UPDATE pago SET fecha = %s WHERE numTransaccion = %s"
        self._cursor.execute(consulta, (fecha, numTransaccion))
        self._conexion.commit()

    def actualizar_monto(self, numTransaccion, monto):
        consulta = "UPDATE pago SET monto = %s WHERE numTransaccion = %s"
        self._cursor.execute(consulta, (monto, numTransaccion))
        self._conexion.commit()

    def actualizar_numeroPago(self, numTransaccion, numeroPago):
        consulta = "UPDATE pago SET numeroPago = %s WHERE numTransaccion = %s"
        self._cursor.execute(consulta, (numeroPago, numTransaccion))
        self._conexion.commit()

    def actualizar_saldo(self, numTransaccion, saldo):
        consulta = "UPDATE pago SET saldo = %s WHERE numTransaccion = %s"
        self._cursor.execute(consulta, (saldo, numTransaccion))
        self._conexion.commit()

    def eliminar(self, numTransaccion):
        consulta = "DELETE FROM pago WHERE numTransaccion = %s"
        self._cursor.execute(consulta, (numTransaccion,))
        self._conexion.commit()