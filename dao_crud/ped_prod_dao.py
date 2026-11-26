from clases.ped_prod import Ped_Prod

class Ped_ProdDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, ped_prod: Ped_Prod):
        consulta = "INSERT INTO ped_prod (pedido, catalogo, producto, cantidad, precioUnitario, importe) VALUES (%s, %s, %s, %s, %s, %s)"
        self._cursor.execute(consulta, (ped_prod._pedido, ped_prod._catalogo, ped_prod._producto, ped_prod._cantidad, ped_prod._precioUnitario, ped_prod._importe))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT pedido, catalogo, producto, cantidad, precioUnitario, importe FROM ped_prod")
        return[Ped_Prod(*fila) for fila in self._cursor.fetchall()]
    
    def consultar_por_pedido(self, pedido):
        self._cursor.execute("SELECT pedido, catalogo, producto, cantidad, precioUnitario, importe FROM ped_prod WHERE pedido = %s ORDER BY producto", (pedido,))
        return[Ped_Prod(*fila) for fila in self._cursor.fetchall()]

    def actualizar_cantidad(self, pedido, catalogo, producto, cantidad):
        consulta  = "UPDATE ped_prod SET cantidad = %s WHERE pedido = %s AND catalogo = %s AND producto = %s"
        self._cursor.execute(consulta, (cantidad, pedido, catalogo, producto))
        self._conexion.commit()

    def actualizar_precio_unitario(self, pedido, catalogo, producto, precioUnitario):
        consulta = "UPDATE ped_prod SET precioUnitario = %s WHERE pedido = %s AND catalogo = %s AND producto = %s"
        self._cursor.execute(consulta, (precioUnitario, pedido, catalogo, producto))
        self._conexion.commit()

    def actualizar_importe(self, pedido, catalogo, producto, importe):
        consulta = "UPDATE ped_prod SET importe = %s WHERE pedido = %s AND catalogo = %s AND producto = %s"
        self._cursor.execute(consulta,(importe, pedido, catalogo, producto))
        self._conexion.commit()
        
    def eliminar(self, pedido, catalogo, producto):
        consulta = "DELETE FROM ped_prod WHERE pedido = %s AND catalogo = %s AND producto = %s"
        self._cursor.execute(consulta, (pedido, catalogo, producto,))
        self._conexion.commit()
    
    