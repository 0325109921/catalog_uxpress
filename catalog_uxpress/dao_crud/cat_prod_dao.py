from clases.cat_prod import Cat_Prod

class Cat_ProdDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()


    def agregar(self, cat_prod: Cat_Prod): 
        consulta = "INSERT INTO cat_prod (catalogo, producto, precio) VALUES (%s, %s, %s)"
        self._cursor.execute(consulta, (cat_prod._catalogo, cat_prod._producto, cat_prod._precio))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT catalogo, producto, precio FROM cat_prod")
        return[Cat_Prod(*fila) for fila in self._cursor.fetchall()]

    def actualizar_precio(self, catalogo, producto, precio):
        consulta = "UPDATE cat_prod SET precio = %s WHERE catalogo = %s and producto = %s"
        self._cursor.execute(consulta, (precio, catalogo, producto))
        self._conexion.commit()

    """
    Es necesario eliminiar? 
    """
    def eliminar(self, catalogo, producto):
        consulta = "DELETE FROM cat_prod WHERE catalogo = %s and producto = %s"
        self._cursor.execute(consulta, (catalogo, producto,))
        self._conexion.commit()
            