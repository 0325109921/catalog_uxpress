from datetime import datetime
from mysql.connector import Error
from clases.pedido import Pedido
from clases.ped_prod import Ped_Prod
from clases.pago import Pago
from clases.entrega import Entrega
from clases.estado_pedido import Estado_Pedido
from clases.estado_entrega import Estado_Entrega
from dao_crud.pedido_dao import PedidoDAO
from dao_crud.ped_prod_dao import Ped_ProdDAO
from dao_crud.pago_dao import PagoDAO
from dao_crud.entrega_dao import EntregaDAO
from dao_crud.estado_pedido_dao import Estado_PedidoDAO
from dao_crud.estado_entrega_dao import Estado_EntregaDAO
from dao_crud.catalogo_dao import CatalogoDAO
from dao_crud.cliente_dao import ClienteDAO
from dao_crud.vendedor_dao import VendedorDAO
from dao_crud.sucursal_dao import SucursalDAO
from dao_crud.repartidor_dao import RepartidorDAO
from dao_crud.direccion_dao import DireccionDAO
from utils.autenticacion import ServicioAutenticacion
from utils.impresion import s, l, ms, limpiar_consola
from utils.validaciones import pedir_texto, pedir_entero, pedir_flotante, confirmar_accion


# ==========================================
# FUNCIONES AUXILIARES DE CALCULO
# ==========================================
def recalcular_totales_pedido(num_pedido: int, pedido_dao: PedidoDAO, ped_prod_dao: Ped_ProdDAO):
    """
    Suma las partidas de ped_prod para ese pedido y actualiza cantArticulos, subtotal, IVA y total
    """
    partidas = ped_prod_dao.consultar_todas()
    total_articulos = 0
    subtotal = 0.0

    for item in partidas:
        if item._pedido == num_pedido:
            total_articulos += int(item._cantidad)
            subtotal += float(item._importe)

    iva = round(subtotal * 0.16, 2)
    total = round(subtotal + iva, 2)

    pedido_dao.actualizar_cantArticulos(num_pedido, total_articulos)
    pedido_dao.actualizar_subtotal(num_pedido, round(subtotal, 2))
    pedido_dao.actualizar_iva(num_pedido, iva)
    pedido_dao.actualizar_total(num_pedido, total)
    print(f"Totales actualizados -> Articulos: {total_articulos} | Subtotal: ${subtotal:.2f} | IVA: ${iva:.2f} | Total: ${total:.2f}")


# ==========================================
# SECCION 1: PEDIDOS Y DETALLE DE PRODUCTOS
# ==========================================
def listar_pedidos(pedido_dao: PedidoDAO):
    lista = pedido_dao.consultar_todas()
    s()
    l(80)
    print(" LISTADO DE PEDIDOS")
    l(80)
    if not lista:
        print("No hay pedidos registrados.")
        return
    for p in lista:
        print(p)


def agregar_productos_a_pedido(
    num_pedido: int,
    num_catalogo: int,
    pedido_dao: PedidoDAO,
    ped_prod_dao: Ped_ProdDAO,
    catalogo_dao: CatalogoDAO,
):
    """
    Permite capturar uno o varios productos dentro de un pedido y recalcula sus totales
    """
    while True:
        print(f"\nProductos disponibles en catalogo #{num_catalogo}:")
        productos = catalogo_dao.lista_productos(num_catalogo)
        if not productos:
            print("Este catalogo no tiene productos asignados.")
            break
        for prod in productos:
            print(prod)

        sku = pedir_texto("\nSKU del producto a agregar (ej. P001): ").upper()
        cantidad = pedir_entero("Cantidad: ")
        precio_unit = pedir_flotante("Precio unitario del catalogo: ")
        importe = round(cantidad * precio_unit, 2)

        ped_prod_dao.agregar(Ped_Prod(num_pedido, num_catalogo, sku, cantidad, precio_unit, importe))
        print(f"Producto {sku} agregado (Importe: ${importe:.2f}).")

        if not confirmar_accion("Deseas agregar otro producto a este pedido? (s/n): "):
            break

    recalcular_totales_pedido(num_pedido, pedido_dao, ped_prod_dao)


def gestionar_pedidos(
    auth: ServicioAutenticacion,
    pedido_dao: PedidoDAO,
    ped_prod_dao: Ped_ProdDAO,
    catalogo_dao: CatalogoDAO,
    cliente_dao: ClienteDAO,
    vendedor_dao: VendedorDAO,
    estado_pedido_dao: Estado_PedidoDAO,
    entrega_dao: EntregaDAO,
):
    user = auth.usuario_actual

    while True:
        limpiar_consola()
        l(55)
        print(" GESTION DE PEDIDOS")
        l(55)
        print("1. Listar pedidos")
        print("2. Ver detalle de productos por pedido")
        print("3. Registrar nuevo pedido")
        print("4. Agregar productos a un pedido existente")
        print("5. Actualizar estado o entrega de pedido")
        print("6. Eliminar pedido (solo ADMIN)")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_pedidos(pedido_dao)
                ms()
            elif op == "2":
                listar_pedidos(pedido_dao)
                num_ped = pedir_entero("\nNumero de pedido a consultar: ")
                s()
                encontrados = False
                for item in ped_prod_dao.consultar_todas():
                    if item._pedido == num_ped:
                        print(item)
                        encontrados = True
                if not encontrados:
                    print("Ese pedido no tiene productos registrados.")
                ms()
            elif op == "3":
                num_ped = pedir_entero("Numero de pedido: ")
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print("\nCatalogos disponibles:")
                for c in catalogo_dao.consultar_todas():
                    print(c)
                num_cat = pedir_entero("Numero de catalogo: ")

                if user.es_vendedor() and user.numEmpleado is not None:
                    num_vend = user.numEmpleado
                    print(f"Vendedor asignado automaticamente: Empleado #{num_vend}")
                else:
                    print("\nVendedores disponibles:")
                    for v in vendedor_dao.consultar_todas():
                        print(v)
                    num_vend = pedir_entero("Numero de empleado vendedor: ")

                print("\nEstados de pedido disponibles:")
                for ep in estado_pedido_dao.consultar_todas():
                    print(ep)
                estado_ped = pedir_texto("Codigo de estado de pedido (ej. PEN): ").upper()

                ent_in = input("Codigo de entrega asociada (Enter si aun no tiene): ").strip()
                entrega_id = int(ent_in) if ent_in != "" else None

                print("\nClientes disponibles:")
                for cli in cliente_dao.consultar_todas():
                    print(cli)
                num_cli = pedir_entero("Numero de cliente: ")

                nuevo_pedido = Pedido(
                    num_ped, fecha_actual, 0, 0.0, 0.0, 0.0,
                    num_cat, num_vend, estado_ped, entrega_id, num_cli
                )
                pedido_dao.agregar(nuevo_pedido)
                print("\nPedido creado. Ahora captura sus productos:")
                agregar_productos_a_pedido(num_ped, num_cat, pedido_dao, ped_prod_dao, catalogo_dao)
                ms()
            elif op == "4":
                listar_pedidos(pedido_dao)
                num_ped = pedir_entero("\nNumero de pedido: ")
                num_cat = pedir_entero("Numero de catalogo del pedido: ")
                agregar_productos_a_pedido(num_ped, num_cat, pedido_dao, ped_prod_dao, catalogo_dao)
                ms()
            elif op == "5":
                listar_pedidos(pedido_dao)
                num_ped = pedir_entero("\nNumero de pedido a actualizar: ")
                print("1. Estado del pedido | 2. Asignar codigo de entrega")
                campo = input("Elige una opcion: ").strip()
                if campo == "1":
                    for ep in estado_pedido_dao.consultar_todas():
                        print(ep)
                    nuevo_est = pedir_texto("Nuevo codigo de estado: ").upper()
                    pedido_dao.actualizar_estado_pedido(num_ped, nuevo_est)
                    print("Estado del pedido actualizado.")
                elif campo == "2":
                    for ent in entrega_dao.consultar_todas():
                        print(ent)
                    cod_ent = pedir_entero("Codigo de entrega: ")
                    pedido_dao.actualizar_entrega(num_ped, cod_ent)
                    print("Entrega vinculada al pedido.")
                else:
                    print("Opcion no valida.")
                ms()
            elif op == "6":
                if not user.es_admin():
                    print("Solo un administrador puede eliminar pedidos.")
                    ms()
                    continue
                listar_pedidos(pedido_dao)
                num_ped = pedir_entero("\nNumero de pedido a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este pedido? (s/n): "):
                    pedido_dao.eliminar(num_ped)
                    print("Pedido eliminado.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# SECCION 2: PAGOS
# ==========================================
def listar_pagos(pago_dao: PagoDAO):
    lista = pago_dao.consultar_todas()
    s()
    l(80)
    print(" REGISTRO DE PAGOS")
    l(80)
    if not lista:
        print("No hay pagos registrados.")
        return
    for pg in lista:
        print(pg)


def gestionar_pagos(
    auth: ServicioAutenticacion,
    pago_dao: PagoDAO,
    pedido_dao: PedidoDAO,
    cliente_dao: ClienteDAO,
):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE PAGOS")
        l(50)
        print("1. Listar pagos")
        print("2. Registrar nuevo pago")
        print("3. Actualizar concepto o monto de pago")
        print("4. Eliminar pago (solo ADMIN)")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_pagos(pago_dao)
                ms()
            elif op == "2":
                num_trans = pedir_entero("Numero de transaccion: ")
                concepto = pedir_texto("Concepto (ej. Anticipo pedido 1): ")
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                monto = pedir_flotante("Monto pagado: ")
                num_pago = pedir_entero("Numero de parcialidad/pago (ej. 1, 2): ")
                saldo = pedir_flotante("Saldo restante despues del pago: ")
                listar_pedidos(pedido_dao)
                num_ped = pedir_entero("Numero de pedido: ")
                print("\nClientes disponibles:")
                for c in cliente_dao.consultar_todas():
                    print(c)
                num_cli = pedir_entero("Numero de cliente: ")

                pago_dao.agregar(Pago(num_trans, concepto, fecha_actual, monto, num_pago, saldo, num_ped, num_cli))
                print("\nPago registrado correctamente.")
                ms()
            elif op == "3":
                listar_pagos(pago_dao)
                num_trans = pedir_entero("\nNumero de transaccion a modificar: ")
                print("1. Concepto | 2. Monto | 3. Saldo")
                campo = input("Campo a actualizar: ").strip()
                if campo == "1":
                    pago_dao.actualizar_concepto(num_trans, pedir_texto("Nuevo concepto: "))
                elif campo == "2":
                    pago_dao.actualizar_monto(num_trans, pedir_flotante("Nuevo monto: "))
                elif campo == "3":
                    pago_dao.actualizar_saldo(num_trans, pedir_flotante("Nuevo saldo: "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Pago actualizado.")
                ms()
            elif op == "4":
                if not auth.usuario_actual.es_admin():
                    print("Solo un administrador puede eliminar pagos.")
                    ms()
                    continue
                listar_pagos(pago_dao)
                num_trans = pedir_entero("\nNumero de transaccion a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este pago? (s/n): "):
                    pago_dao.eliminar(num_trans)
                    print("Pago eliminado.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# SECCION 3: ENTREGAS
# ==========================================
def listar_entregas(entrega_dao: EntregaDAO):
    lista = entrega_dao.consultar_todas()
    s()
    l(80)
    print(" LISTADO DE ENTREGAS")
    l(80)
    if not lista:
        print("No hay entregas registradas.")
        return
    for ent in lista:
        print(ent)


def gestionar_entregas(
    auth: ServicioAutenticacion,
    entrega_dao: EntregaDAO,
    estado_entrega_dao: Estado_EntregaDAO,
    sucursal_dao: SucursalDAO,
    repartidor_dao: RepartidorDAO,
    direccion_dao: DireccionDAO,
):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE ENTREGAS")
        l(50)
        print("1. Listar entregas")
        print("2. Registrar nueva entrega")
        print("3. Actualizar estado, confirmacion o repartidor")
        print("4. Eliminar entrega (solo ADMIN)")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_entregas(entrega_dao)
                ms()
            elif op == "2":
                codigo = pedir_entero("Codigo de entrega: ")
                fecha_ent = pedir_texto("Fecha programada de entrega (AAAA-MM-DD): ")
                confirmada = pedir_texto("Confirmacion (ej. Pendiente / Entrega confirmada): ")

                print("\nEstados de entrega disponibles:")
                for ee in estado_entrega_dao.consultar_todas():
                    print(ee)
                estado_ent = pedir_texto("Codigo de estado de entrega (ej. PRO): ").upper()

                print("\nSucursales disponibles:")
                for suc in sucursal_dao.consultar_todas():
                    print(suc)
                cod_suc = pedir_texto("Codigo de sucursal: ").upper()

                print("\nRepartidores disponibles:")
                for rep in repartidor_dao.consultar_todas():
                    print(rep)
                num_rep = pedir_entero("Numero de repartidor: ")

                print("\nDirecciones disponibles:")
                for d in direccion_dao.consultar_todas():
                    print(d)
                num_dir = pedir_entero("Numero de direccion: ")

                entrega_dao.agregar(Entrega(codigo, fecha_ent, confirmada, estado_ent, cod_suc, num_rep, num_dir))
                print("\nEntrega registrada correctamente.")
                ms()
            elif op == "3":
                listar_entregas(entrega_dao)
                codigo = pedir_entero("\nCodigo de entrega a actualizar: ")
                print("1. Estado de entrega | 2. Confirmacion | 3. Repartidor | 4. Fecha entrega")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    for ee in estado_entrega_dao.consultar_todas():
                        print(ee)
                    entrega_dao.actualizar_estado_entrega(codigo, pedir_texto("Nuevo codigo de estado: ").upper())
                elif campo == "2":
                    entrega_dao.actualizar_entrega_confirmada(codigo, pedir_texto("Nuevo texto de confirmacion: "))
                elif campo == "3":
                    for rep in repartidor_dao.consultar_todas():
                        print(rep)
                    entrega_dao.actualizar_repartidor(codigo, pedir_entero("Nuevo numero de repartidor: "))
                elif campo == "4":
                    entrega_dao.actualizar_fecha_entrega(codigo, pedir_texto("Nueva fecha (AAAA-MM-DD): "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Entrega actualizada.")
                ms()
            elif op == "4":
                if not auth.usuario_actual.es_admin():
                    print("Solo un administrador puede eliminar entregas.")
                    ms()
                    continue
                listar_entregas(entrega_dao)
                codigo = pedir_entero("\nCodigo de entrega a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar esta entrega? (s/n): "):
                    entrega_dao.eliminar(codigo)
                    print("Entrega eliminada.")
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()


# ==========================================
# SECCION 4: CATALOGO DE ESTADOS (SOLO ADMIN)
# ==========================================
def gestionar_estados(estado_pedido_dao: Estado_PedidoDAO, estado_entrega_dao: Estado_EntregaDAO):
    while True:
        limpiar_consola()
        l(55)
        print(" CATALOGOS DE ESTADOS (PEDIDOS Y ENTREGAS)")
        l(55)
        print("1. Listar estados de pedido")
        print("2. Agregar estado de pedido")
        print("3. Listar estados de entrega")
        print("4. Agregar estado de entrega")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                for ep in estado_pedido_dao.consultar_todas():
                    print(ep)
                ms()
            elif op == "2":
                cod = pedir_texto("Codigo (3 letras, ej. DEV): ").upper()
                desc = pedir_texto("Descripcion: ")
                estado_pedido_dao.agregar(Estado_Pedido(cod, desc))
                print("Estado de pedido agregado.")
                ms()
            elif op == "3":
                for ee in estado_entrega_dao.consultar_todas():
                    print(ee)
                ms()
            elif op == "4":
                cod = pedir_texto("Codigo (3 letras, ej. RET): ").upper()
                desc = pedir_texto("Descripcion: ")
                estado_entrega_dao.agregar(Estado_Entrega(cod, desc))
                print("Estado de entrega agregado.")
                ms()
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
def menu_operaciones(conexion, auth: ServicioAutenticacion):
    pedido_dao = PedidoDAO(conexion)
    ped_prod_dao = Ped_ProdDAO(conexion)
    pago_dao = PagoDAO(conexion)
    entrega_dao = EntregaDAO(conexion)
    estado_pedido_dao = Estado_PedidoDAO(conexion)
    estado_entrega_dao = Estado_EntregaDAO(conexion)
    catalogo_dao = CatalogoDAO(conexion)
    cliente_dao = ClienteDAO(conexion)
    vendedor_dao = VendedorDAO(conexion)
    sucursal_dao = SucursalDAO(conexion)
    repartidor_dao = RepartidorDAO(conexion)
    direccion_dao = DireccionDAO(conexion)

    es_admin = auth.usuario_actual.es_admin()

    while True:
        limpiar_consola()
        l(50)
        print(" MODULO: PEDIDOS, PAGOS Y ENTREGAS")
        l(50)
        print("1. Pedidos y Detalle de Productos")
        print("2. Pagos")
        print("3. Entregas")
        if es_admin:
            print("4. Configurar Estados de Pedido y Entrega")
        print("0. Volver al menu principal")

        op = input("\nElige una opcion: ").strip()
        if op == "1":
            gestionar_pedidos(
                auth, pedido_dao, ped_prod_dao, catalogo_dao,
                cliente_dao, vendedor_dao, estado_pedido_dao, entrega_dao
            )
        elif op == "2":
            gestionar_pagos(auth, pago_dao, pedido_dao, cliente_dao)
        elif op == "3":
            gestionar_entregas(
                auth, entrega_dao, estado_entrega_dao,
                sucursal_dao, repartidor_dao, direccion_dao
            )
        elif op == "4" and es_admin:
            gestionar_estados(estado_pedido_dao, estado_entrega_dao)
        elif op == "0":
            break
        else:
            print("Opcion no valida.")
            ms()