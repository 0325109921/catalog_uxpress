from clases.tel_cliente import Tel_Cliente

class Tel_ClienteDAO:
    def __init__(self,conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, tel_cliente: Tel_Cliente):
        consulta = "INSERT INTO tel_cliente(cliente, numero, numTel) VALUES (%s,%s,%s)"
        self._cursor.execute(consulta, (tel_cliente._cliente, tel_cliente._numero, tel_cliente._numTel))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT cliente,numero,numTel FROM tel_cliente")
        return[Tel_Cliente(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_num_tel(self, cliente, numero, numTel):
        consulta = "UPDATE tel_cliente SET numTel = %s WHERE cliente = %s AND numero = %s"
        self._cursor.execute(consulta, (numTel, cliente, numero))
        self._conexion.commit()

    def eliminar(self, cliente, numero):
        consulta = "DELETE FROM tel_cliente WHERE cliente = %s AND numero = %s"
        self._cursor.execute(consulta, (cliente, numero,))
        self._conexion.commit()
