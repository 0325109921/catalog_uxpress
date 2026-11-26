import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


from dao_crud.usuario_dao import UsuarioDAO
from menus.menu_usuarios import menu_usuarios
from menus.menu_catalogos import menu_catalogos
from menus.menu_personas import menu_personas
from menus.menu_operaciones import menu_operaciones
from utils.autenticacion import ServicioAutenticacion
from utils.excepciones import AutenticacionError, PermisoDenegadoError
from utils.impresion import l, ms, limpiar_consola
from utils.logo import imprimir_logo
from utils.validaciones import pedir_texto, confirmar_accion


def mostrar_login(auth: ServicioAutenticacion):
    """
    Pide las credenciales hasta que se inicie la sesion o que el usuario decida salir
    """
    while True:
        limpiar_consola()
        imprimir_logo()
        l(45)
        print("      CATALOG UXPRESS - INICIO DE SESION")
        l(45)
        print("1. Iniciar sesion")
        print("0. Salir del sistema")
        opcion = input("\nSelecciona una opcion: ").strip()

        if opcion == "0":
            return None

        if opcion == "1":
            usuario = pedir_texto("Usuario: ")
            password = pedir_texto("Contrasena: ")
            try:
                user = auth.iniciar_sesion(usuario, password)
                print(f"\nBienvenido, {user.nombreUsuario} (Rol: {user.rol})")
                return user
            except AutenticacionError as e:
                print(f"\nACCESO DENEGADO: {e}")
                input("Presione Enter para continuar...")
        else:
            print("Opcion no valida.")


def menu_admin(conexion, auth: ServicioAutenticacion):
    """
    Menu completo exclusivo para administradores
    """
    while True:
        limpiar_consola()
        l(50)
        print(f" MENU ADMINISTRADOR | Usuario: {auth.usuario_actual.nombreUsuario}")
        l(50)
        print("1. Gestion de Usuarios y Roles")
        print("2. Catalogos, Productos y Stock")
        print("3. Clientes, Vendedores y Repartidores")
        print("4. Pedidos, Pagos y Entregas")
        print("0. Cerrar sesion")

        opcion = input("\nElige un modulo: ").strip()

        try:
            auth.exigir_admin()

            if opcion == "1":
                menu_usuarios(conexion, auth)
            elif opcion == "2":
                menu_catalogos(conexion, auth, solo_lectura=False)
            elif opcion == "3":
                menu_personas(conexion, auth, solo_clientes=False)
            elif opcion == "4":
                menu_operaciones(conexion, auth)
            elif opcion == "0":
                if confirmar_accion("Seguro que deseas cerrar sesion? (s/n): "):
                    auth.cerrar_sesion()
                    print("Sesion cerrada.")
                    break
            else:
                print("Opcion no valida.")
        except PermisoDenegadoError as e:
            print(f"\nERROR DE PERMISOS: {e}")
            break


def menu_vendedor(conexion, auth: ServicioAutenticacion):
    """
    Menu operativo para vendedores
    """
    user = auth.usuario_actual

    # Un vendedor solo opera sobre su sucursal: si su usuario no esta vinculado a un vendedor no puede continuar
    try:
        auth.sucursal_permitida()
    except PermisoDenegadoError as e:
        print(f"\nERROR DE PERMISOS: {e}")
        ms()
        auth.cerrar_sesion()
        return

    while True:
        limpiar_consola()
        l(65)
        print(f" MENU VENDEDOR | Usuario: {user.nombreUsuario} (Empleado #{user.numEmpleado}) | Sucursal: {user.sucursal}")
        l(65)
        print("1. Consultar Catalogos, Productos y Stock")
        print("2. Gestion de Clientes y Direcciones")
        print("3. Pedidos, Pagos y Entregas")
        print("0. Cerrar sesion")

        opcion = input("\nElige un modulo: ").strip()

        if opcion == "1":
            menu_catalogos(conexion, auth, solo_lectura=True)
        elif opcion == "2":
            menu_personas(conexion, auth, solo_clientes=True)
        elif opcion == "3":
            menu_operaciones(conexion, auth)
        elif opcion == "0":
            if confirmar_accion("Seguro que deseas cerrar sesion? (s/n): "):
                auth.cerrar_sesion()
                print("Sesion cerrada.")
                break
        else:
            print("Opcion no valida.")


def iniciar_sistema(conexion):
    """
    Punto de entrada principal de la interfaz de consola
    """
    usuario_dao = UsuarioDAO(conexion)
    auth = ServicioAutenticacion(usuario_dao)

    while True:
        user = mostrar_login(auth)
        if user is None:
            print("\nSaliendo de Catalog UXpress...")
            break

        if user.es_admin():
            menu_admin(conexion, auth)
        elif user.es_vendedor():
            menu_vendedor(conexion, auth)
        else:
            print(f"Rol no reconocido: {user.rol}")
            auth.cerrar_sesion()