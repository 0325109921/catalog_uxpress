from clases.pago import Pago

class PagoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, pago: Pago):
        # numTransaccion es AUTO_INCREMENT: no se inserta, la BD lo asigna y se recupera con lastrowid
        consulta = "INSERT INTO pago (concepto, fecha, monto, numeroPago, saldo, pedido, cliente) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (pago._concepto, pago._fecha, pago._monto, pago._numeroPago, pago._saldo, pago._pedido, pago._cliente))
        self._conexion.commit()
        pago._numTransaccion = self._cursor.lastrowid
        return pago._numTransaccion

    def consultar_todas(self, sucursal=None):
        """ Si se indica 'sucursal' solo devuelve los pagos de pedidos atendidos por vendedores de esa sucursal """
        consulta = "SELECT pg.numTransaccion, pg.concepto, pg.fecha, pg.monto, pg.numeroPago, pg.saldo, pg.pedido, pg.cliente FROM pago AS pg"
        parametros = ()
        if sucursal is not None:
            consulta += " INNER JOIN pedido AS p ON p.numPedido = pg.pedido INNER JOIN vendedor AS v ON v.numEmpleado = p.vendedor WHERE v.sucursal = %s"
            parametros = (sucursal,)
        self._cursor.execute(consulta + " ORDER BY pg.numTransaccion", parametros)
        return[Pago(*fila) for fila in self._cursor.fetchall()]

    def pertenece_a_sucursal(self, numTransaccion, sucursal):
        consulta = "SELECT COUNT(*) FROM pago AS pg INNER JOIN pedido AS p ON p.numPedido = pg.pedido INNER JOIN vendedor AS v ON v.numEmpleado = p.vendedor WHERE pg.numTransaccion = %s AND v.sucursal = %s"
        self._cursor.execute(consulta, (numTransaccion, sucursal))
        return self._cursor.fetchall()[0][0] > 0

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