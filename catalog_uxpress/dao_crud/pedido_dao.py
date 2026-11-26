from clases.pedido import Pedido

class PedidoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, pedido: Pedido):
        consulta = "INSERT INTO pedido (numPedido, fecha, cantArticulos, subtotal, IVA, total, catalogo, vendedor, estadoPedido, entrega, cliente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (pedido._numPedido, pedido._fecha, pedido._cantArticulos, pedido._subtotal, pedido._IVA, pedido._total, pedido._catalogo, pedido._vendedor, pedido._estadoPedido, pedido._entrega, pedido._cliente))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numPedido, fecha, cantArticulos, subtotal, IVA, total, catalogo, vendedor, estadoPedido, entrega, cliente FROM pedido")
        return[Pedido(*fila) for fila in self._cursor.fetchall()]

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