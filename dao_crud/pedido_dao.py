from clases.pedido import Pedido

class PedidoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, pedido: Pedido):
        # numPedido es AUTO_INCREMENT: no se inserta, la BD lo asigna y se recupera con lastrowid
        consulta = "INSERT INTO pedido (fecha, cantArticulos, subtotal, IVA, total, catalogo, vendedor, estadoPedido, entrega, cliente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (pedido._fecha, pedido._cantArticulos, pedido._subtotal, pedido._IVA, pedido._total, pedido._catalogo, pedido._vendedor, pedido._estadoPedido, pedido._entrega, pedido._cliente))
        self._conexion.commit()
        pedido._numPedido = self._cursor.lastrowid
        return pedido._numPedido

    def consultar_todas(self, sucursal=None):
        """ Si se indica 'sucursal' solo devuelve los pedidos atendidos por vendedores de esa sucursal """
        consulta = "SELECT p.numPedido, p.fecha, p.cantArticulos, p.subtotal, p.IVA, p.total, p.catalogo, p.vendedor, p.estadoPedido, p.entrega, p.cliente FROM pedido AS p"
        parametros = ()
        if sucursal is not None:
            consulta += " INNER JOIN vendedor AS v ON v.numEmpleado = p.vendedor WHERE v.sucursal = %s"
            parametros = (sucursal,)
        self._cursor.execute(consulta + " ORDER BY p.numPedido", parametros)
        return[Pedido(*fila) for fila in self._cursor.fetchall()]

    def pertenece_a_sucursal(self, numPedido, sucursal):
        consulta = "SELECT COUNT(*) FROM pedido AS p INNER JOIN vendedor AS v ON v.numEmpleado = p.vendedor WHERE p.numPedido = %s AND v.sucursal = %s"
        self._cursor.execute(consulta, (numPedido, sucursal))
        return self._cursor.fetchall()[0][0] > 0

    def actualizar_fecha(self, numPedido, fecha):
        consulta = "UPDATE pedido SET fecha = %s WHERE numPedido = %s"
        self._cursor.execute(consulta, (fecha, numPedido))
        self._conexion.commit()

    def actualizar_cantArticulos(self, numPedido, cantArticulos):
        consulta = "UPDATE pedido SET cantArticulos = %s WHERE numPedido = %s"
        self._cursor.execute(consulta,(cantArticulos, numPedido))
        self._conexion.commit()

    def actualizar_subtotal(self, numPedido, subtotal):
        consulta = "UPDATE pedido SET subtotal = %s WHERE numPedido = %s"
        self._cursor.execute(consulta,(subtotal, numPedido))
        self._conexion.commit()

    def actualizar_iva(self, numPedido, IVA):
        consulta = "UPDATE pedido SET IVA = %s WHERE numPedido = %s"
        self._cursor.execute(consulta, (IVA, numPedido))
        self._conexion.commit()

    def actualizar_total(self, numPedido, total):
        consulta = "UPDATE pedido SET total = %s WHERE numPedido = %s"
        self._cursor.execute(consulta,(total,numPedido))
        self._conexion.commit()

    def actualizar_estado_pedido(self, numPedido, estadoPedido):
        consulta = "UPDATE pedido SET estadoPedido = %s WHERE numPedido = %s"
        self._cursor.execute(consulta, (estadoPedido, numPedido))
        self._conexion.commit()

    def actualizar_entrega(self, numPedido, entrega):
        consulta = "UPDATE pedido SET entrega = %s WHERE numPedido = %s"
        self._cursor.execute(consulta, (entrega, numPedido))
        self._conexion.commit()

    def eliminar(self, numPedido):
        consulta = "DELETE FROM pedido WHERE numPedido = %s"
        self._cursor.execute(consulta, (numPedido,))
        self._conexion.commit()