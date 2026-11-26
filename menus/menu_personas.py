from mysql.connector import Error
from clases.cliente import Cliente
from clases.direccion import Direccion
from clases.tel_cliente import Tel_Cliente
from clases.vendedor import Vendedor
from clases.tel_vendedor import Tel_Vendedor
from clases.repartidor import Repartidor
from clases.tel_repartidor import Tel_Repartidor
from clases.sucursal import Sucursal
from dao_crud.cliente_dao import ClienteDAO
from dao_crud.direccion_dao import DireccionDAO
from dao_crud.tel_cliente_dao import Tel_ClienteDAO
from dao_crud.vendedor_dao import VendedorDAO
from dao_crud.tel_vendedor_dao import Tel_VendedorDAO
from dao_crud.repartidor_dao import RepartidorDAO
from dao_crud.tel_repartidor_dao import Tel_RepartidorDAO
from dao_crud.sucursal_dao import SucursalDAO
from utils.autenticacion import ServicioAutenticacion
from utils.impresion import s, l, ms, limpiar_consola, encabezado, imprimir_tabla
from utils.validaciones import pedir_texto, pedir_entero, confirmar_accion


# ==========================================
# SECCION 1: CLIENTES, DIRECCIONES Y TELEFONOS
# ==========================================
def listar_clientes(cliente_dao: ClienteDAO):
    lista = cliente_dao.consultar_todas()
    s()
    l(65)
    print(" LISTADO DE CLIENTES")
    l(65)
    if not lista:
        print("No hay clientes registrados.")
        return
    encabezado(Cliente.encabezado())
    for cli in lista:
        print(cli)


def gestionar_direcciones_cliente(direccion_dao: DireccionDAO, cliente_dao: ClienteDAO):
    while True:
        limpiar_consola()
        l(50)
        print(" DIRECCIONES DE CLIENTES")
        l(50)
        print("1. Listar todas las direcciones")
        print("2. Agregar direccion a un cliente")
        print("3. Actualizar direccion")
        print("4. Eliminar direccion")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                lista = direccion_dao.consultar_todas()
                s()
                if not lista:
                    print("No hay direcciones registradas.")
                else:
                    encabezado(Direccion.encabezado())
                    for d in lista:
                        print(d)
                ms()
            elif op == "2":
                listar_clientes(cliente_dao)
                calle = pedir_texto("\nCalle: ")
                numero = pedir_texto("Numero exterior/interior: ")
                colonia = pedir_texto("Colonia: ")
                num_cli = pedir_entero("Numero de cliente (numCliente): ")
                num_dir = direccion_dao.agregar(Direccion(None, calle, numero, colonia, num_cli))
                print(f"Direccion registrada correctamente con el numero {num_dir}.")
                ms()
            elif op == "3":
                imprimir_tabla(Direccion.encabezado(), direccion_dao.consultar_todas())
                num_dir = pedir_entero("\nNumero de direccion a modificar: ")
                print("1. Calle | 2. Numero | 3. Colonia")
                campo = input("Campo a actualizar: ").strip()
                if campo == "1":
                    direccion_dao.actualizar_calle(num_dir, pedir_texto("Nueva calle: "))
                elif campo == "2":
                    direccion_dao.actualizar_numero(num_dir, pedir_texto("Nuevo numero: "))
                elif campo == "3":
                    direccion_dao.actualizar_colonia(num_dir, pedir_texto("Nueva colonia: "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Direccion actualizada.")
                ms()
            elif op == "4":
                imprimir_tabla(Direccion.encabezado(), direccion_dao.consultar_todas())
                num_dir = pedir_entero("\nNumero de direccion a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar esta direccion? (s/n): "):
                    direccion_dao.eliminar(num_dir)
                    print("Direccion eliminada.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


def gestionar_tel_clientes(tel_cliente_dao: Tel_ClienteDAO, cliente_dao: ClienteDAO):
    while True:
        limpiar_consola()
        l(50)
        print(" TELEFONOS DE CLIENTES")
        l(50)
        print("1. Listar telefonos de clientes")
        print("2. Agregar telefono")
        print("3. Actualizar numero telefonico")
        print("4. Eliminar telefono")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                lista = tel_cliente_dao.consultar_todas()
                s()
                if not lista:
                    print("No hay telefonos registrados.")
                else:
                    encabezado(Tel_Cliente.encabezado())
                    for t in lista:
                        print(t)
                ms()
            elif op == "2":
                listar_clientes(cliente_dao)
                num_cli = pedir_entero("\nNumero de cliente: ")
                consecutivo = pedir_entero("Numero consecutivo de telefono (ej. 1, 2): ")
                telefono = pedir_texto("Numero telefonico (10 digitos): ")
                tel_cliente_dao.agregar(Tel_Cliente(num_cli, consecutivo, telefono))
                print("Telefono registrado.")
                ms()
            elif op == "3":
                imprimir_tabla(Tel_Cliente.encabezado(), tel_cliente_dao.consultar_todas())
                num_cli = pedir_entero("\nNumero de cliente: ")
                consecutivo = pedir_entero("Consecutivo del telefono: ")
                nuevo_tel = pedir_texto("Nuevo numero telefonico: ")
                tel_cliente_dao.actualizar_num_tel(num_cli, consecutivo, nuevo_tel)
                print("Telefono actualizado.")
                ms()
            elif op == "4":
                imprimir_tabla(Tel_Cliente.encabezado(), tel_cliente_dao.consultar_todas())
                num_cli = pedir_entero("\nNumero de cliente: ")
                consecutivo = pedir_entero("Consecutivo a eliminar: ")
                if confirmar_accion("Eliminar telefono? (s/n): "):
                    tel_cliente_dao.eliminar(num_cli, consecutivo)
                    print("Telefono eliminado.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


def gestionar_clientes(
    cliente_dao: ClienteDAO,
    direccion_dao: DireccionDAO,
    tel_cliente_dao: Tel_ClienteDAO,
):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE CLIENTES")
        l(50)
        print("1. Listar clientes")
        print("2. Registrar nuevo cliente")
        print("3. Actualizar datos de cliente")
        print("4. Eliminar cliente")
        print("5. Gestionar direcciones de clientes")
        print("6. Gestionar telefonos de clientes")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_clientes(cliente_dao)
                ms()
            elif op == "2":
                nombre = pedir_texto("Nombre de pila: ")
                ap1 = pedir_texto("Primer apellido: ")
                ap2_in = input("Segundo apellido (Enter si no tiene): ").strip()
                ap2 = ap2_in if ap2_in != "" else None
                num_cli = cliente_dao.agregar(Cliente(None, nombre, ap1, ap2))
                print(f"\nCliente registrado correctamente con el numero {num_cli}.")
                ms()
            elif op == "3":
                listar_clientes(cliente_dao)
                num_cli = pedir_entero("\nNumero de cliente a actualizar: ")
                print("1. Nombre | 2. Primer apellido | 3. Segundo apellido")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    cliente_dao.actualizar_nombre(num_cli, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    cliente_dao.actualizar_primer_apell(num_cli, pedir_texto("Nuevo primer apellido: "))
                elif campo == "3":
                    ap2_in = input("Nuevo segundo apellido (Enter para vacio): ").strip()
                    cliente_dao.actualizar_segundo_apell(num_cli, ap2_in if ap2_in != "" else None)
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Cliente actualizado.")
                ms()
            elif op == "4":
                listar_clientes(cliente_dao)
                num_cli = pedir_entero("\nNumero de cliente a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este cliente? (s/n): "):
                    cliente_dao.eliminar(num_cli)
                    print("Cliente eliminado.")
                ms()
            elif op == "5":
                gestionar_direcciones_cliente(direccion_dao, cliente_dao)
            elif op == "6":
                gestionar_tel_clientes(tel_cliente_dao, cliente_dao)
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# SECCION 2: VENDEDORES Y TELEFONOS (ADMIN)
# ==========================================
def listar_vendedores(vendedor_dao: VendedorDAO):
    lista = vendedor_dao.consultar_todas()
    s()
    l(75)
    print(" LISTADO DE VENDEDORES")
    l(75)
    if not lista:
        print("No hay vendedores registrados.")
        return
    encabezado(Vendedor.encabezado())
    for v in lista:
        print(v)


def gestionar_tel_vendedores(tel_vendedor_dao: Tel_VendedorDAO, vendedor_dao: VendedorDAO):
    while True:
        limpiar_consola()
        l(50)
        print(" TELEFONOS DE VENDEDORES")
        l(50)
        print("1. Listar telefonos de vendedores")
        print("2. Agregar telefono")
        print("3. Actualizar numero telefonico")
        print("4. Eliminar telefono")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                lista = tel_vendedor_dao.consultar_todas()
                s()
                if not lista:
                    print("No hay telefonos registrados.")
                else:
                    encabezado(Tel_Vendedor.encabezado())
                    for t in lista:
                        print(t)
                ms()
            elif op == "2":
                listar_vendedores(vendedor_dao)
                num_emp = pedir_entero("\nNumero de empleado: ")
                consecutivo = pedir_entero("Numero consecutivo (ej. 1, 2): ")
                telefono = pedir_texto("Numero telefonico: ")
                tel_vendedor_dao.agregar(Tel_Vendedor(num_emp, consecutivo, telefono))
                print("Telefono registrado.")
                ms()
            elif op == "3":
                imprimir_tabla(Tel_Vendedor.encabezado(), tel_vendedor_dao.consultar_todas())
                num_emp = pedir_entero("\nNumero de empleado: ")
                consecutivo = pedir_entero("Consecutivo del telefono: ")
                nuevo_tel = pedir_texto("Nuevo numero telefonico: ")
                tel_vendedor_dao.actualizar_numTel(num_emp, consecutivo, nuevo_tel)
                print("Telefono actualizado.")
                ms()
            elif op == "4":
                imprimir_tabla(Tel_Vendedor.encabezado(), tel_vendedor_dao.consultar_todas())
                num_emp = pedir_entero("\nNumero de empleado: ")
                consecutivo = pedir_entero("Consecutivo a eliminar: ")
                if confirmar_accion("Eliminar telefono? (s/n): "):
                    tel_vendedor_dao.eliminar(num_emp, consecutivo)
                    print("Telefono eliminado.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


def gestionar_vendedores(
    vendedor_dao: VendedorDAO,
    tel_vendedor_dao: Tel_VendedorDAO,
    sucursal_dao: SucursalDAO,
):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE VENDEDORES")
        l(50)
        print("1. Listar vendedores")
        print("2. Registrar nuevo vendedor")
        print("3. Actualizar datos de vendedor")
        print("4. Activar / Desactivar vendedor")
        print("5. Eliminar vendedor")
        print("6. Gestionar telefonos de vendedores")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_vendedores(vendedor_dao)
                ms()
            elif op == "2":
                nombre = pedir_texto("Nombre de pila: ")
                ap1 = pedir_texto("Primer apellido: ")
                ap2_in = input("Segundo apellido (Enter si no tiene): ").strip()
                ap2 = ap2_in if ap2_in != "" else None
                calle = pedir_texto("Calle: ")
                numero = pedir_texto("Numero exterior: ")
                colonia = pedir_texto("Colonia: ")
                print("\nSucursales disponibles:")
                imprimir_tabla(Sucursal.encabezado(), sucursal_dao.consultar_todas())
                sucursal = pedir_texto("Codigo de sucursal: ").upper()
                num_emp = vendedor_dao.agregar(Vendedor(None, nombre, ap1, ap2, calle, numero, colonia, sucursal, True))
                print(f"\nVendedor registrado correctamente con el numero de empleado {num_emp}.")
                ms()
            elif op == "3":
                listar_vendedores(vendedor_dao)
                num_emp = pedir_entero("\nNumero de empleado a actualizar: ")
                print("1. Nombre | 2. Primer apellido | 3. Segundo apellido")
                print("4. Calle  | 5. Numero          | 6. Colonia | 7. Sucursal")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    vendedor_dao.actualizar_nombre(num_emp, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    vendedor_dao.actualizar_primer_apell(num_emp, pedir_texto("Nuevo primer apellido: "))
                elif campo == "3":
                    ap2_in = input("Nuevo segundo apellido (Enter para vacio): ").strip()
                    vendedor_dao.actualizar_segundo_apell(num_emp, ap2_in if ap2_in != "" else None)
                elif campo == "4":
                    vendedor_dao.actualizar_dir_calle(num_emp, pedir_texto("Nueva calle: "))
                elif campo == "5":
                    vendedor_dao.actualizar_dir_numero(num_emp, pedir_texto("Nuevo numero: "))
                elif campo == "6":
                    vendedor_dao.actualizar_dir_colonia(num_emp, pedir_texto("Nueva colonia: "))
                elif campo == "7":
                    vendedor_dao.actualizar_sucursal(num_emp, pedir_texto("Nueva sucursal: ").upper())
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Vendedor actualizado.")
                ms()
            elif op == "4":
                listar_vendedores(vendedor_dao)
                num_emp = pedir_entero("\nNumero de empleado: ")
                activo = 1 if confirmar_accion("Marcar como Activo? ('s' Activo / 'n' Inactivo): ") else 0
                vendedor_dao.actualizar_estado(num_emp, activo)
                print(f"Estado cambiado a {'Activo' if activo == 1 else 'Inactivo'}.")
                ms()
            elif op == "5":
                listar_vendedores(vendedor_dao)
                num_emp = pedir_entero("\nNumero de empleado a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este vendedor? (s/n): "):
                    vendedor_dao.eliminar(num_emp)
                    print("Vendedor eliminado.")
                ms()
            elif op == "6":
                gestionar_tel_vendedores(tel_vendedor_dao, vendedor_dao)
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# SECCION 3: REPARTIDORES Y TELEFONOS (ADMIN)
# ==========================================
def listar_repartidores(repartidor_dao: RepartidorDAO):
    lista = repartidor_dao.consultar_todas()
    s()
    l(75)
    print(" LISTADO DE REPARTIDORES")
    l(75)
    if not lista:
        print("No hay repartidores registrados.")
        return
    encabezado(Repartidor.encabezado())
    for r in lista:
        print(r)


def gestionar_tel_repartidores(tel_repartidor_dao: Tel_RepartidorDAO, repartidor_dao: RepartidorDAO):
    while True:
        limpiar_consola()
        l(50)
        print(" TELEFONOS DE REPARTIDORES")
        l(50)
        print("1. Listar telefonos de repartidores")
        print("2. Agregar telefono")
        print("3. Actualizar numero telefonico")
        print("4. Eliminar telefono")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                lista = tel_repartidor_dao.consultar_todas()
                s()
                if not lista:
                    print("No hay telefonos registrados.")
                else:
                    encabezado(Tel_Repartidor.encabezado())
                    for t in lista:
                        print(t)
                ms()
            elif op == "2":
                listar_repartidores(repartidor_dao)
                num_rep = pedir_entero("\nNumero de repartidor: ")
                consecutivo = pedir_entero("Numero consecutivo (ej. 1, 2): ")
                telefono = pedir_texto("Numero telefonico: ")
                tel_repartidor_dao.agregar(Tel_Repartidor(num_rep, consecutivo, telefono))
                print("Telefono registrado.")
                ms()
            elif op == "3":
                imprimir_tabla(Tel_Repartidor.encabezado(), tel_repartidor_dao.consultar_todas())
                num_rep = pedir_entero("\nNumero de repartidor: ")
                consecutivo = pedir_entero("Consecutivo del telefono: ")
                nuevo_tel = pedir_texto("Nuevo numero telefonico: ")
                tel_repartidor_dao.actualizar_num_tel(num_rep, consecutivo, nuevo_tel)
                print("Telefono actualizado.")
                ms()
            elif op == "4":
                imprimir_tabla(Tel_Repartidor.encabezado(), tel_repartidor_dao.consultar_todas())
                num_rep = pedir_entero("\nNumero de repartidor: ")
                consecutivo = pedir_entero("Consecutivo a eliminar: ")
                if confirmar_accion("Eliminar telefono? (s/n): "):
                    tel_repartidor_dao.eliminar(num_rep, consecutivo)
                    print("Telefono eliminado.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


def gestionar_repartidores(repartidor_dao: RepartidorDAO, tel_repartidor_dao: Tel_RepartidorDAO):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE REPARTIDORES")
        l(50)
        print("1. Listar repartidores")
        print("2. Registrar nuevo repartidor")
        print("3. Actualizar datos de repartidor")
        print("4. Activar / Desactivar repartidor")
        print("5. Eliminar repartidor")
        print("6. Gestionar telefonos de repartidores")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_repartidores(repartidor_dao)
                ms()
            elif op == "2":
                nombre = pedir_texto("Nombre de pila: ")
                ap1 = pedir_texto("Primer apellido: ")
                ap2_in = input("Segundo apellido (Enter si no tiene): ").strip()
                ap2 = ap2_in if ap2_in != "" else None
                calle = pedir_texto("Calle: ")
                numero = pedir_texto("Numero exterior: ")
                colonia = pedir_texto("Colonia: ")
                num_rep = repartidor_dao.agregar(Repartidor(None, nombre, ap1, ap2, calle, numero, colonia, True))
                print(f"\nRepartidor registrado correctamente con el numero {num_rep}.")
                ms()
            elif op == "3":
                listar_repartidores(repartidor_dao)
                num_rep = pedir_entero("\nNumero de repartidor a actualizar: ")
                print("1. Nombre | 2. Primer apellido | 3. Segundo apellido")
                print("4. Calle  | 5. Numero          | 6. Colonia")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    repartidor_dao.actualizar_nombre(num_rep, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    repartidor_dao.actualizar_primer_apell(num_rep, pedir_texto("Nuevo primer apellido: "))
                elif campo == "3":
                    ap2_in = input("Nuevo segundo apellido (Enter para vacio): ").strip()
                    repartidor_dao.actualizar_segundo_apell(num_rep, ap2_in if ap2_in != "" else None)
                elif campo == "4":
                    repartidor_dao.actualizar_dir_calle(num_rep, pedir_texto("Nueva calle: "))
                elif campo == "5":
                    repartidor_dao.actualizar_dir_numero(num_rep, pedir_texto("Nuevo numero: "))
                elif campo == "6":
                    repartidor_dao.actualizar_dir_colonia(num_rep, pedir_texto("Nueva colonia: "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Repartidor actualizado.")
                ms()
            elif op == "4":
                listar_repartidores(repartidor_dao)
                num_rep = pedir_entero("\nNumero de repartidor: ")
                activo = 1 if confirmar_accion("Marcar como Activo? ('s' Activo / 'n' Inactivo): ") else 0
                repartidor_dao.actualizar_estado(num_rep, activo)
                print(f"Estado cambiado a {'Activo' if activo == 1 else 'Inactivo'}.")
                ms()
            elif op == "5":
                listar_repartidores(repartidor_dao)
                num_rep = pedir_entero("\nNumero de repartidor a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este repartidor? (s/n): "):
                    repartidor_dao.eliminar(num_rep)
                    print("Repartidor eliminado.")
                ms()
            elif op == "6":
                gestionar_tel_repartidores(tel_repartidor_dao, repartidor_dao)
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# MENU PRINCIPAL DEL MODULO
# ==========================================
def menu_personas(conexion, auth: ServicioAutenticacion, solo_clientes=False):
    cliente_dao = ClienteDAO(conexion)
    direccion_dao = DireccionDAO(conexion)
    tel_cliente_dao = Tel_ClienteDAO(conexion)

    if solo_clientes:
        gestionar_clientes(cliente_dao, direccion_dao, tel_cliente_dao)
        return

    auth.exigir_admin()
    vendedor_dao = VendedorDAO(conexion)
    tel_vendedor_dao = Tel_VendedorDAO(conexion)
    repartidor_dao = RepartidorDAO(conexion)
    tel_repartidor_dao = Tel_RepartidorDAO(conexion)
    sucursal_dao = SucursalDAO(conexion)

    while True:
        limpiar_consola()
        l(50)
        print(" MODULO: CLIENTES, VENDEDORES Y REPARTIDORES")
        l(50)
        print("1. Clientes, Direcciones y Telefonos")
        print("2. Vendedores y Telefonos")
        print("3. Repartidores y Telefonos")
        print("0. Volver al menu principal")

        op = input("\nElige una opcion: ").strip()
        if op == "1":
            gestionar_clientes(cliente_dao, direccion_dao, tel_cliente_dao)
        elif op == "2":
            gestionar_vendedores(vendedor_dao, tel_vendedor_dao, sucursal_dao)
        elif op == "3":
            gestionar_repartidores(repartidor_dao, tel_repartidor_dao)
        elif op == "0":
            break
        else:
            print("Opcion no valida.")
            ms()