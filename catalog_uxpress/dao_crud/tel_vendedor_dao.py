from clases.tel_vendedor import Tel_Vendedor

class Tel_VendedorDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, tel_vendedor: Tel_Vendedor):
        consulta = "INSERT INTO tel_vendedor (vendedor, numero, numTel) VALUES (%s,%s,%s)"
        self._cursor.execute(consulta, (tel_vendedor._vendedor, tel_vendedor._numero, tel_vendedor._numTel))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT vendedor,numero,numTel FROM tel_vendedor")
        return[Tel_Vendedor(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_numTel(self, vendedor, numero, numTel):
        consulta="UPDATE tel_vendedor SET numTel = %s WHERE vendedor = %s AND numero = %s"
        self._cursor.execute(consulta,(numTel, vendedor, numero))
        self._conexion.commit()

    def eliminar(self, vendedor, numero):
        consulta="DELETE FROM tel_vendedor WHERE vendedor = %s AND numero = %s"
        self._cursor.execute(consulta,(vendedor, numero))
        self._conexion.commit()