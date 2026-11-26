class Usuario:
    """
    Quien inicio sesion (sin contrasena)
    
    Solo existen dos roles: 
        ADMIN
        VENDEDOR
    ."""

    def __init__(self, idUsuario, nombreUsuario, rol, numEmpleado = None, sucursal = None):
        self.idUsuario = idUsuario
        self.nombreUsuario = nombreUsuario
        self.rol = rol
        self.numEmpleado = numEmpleado
        self.sucursal = sucursal # sucursal del vendedor vinculado (None si es ADMIN)

    def es_admin(self):
        return self.rol == "ADMIN"

    def es_vendedor(self):
        return self.rol == "VENDEDOR"

    def __str__(self):
        return f"{self.nombreUsuario} ({self.rol})"
