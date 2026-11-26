from clases.catalogo import Catalogo

class CatalogoDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, catalogo: Catalogo):
        consulta = "INSERT INTO catalogo (numCatalogo, nombre, vigenciaInicio, vigenciaFin, sucursal) VALUES (%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (catalogo._numCatalogo, catalogo._nombre, catalogo._vigenciaInicio, catalogo._vigenciaFin, catalogo._sucursal))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numCatalogo, nombre, vigenciaInicio, vigenciaFin, sucursal FROM catalogo")
        return[Catalogo(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_nombre(self, numCatalogo, nombre):
        consulta = "UPDATE catalogo SET nombre = %s WHERE numCatalogo = %s"
        self._cursor.execute(consulta,(nombre, numCatalogo))
        self._conexion.commit()

    def actualizar_vigencia_inicio(self, numCatalogo, vigenciaInicio):
        consulta="UPDATE catalogo SET vigenciaInicio = %s WHERE numCatalogo = %s"
        self._cursor.execute(consulta, (vigenciaInicio, numCatalogo))
        self._conexion.commit()

    def actualizar_vigencia_fin(self, numCatalogo, vigenciaFin):
        consulta = "UPDATE catalogo SET vigenciaFin = %s WHERE numCatalogo = %s"
        self._cursor.execute(consulta, (vigenciaFin, numCatalogo))
        self._conexion.commit()

    def actualizar_sucursal(self, numCatalogo, sucursal):
        consulta = "UPDATE catalogo SET sucursal = %s WHERE numCatalogo = %s"
        self._cursor.execute(consulta, (sucursal, numCatalogo))
        self._conexion.commit()

    def eliminar(self, numCatalogo):
        consulta = "DELETE FROM catalogo WHERE numCatalogo = %s"
        self._cursor.execute(consulta, (numCatalogo,))
        self._conexion.commit()

    """ Conserva esto """
    def consultar_dato(self, numCatalogo: int, nombre_campo: str):
        self._cursor.execute( f"SELECT {nombre_campo} FROM catalogo WHERE numCatalogo = %s", (numCatalogo,),)
        fila = self._cursor.fetchone()
        return fila[0] if fila else None

    def catalogos_sucursal(self, sucursal: str):
        self._cursor.execute("SELECT numCatalogo, nombre, vigenciaInicio, vigenciaFin FROM catalogo WHERE sucursal = %s",(sucursal,),)
        lineas = []
        for numero, nombre, inicio, fin in self._cursor.fetchall():
            fin = str(fin) if fin else "Sin fin"   # vigenciaFin puede ser NULL
            lineas.append(f"| {numero:<6} | {nombre:<100} | {str(inicio):<10} | {fin:<10} |")
        return lineas
    
    def lista_catalogos(self, sucursal: str):
        self._cursor.execute("SELECT numCatalogo FROM catalogo WHERE sucursal = %s",(sucursal,),)
        return [str(fila[0]) for fila in self._cursor.fetchall()]

    def lista_productos(self, catalogo:str):
        self._cursor.execute("SELECT producto.nombre, producto.descripcion, cat_prod.precio from cat_prod inner join catalogo on cat_prod.catalogo=catalogo.numCatalogo inner join producto on cat_prod.producto=producto.SKU where cat_prod.catalogo = %s",(catalogo,),)
        productos = []
        for nombre, descricpion, precio in self._cursor.fetchall():
            productos.append(f"| {nombre:<50} | {descricpion:<150} | ${precio:<8.2f} |")
        return productos

    
    