from clases.tel_repartidor import Tel_Repartidor

class Tel_RepartidorDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, tel_repartidor: Tel_Repartidor):
        consulta="INSERT INTO tel_repartidor(repartidor,numero,numTel) VALUES (%s,%s,%s)"
        self._cursor.execute(consulta, (tel_repartidor._repartidor, tel_repartidor._numero, tel_repartidor._numTel))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT repartidor, numero, numTel FROM tel_repartidor")
        return[Tel_Repartidor(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_num_tel(self, repartidor, numero, numTel):
        consulta = "UPDATE tel_repartidor SET numTel = %s WHERE repartidor = %s AND numero = %s"
        self._cursor.execute(consulta,(numTel, repartidor, numero))
        self._conexion.commit()

    def eliminar(self, repartidor, numero):
        consulta = "DELETE FROM tel_repartidor WHERE repartidor = %s AND numero = %s"
        self._cursor.execute(consulta, (repartidor, numero,))
        self._conexion.commit()