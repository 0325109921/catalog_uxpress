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
        self._cursor.execute("SELECT sucursal,producto,cantStock FROM stock")
        return[Stock(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_stock(self, sucursal, producto, cantStock):
        consulta = "UPDATE stock SET cantStock = %s WHERE sucursal = %s AND producto = %s"
        self._cursor.execute(consulta,(cantStock, sucursal, producto))
        self._conexion.commit()

    def eliminar(self, sucursal, producto):
        consulta = "DELETE FROM stock WHERE sucursal = %s AND producto = %s"
        self._cursor.execute(consulta,(sucursal, producto,))
        self._conexion.commit()