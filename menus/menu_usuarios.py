from mysql.connector import Error
from dao_crud.usuario_dao import UsuarioDAO
from dao_crud.vendedor_dao import VendedorDAO
from clases.vendedor import Vendedor
from utils.impresion import imprimir_tabla
from utils.autenticacion import ServicioAutenticacion
from utils.seguridad import generar_hash
from utils.validaciones import pedir_texto, pedir_entero, confirmar_accion


def listar_usuarios(usuario_dao: UsuarioDAO):
    """
    Muestra todos los usuarios registrados y su empleado vinculado si aplica
    """
    filas = usuario_dao.consultar_todos()
    if not filas:
        print("\nNo hay usuarios registrados.")
        return

    print("\n" + "=" * 78)
    print(f"| {'ID':<4} | {'USUARIO':<16} | {'ROL':<10} | {'ESTADO':<10} | {'BLOQ':<5} | {'EMPLEADO':<8} |")
    print("-" * 78)
    for id_u, nombre, rol, activo, _, bloqueado, vendedor in filas:
        estado_txt = "Activo" if activo == 1 else "Inactivo"
        bloq_txt = "Si" if bloqueado == 1 else "No"
        emp_txt = str(vendedor) if vendedor is not None else "-"
        print(f"| {id_u:<4} | {nombre:<16} | {rol:<10} | {estado_txt:<10} | {bloq_txt:<5} | {emp_txt:<8} |")
    print("-" * 78)


def crear_usuario(usuario_dao: UsuarioDAO, vendedor_dao: VendedorDAO):
    """
    Registra un nuevo usuario y permite vincularlo a un vendedor si su rol es VENDEDOR
    """
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    nombre = pedir_texto("Nombre de usuario: ")

    if usuario_dao.buscar_credenciales(nombre):
        print(f"El usuario '{nombre}' ya existe. Elige otro nombre.")
        return

    password = pedir_texto("Contrasena inicial: ")

    while True:
        rol = pedir_texto("Rol (ADMIN / VENDEDOR): ").upper() 
        if rol in ("ADMIN", "VENDEDOR"):
            break
        print("Rol no valido. Escribe ADMIN o VENDEDOR.")

    password_hash = generar_hash(password)

    try:
        usuario_dao.agregar(nombre, password_hash, rol)
        print(f"\nUsuario '{nombre}' creado correctamente.")

        if rol == "VENDEDOR" and confirmar_accion("Deseas vincularlo a un vendedor ahora? (s/n): "):
            vendedores = vendedor_dao.consultar_todas()
            if not vendedores:
                print("No hay vendedores registrados en la base de datos.")
                return

            print("\nVendedores disponibles:")
            imprimir_tabla(Vendedor.encabezado(), vendedores)

            num_emp = pedir_entero("Ingresa el numEmpleado a vincular: ")
            registro = usuario_dao.buscar_credenciales(nombre)
            id_nuevo = registro[0]
            usuario_dao.vincular_vendedor(id_nuevo, num_emp)
            print(f"Usuario '{nombre}' vinculado al empleado #{num_emp}.")

    except Error as e:
        print(f"\nError de base de datos al crear usuario: {e}")


def desbloquear_usuario(usuario_dao: UsuarioDAO):
    """
    Reinicia intentos fallidos y quita el bloqueo de una cuenta
    """
    listar_usuarios(usuario_dao)
    nombre = pedir_texto("\nNombre de usuario a desbloquear: ")

    if not usuario_dao.buscar_credenciales(nombre):
        print(f"No se encontro el usuario '{nombre}'.")
        return

    usuario_dao.desbloquear(nombre)
    print(f"Usuario '{nombre}' desbloqueado correctamente.")


def cambiar_estado_usuario(usuario_dao: UsuarioDAO, auth: ServicioAutenticacion):
    """
    Activa o desactiva una cuenta evitando que el admin actual se desactive a si mismo
    """
    listar_usuarios(usuario_dao)
    nombre = pedir_texto("\nNombre de usuario a modificar: ")

    if nombre == auth.usuario_actual.nombreUsuario:
        print("No puedes desactivar tu propia cuenta mientras tienes sesion iniciada.")
        return

    if not usuario_dao.buscar_credenciales(nombre):
        print(f"No se encontro el usuario '{nombre}'.")
        return

    activo = 1 if confirmar_accion("Activar cuenta? ('s' para activar / 'n' para desactivar): ") else 0
    usuario_dao.cambiar_estado(nombre, activo)
    estado_txt = "activada" if activo == 1 else "desactivada"
    print(f"Cuenta '{nombre}' {estado_txt} correctamente.")


def gestionar_vinculo_vendedor(usuario_dao: UsuarioDAO, vendedor_dao: VendedorDAO):
    """
    Vincula o desvincula un usuario a un registro de la tabla vendedor
    """
    listar_usuarios(usuario_dao)
    id_usuario = pedir_entero("\nIngresa el ID del usuario: ")
    print("1. Vincular a un vendedor")
    print("2. Desvincular vendedor actual")
    op = input("Selecciona una opcion: ").strip()

    try:
        if op == "1":
            vendedores = vendedor_dao.consultar_todas()
            if not vendedores:
                print("No hay vendedores registrados.")
                return
            print("\nVendedores disponibles:")
            imprimir_tabla(Vendedor.encabezado(), vendedores)
            num_emp = pedir_entero("Numero de empleado (numEmpleado): ")
            usuario_dao.vincular_vendedor(id_usuario, num_emp)
            print("Vinculo registrado correctamente.")
        elif op == "2":
            usuario_dao.desvincular_vendedor(id_usuario)
            print("Operacion completada. Si existia un vinculo, fue eliminado.")
        else:
            print("Opcion no valida.")
    except Error as e:
        print(f"\nError de base de datos en el vinculo: {e}")


def menu_usuarios(conexion, auth: ServicioAutenticacion):
    """
    Submenu de administracion de cuentas y roles
    """
    auth.exigir_admin()
    usuario_dao = UsuarioDAO(conexion)
    vendedor_dao = VendedorDAO(conexion)

    while True:
        print("\n" + "-" * 45)
        print(" GESTION DE USUARIOS Y ROLES")
        print("-" * 45)
        print("1. Listar usuarios")
        print("2. Crear nuevo usuario")
        print("3. Desbloquear usuario")
        print("4. Activar / Desactivar usuario")
        print("5. Vincular / Desvincular vendedor")
        print("0. Volver al menu principal")

        opcion = input("\nElige una opcion: ").strip() # Elimina los espacios en blanco

        if opcion == "1":
            listar_usuarios(usuario_dao)
        elif opcion == "2":
            crear_usuario(usuario_dao, vendedor_dao)
        elif opcion == "3":
            desbloquear_usuario(usuario_dao)
        elif opcion == "4":
            cambiar_estado_usuario(usuario_dao, auth)
        elif opcion == "5":
            gestionar_vinculo_vendedor(usuario_dao, vendedor_dao)
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")