from clases.entrega import Entrega

class EntregaDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, entrega: Entrega):
        # codigo es AUTO_INCREMENT: no se inserta, la BD lo asigna y se recupera con lastrowid
        consulta = "INSERT INTO entrega (fechaEntrega, entregaConfirmada, estadoEntrega, sucursal, repartidor, direccion) VALUES (%s,%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (entrega._fechaEntrega, entrega._entregaConfirmada, entrega._estadoEntrega, entrega._sucursal, entrega._repartidor, entrega._direccion))
        self._conexion.commit()
        entrega._codigo = self._cursor.lastrowid
        return entrega._codigo

    def consultar_todas(self, sucursal=None):
        consulta = "SELECT codigo, fechaEntrega, entregaConfirmada, estadoEntrega, sucursal, repartidor, direccion FROM entrega"
        parametros = ()
        if sucursal is not None:      # filtra por sucursal cuando se indica una
            consulta += " WHERE sucursal = %s"
            parametros = (sucursal,)
        self._cursor.execute(consulta + " ORDER BY codigo", parametros)
        return[Entrega(*fila) for fila in self._cursor.fetchall()]

    def pertenece_a_sucursal(self, codigo, sucursal):
        self._cursor.execute("SELECT COUNT(*) FROM entrega WHERE codigo = %s AND sucursal = %s", (codigo, sucursal))
        return self._cursor.fetchall()[0][0] > 0
    
    def actualizar_fecha_entrega(self, codigo, fechaEntrega):
        consulta = "UPDATE entrega SET fechaEntrega = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (fechaEntrega, codigo))
        self._conexion.commit()

    def actualizar_entrega_confirmada(self, codigo, entregaConfirmada):
        consulta = "UPDATE entrega SET entregaConfirmada = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (entregaConfirmada, codigo))
        self._conexion.commit()

    def actualizar_estado_entrega(self, codigo, estadoEntrega):
        consulta = "UPDATE entrega SET estadoEntrega = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (estadoEntrega, codigo))
        self._conexion.commit()

    def actualizar_sucursal(self, codigo, sucursal):
        consulta = "UPDATE entrega SET sucursal = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (sucursal, codigo))
        self._conexion.commit()

    def actualizar_repartidor(self, codigo, repartidor):
        consulta = "UPDATE entrega SET repartidor = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (repartidor, codigo))
        self._conexion.commit()

    def actualizar_direccion(self, codigo, direccion):
        consulta = "UPDATE entrega SET direccion = %s WHERE codigo = %s"
        self._cursor.execute(consulta, (direccion, codigo))
        self._conexion.commit()

    def eliminar(self, codigo):
        consulta = "DELETE FROM entrega WHERE codigo = %s"
        self._cursor.execute(consulta, (codigo,))
        self._conexion.commit()