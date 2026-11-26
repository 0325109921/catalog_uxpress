from clases.producto import Producto

class ProductoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, producto: Producto):
        consulta = "INSERT INTO producto (SKU, nombre, descripcion) VALUES(%s,%s,%s)"
        self._cursor.execute(consulta,(producto._SKU, producto._nombre, producto._descripcion))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT SKU, nombre, descripcion FROM producto")
        return[Producto(*fila) for fila in self._cursor.fetchall() ]

    def consultar_por_sucursal(self, sucursal):
        """ Productos que la sucursal maneja: los que tiene en stock o en alguno de sus catalogos """
        consulta = ("SELECT SKU, nombre, descripcion FROM producto "
                    "WHERE SKU IN (SELECT producto FROM stock WHERE sucursal = %s) "
                    "OR SKU IN (SELECT cp.producto FROM cat_prod AS cp "
                    "INNER JOIN catalogo AS c ON c.numCatalogo = cp.catalogo WHERE c.sucursal = %s) "
                    "ORDER BY SKU")
        self._cursor.execute(consulta, (sucursal, sucursal))
        return[Producto(*fila) for fila in self._cursor.fetchall()]

    def actualizar_nombre(self, SKU, nombre):
        consulta = "UPDATE producto SET nombre = %s WHERE SKU = %s"
        self._cursor.execute(consulta, (nombre, SKU))
        self._conexion.commit()

    def actualizar_descripcion(self, SKU, descripcion):
        consulta = "UPDATE producto SET descripcion = %s WHERE SKU = %s"
        self._cursor.execute(consulta,(descripcion, SKU))
        self._conexion.commit()

    def eliminar (self, SKU):
        consulta = "DELETE FROM producto WHERE SKU = %s"
        self._cursor.execute(consulta, (SKU,))
        self._conexion.commit()