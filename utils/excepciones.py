class AutenticacionError(Exception):
    """Clase base de los errores del login."""


class CredencialesInvalidasError(AutenticacionError):
    def __init__(self, mensaje = "Usuario o contrasena incorrectos"):
        super().__init__(mensaje)


class UsuarioBloqueadoError(AutenticacionError):
    def __init__(self, mensaje = "Usuario bloqueado por intentos fallidos"):
        super().__init__(mensaje)


class PermisoDenegadoError(AutenticacionError):
    def __init__(self, mensaje = "No tienes permiso para esta operacion"):
        super().__init__(mensaje)
