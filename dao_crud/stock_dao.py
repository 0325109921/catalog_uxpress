from clases.stock import Stock

class StockDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, stock: Stock):
        consulta = "INSERT INTO stock (sucursal, producto, cantStock) VALUES (%s,%s,%s)"
        self._cursor.execute(consulta, (stock._sucursal, stock._producto, stock._cantStock))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT s.sucursal, s.producto, s.cantStock, p.nombre FROM stock AS s INNER JOIN producto AS p ON p.SKU = s.producto ORDER BY s.sucursal, s.producto")
        return[Stock(*fila) for fila in self._cursor.fetchall()]

    def consultar_por_sucursal(self, sucursal):
        """ Stock de una sola sucursal, con el nombre del producto junto a su SKU """
        self._cursor.execute("SELECT s.sucursal, s.producto, s.cantStock, p.nombre FROM stock AS s INNER JOIN producto AS p ON p.SKU = s.producto WHERE s.sucursal = %s ORDER BY s.producto", (sucursal,))
        return[Stock(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_stock(self, sucursal, producto, cantStock):
        consulta = "UPDATE stock SET cantStock = %s WHERE sucursal = %s AND producto = %s"
        self._cursor.execute(consulta,(cantStock, sucursal, producto))
        self._conexion.commit()

    def eliminar(self, sucursal, producto):
        consulta = "DELETE FROM stock WHERE sucursal = %s AND producto = %s"
        self._cursor.execute(consulta,(sucursal, producto,))
        self._conexion.commit()