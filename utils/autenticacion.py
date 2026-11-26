from utils.excepciones import (AutenticacionError, CredencialesInvalidasError,
                               UsuarioBloqueadoError, PermisoDenegadoError)
from utils.seguridad import verificar_password
from clases.usuario import Usuario


class ServicioAutenticacion:
    MAX_INTENTOS = 3

    def __init__(self, usuario_dao):
        self._dao = usuario_dao
        self._usuario_actual = None

    @property
    def usuario_actual(self):
        return self._usuario_actual

    def iniciar_sesion(self, nombreUsuario, password):
        fila = self._dao.buscar_credenciales(nombreUsuario)
        if fila is None:                       # el usuario no existe
            raise CredencialesInvalidasError()

        # Desempaquetamos las 9 columnas exactas que devuelve UsuarioDAO
        id_usuario, nombre, hash_guardado, rol, activo, _, bloqueado, num_empleado, sucursal = fila

        if not activo:
            raise AutenticacionError("Esta cuenta de usuario está desactivada")

        if bloqueado:
            raise UsuarioBloqueadoError()

        if not verificar_password(password, hash_guardado):
            self._dao.registrar_intento_fallido(nombre, self.MAX_INTENTOS)
            raise CredencialesInvalidasError()

        self._dao.reiniciar_intentos(nombre)
        self._usuario_actual = Usuario(id_usuario, nombre, rol, num_empleado, sucursal)
        return self._usuario_actual

    def cerrar_sesion(self):
        self._usuario_actual = None

    def sucursal_permitida(self):
        """ADMIN -> None (sin restriccion). VENDEDOR -> codigo de su sucursal.
        Un vendedor sin sucursal (usuario sin vincular) no puede consultar datos."""
        usuario = self._usuario_actual
        if usuario is None:
            raise PermisoDenegadoError()
        if usuario.es_admin():
            return None
        if usuario.sucursal is None:
            raise PermisoDenegadoError("Tu usuario no esta vinculado a un vendedor con sucursal asignada")
        return usuario.sucursal

    def exigir_admin(self):
        if self._usuario_actual is None or not self._usuario_actual.es_admin():
            raise PermisoDenegadoError()