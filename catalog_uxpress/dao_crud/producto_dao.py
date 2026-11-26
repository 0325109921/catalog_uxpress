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