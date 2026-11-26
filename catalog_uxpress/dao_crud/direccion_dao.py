from clases.direccion import Direccion

class DireccionDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def agregar(self, direccion: Direccion):
        consulta = "INSERT INTO direccion (numDireccion, calle, numero, colonia, cliente) VALUES (%s,%s,%s,%s,%s)"
        self._cursor.execute(consulta, (direccion._numDireccion, direccion._calle, direccion._numero, direccion._colonia, direccion._cliente))
        self._conexion.commit()

    def consultar_todas(self):
        self._cursor.execute("SELECT numDireccion, calle, numero, colonia, cliente FROM direccion")
        return[Direccion(*fila) for fila in self._cursor.fetchall()]
    
    def actualizar_calle(self, numDireccion, calle):
        consulta = "UPDATE direccion SET calle = %s WHERE numDireccion = %s"
        self._cursor.execute(consulta,(calle, numDireccion))
        self._conexion.commit()

    def actualizar_numero(self, numDireccion, numero):
        consulta = "UPDATE direccion SET numero = %s WHERE numDireccion = %s"
        self._cursor.execute(consulta,(numero, numDireccion))
        self._conexion.commit()

    def actualizar_colonia(self, numDireccion, colonia):
        consulta = "UPDATE direccion SET colonia = %s WHERE numDireccion = %s"
        self._cursor.execute(consulta,(colonia, numDireccion))
        self._conexion.commit()

    """
    cliente no tiene metodo actualizar porque Una dirección 
    registrada le pertenece a un cliente especifico: no se transfiere la casa de un cliente a otro.
    """
        
    def eliminar(self, numDireccion):
        consulta = "DELETE FROM direccion WHERE numDireccion = %s"
        self._cursor.execute(consulta, (numDireccion,))
        self._conexion.commit()