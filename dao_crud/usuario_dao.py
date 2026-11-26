class UsuarioDAO:
    def __init__(self, conexion):
        self._conexion = conexion
        self._cursor = conexion.cursor()

    def contar(self):
        self._cursor.execute("SELECT COUNT(*) FROM usuario")
        return self._cursor.fetchone()[0]

    def agregar(self, nombreUsuario, passwordHash, rol):
        consulta = ("INSERT INTO usuario (nombreUsuario, passwordHash, rol) "
                    "VALUES (%s, %s, %s)")
        self._cursor.execute(consulta, (nombreUsuario, passwordHash, rol))
        self._conexion.commit()

    def buscar_credenciales(self, nombreUsuario):
        consulta = ("SELECT u.idUsuario, u.nombreUsuario, u.passwordHash, u.rol, u.activo, u.intentos, u.bloqueado, uv.vendedor, v.sucursal "
                    "FROM usuario AS u "
                    "LEFT JOIN usuario_vendedor AS uv ON uv.usuario = u.idUsuario "
                    "LEFT JOIN vendedor AS v ON v.numEmpleado = uv.vendedor "
                    "WHERE u.nombreUsuario = %s")
        self._cursor.execute(consulta, (nombreUsuario,))
        return self._cursor.fetchone()      # tupla o None

    def registrar_intento_fallido(self, nombreUsuario, maximo):
        # 1) suma el intento   2) bloquea si ya llego al maximo
        self._cursor.execute(
            "UPDATE usuario SET intentos = intentos + 1 WHERE nombreUsuario = %s",
            (nombreUsuario,))
        self._cursor.execute(
            "UPDATE usuario SET bloqueado = 1 "
            "WHERE nombreUsuario = %s AND intentos >= %s", (nombreUsuario, maximo))
        self._conexion.commit()

    def reiniciar_intentos(self, nombreUsuario):
        self._cursor.execute(
            "UPDATE usuario SET intentos = 0 WHERE nombreUsuario = %s", (nombreUsuario,))
        self._conexion.commit()

    def desbloquear(self, nombreUsuario):
        self._cursor.execute(
            "UPDATE usuario SET intentos = 0, bloqueado = 0 "
            "WHERE nombreUsuario = %s", (nombreUsuario,))
        self._conexion.commit()
        return self._cursor.rowcount > 0



    def consultar_todos(self):
        consulta = (
            "SELECT u.idUsuario, u.nombreUsuario, u.rol, u.activo, "
            "u.intentos, u.bloqueado, uv.vendedor "
            "FROM usuario AS u "
            "LEFT JOIN usuario_vendedor AS uv ON uv.usuario = u.idUsuario "
            "ORDER BY u.idUsuario"
        )
        self._cursor.execute(consulta)
        return self._cursor.fetchall()

    def cambiar_estado(self, nombreUsuario, activo):
        consulta = "UPDATE usuario SET activo = %s WHERE nombreUsuario = %s"
        self._cursor.execute(consulta, (activo, nombreUsuario))
        self._conexion.commit()

    def vincular_vendedor(self, idUsuario, numEmpleado):
        consulta = "INSERT INTO usuario_vendedor (usuario, vendedor) VALUES (%s, %s)"
        self._cursor.execute(consulta, (idUsuario, numEmpleado))
        self._conexion.commit()

    def desvincular_vendedor(self, idUsuario):
        consulta = "DELETE FROM usuario_vendedor WHERE usuario = %s"
        self._cursor.execute(consulta, (idUsuario,))
        self._conexion.commit()
