from datetime import datetime
from mysql.connector import Error
from clases.pedido import Pedido
from clases.ped_prod import Ped_Prod
from clases.pago import Pago
from clases.entrega import Entrega
from clases.estado_pedido import Estado_Pedido
from clases.estado_entrega import Estado_Entrega
from clases.cliente import Cliente
from clases.vendedor import Vendedor
from clases.sucursal import Sucursal
from clases.repartidor import Repartidor
from clases.direccion import Direccion
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
from menus.menu_catalogos import listar_catalogos
from utils.autenticacion import ServicioAutenticacion
from utils.impresion import s, l, ms, limpiar_consola, encabezado, imprimir_tabla
from utils.validaciones import pedir_texto, pedir_entero, pedir_flotante, confirmar_accion


# ==========================================
# FUNCIONES AUXILIARES DE CALCULO
# ==========================================
def recalcular_totales_pedido(num_pedido: int, pedido_dao: PedidoDAO, ped_prod_dao: Ped_ProdDAO):
    """
    Suma las partidas de ped_prod para ese pedido y actualiza cantArticulos, subtotal, IVA y total
    """
    partidas = ped_prod_dao.consultar_por_pedido(num_pedido)
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
def listar_pedidos(pedido_dao: PedidoDAO, sucursal=None):
    """ Si se indica 'sucursal' solo muestra los pedidos de esa sucursal (usado para el vendedor) """
    lista = pedido_dao.consultar_todas(sucursal)
    s()
    l(80)
    print(" LISTADO DE PEDIDOS")
    l(80)
    if not lista:
        print("No hay pedidos registrados.")
        return
    encabezado(Pedido.encabezado())
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
    agregados = 0
    while True:
        print(f"\nProductos disponibles en catalogo #{num_catalogo}:")
        productos = catalogo_dao.lista_productos(num_catalogo)
        if not productos:
            print("Este catalogo no tiene productos asignados.")
            break
        encabezado(CatalogoDAO.encabezado_productos())
        for prod in productos:
            print(prod)

        sku = pedir_texto("\nSKU del producto a agregar (ej. P001): ").upper()
        precio_unit = catalogo_dao.precio_producto(num_catalogo, sku) # el precio sale del catalogo, no se captura
        if precio_unit is None:
            print(f"El SKU {sku} no esta en el catalogo #{num_catalogo}. Intenta de nuevo.")
            continue
        print(f"Precio unitario del catalogo: ${precio_unit:.2f}")
        cantidad = pedir_entero("Cantidad: ")
        importe = round(cantidad * precio_unit, 2)

        ped_prod_dao.agregar(Ped_Prod(num_pedido, num_catalogo, sku, cantidad, precio_unit, importe))
        agregados += 1
        print(f"Producto {sku} agregado (Importe: ${importe:.2f}).")

        if not confirmar_accion("Deseas agregar otro producto a este pedido? (s/n): "):
            break

    if agregados > 0:
        recalcular_totales_pedido(num_pedido, pedido_dao, ped_prod_dao)
    return agregados


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
    sucursal = auth.sucursal_permitida() # None para ADMIN, codigo de sucursal para VENDEDOR

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
                listar_pedidos(pedido_dao, sucursal)
                ms()
            elif op == "2":
                listar_pedidos(pedido_dao, sucursal)
                num_ped = pedir_entero("\nNumero de pedido a consultar: ")
                if sucursal is not None and not pedido_dao.pertenece_a_sucursal(num_ped, sucursal):
                    print("Ese pedido no pertenece a tu sucursal.")
                    ms()
                    continue
                s()
                partidas = ped_prod_dao.consultar_por_pedido(num_ped)
                if not partidas:
                    print("Ese pedido no tiene productos registrados.")
                else:
                    encabezado(Ped_Prod.encabezado())
                    for item in partidas:
                        print(item)
                ms()
            elif op == "3":
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print("\nCatalogos disponibles:")
                listar_catalogos(catalogo_dao, sucursal)
                num_cat = pedir_entero("Numero de catalogo: ")
                if sucursal is not None and str(num_cat) not in catalogo_dao.lista_catalogos(sucursal):
                    print("Ese catalogo no pertenece a tu sucursal.")
                    ms()
                    continue

                if user.es_vendedor() and user.numEmpleado is not None:
                    num_vend = user.numEmpleado
                    print(f"Vendedor asignado automaticamente: Empleado #{num_vend}")
                else:
                    print("\nVendedores disponibles:")
                    imprimir_tabla(Vendedor.encabezado(), vendedor_dao.consultar_todas())
                    num_vend = pedir_entero("Numero de empleado vendedor: ")

                print("\nEstados de pedido disponibles:")
                imprimir_tabla(Estado_Pedido.encabezado(), estado_pedido_dao.consultar_todas())
                estado_ped = pedir_texto("Codigo de estado de pedido (ej. REG): ").upper()

                print("\nEntregas disponibles:")
                imprimir_tabla(Entrega.encabezado(), entrega_dao.consultar_todas(sucursal))
                ent_in = input("Codigo de entrega asociada (Enter si aun no tiene): ").strip()
                if ent_in != "" and not ent_in.isdigit():
                    print("Codigo de entrega invalido.")
                    ms()
                    continue
                entrega_id = int(ent_in) if ent_in != "" else None
                if entrega_id is not None and sucursal is not None and not entrega_dao.pertenece_a_sucursal(entrega_id, sucursal):
                    print("Esa entrega no pertenece a tu sucursal.")
                    ms()
                    continue

                print("\nClientes disponibles:")
                imprimir_tabla(Cliente.encabezado(), cliente_dao.consultar_todas())
                num_cli = pedir_entero("Numero de cliente: ")

                # cantArticulos tiene CHECK (> 0): se crea con 1 y se recalcula al capturar los productos
                nuevo_pedido = Pedido(
                    None, fecha_actual, 1, 0.0, 0.0, 0.0,
                    num_cat, num_vend, estado_ped, entrega_id, num_cli
                )
                num_ped = pedido_dao.agregar(nuevo_pedido)
                print(f"\nPedido #{num_ped} creado. Ahora captura sus productos:")
                try:
                    agregar_productos_a_pedido(num_ped, num_cat, pedido_dao, ped_prod_dao, catalogo_dao)
                finally:
                    if not ped_prod_dao.consultar_por_pedido(num_ped): # un pedido sin productos no tiene sentido
                        pedido_dao.eliminar(num_ped)
                        print("\nEl pedido se elimino porque no se le registro ningun producto.")
                ms()
            elif op == "4":
                listar_pedidos(pedido_dao, sucursal)
                num_ped = pedir_entero("\nNumero de pedido: ")
                if sucursal is not None and not pedido_dao.pertenece_a_sucursal(num_ped, sucursal):
                    print("Ese pedido no pertenece a tu sucursal.")
                    ms()
                    continue
                num_cat = pedir_entero("Numero de catalogo del pedido: ")
                agregar_productos_a_pedido(num_ped, num_cat, pedido_dao, ped_prod_dao, catalogo_dao)
                ms()
            elif op == "5":
                listar_pedidos(pedido_dao, sucursal)
                num_ped = pedir_entero("\nNumero de pedido a actualizar: ")
                if sucursal is not None and not pedido_dao.pertenece_a_sucursal(num_ped, sucursal):
                    print("Ese pedido no pertenece a tu sucursal.")
                    ms()
                    continue
                print("1. Estado del pedido | 2. Asignar codigo de entrega")
                campo = input("Elige una opcion: ").strip()
                if campo == "1":
                    imprimir_tabla(Estado_Pedido.encabezado(), estado_pedido_dao.consultar_todas())
                    nuevo_est = pedir_texto("Nuevo codigo de estado: ").upper()
                    pedido_dao.actualizar_estado_pedido(num_ped, nuevo_est)
                    print("Estado del pedido actualizado.")
                elif campo == "2":
                    imprimir_tabla(Entrega.encabezado(), entrega_dao.consultar_todas(sucursal))
                    cod_ent = pedir_entero("Codigo de entrega: ")
                    if sucursal is not None and not entrega_dao.pertenece_a_sucursal(cod_ent, sucursal):
                        print("Esa entrega no pertenece a tu sucursal.")
                        ms()
                        continue
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
def listar_pagos(pago_dao: PagoDAO, sucursal=None):
    """ Si se indica 'sucursal' solo muestra los pagos de pedidos de esa sucursal (usado para el vendedor) """
    lista = pago_dao.consultar_todas(sucursal)
    s()
    l(80)
    print(" REGISTRO DE PAGOS")
    l(80)
    if not lista:
        print("No hay pagos registrados.")
        return
    encabezado(Pago.encabezado())
    for pg in lista:
        print(pg)


def gestionar_pagos(
    auth: ServicioAutenticacion,
    pago_dao: PagoDAO,
    pedido_dao: PedidoDAO,
    cliente_dao: ClienteDAO,
):
    sucursal = auth.sucursal_permitida() # None para ADMIN, codigo de sucursal para VENDEDOR

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
                listar_pagos(pago_dao, sucursal)
                ms()
            elif op == "2":
                concepto = pedir_texto("Concepto (ej. Anticipo pedido 1): ")
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                monto = pedir_flotante("Monto pagado: ")
                num_pago = pedir_entero("Numero de parcialidad/pago (ej. 1, 2): ")
                saldo = pedir_flotante("Saldo restante despues del pago: ")
                listar_pedidos(pedido_dao, sucursal)
                num_ped = pedir_entero("Numero de pedido: ")
                if sucursal is not None and not pedido_dao.pertenece_a_sucursal(num_ped, sucursal):
                    print("Ese pedido no pertenece a tu sucursal.")
                    ms()
                    continue
                print("\nClientes disponibles:")
                imprimir_tabla(Cliente.encabezado(), cliente_dao.consultar_todas())
                num_cli = pedir_entero("Numero de cliente: ")

                num_trans = pago_dao.agregar(Pago(None, concepto, fecha_actual, monto, num_pago, saldo, num_ped, num_cli))
                print(f"\nPago registrado correctamente con el numero de transaccion {num_trans}.")
                ms()
            elif op == "3":
                listar_pagos(pago_dao, sucursal)
                num_trans = pedir_entero("\nNumero de transaccion a modificar: ")
                if sucursal is not None and not pago_dao.pertenece_a_sucursal(num_trans, sucursal):
                    print("Ese pago no pertenece a tu sucursal.")
                    ms()
                    continue
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
def listar_entregas(entrega_dao: EntregaDAO, sucursal=None):
    """ Si se indica 'sucursal' solo muestra las entregas de esa sucursal (usado para el vendedor) """
    lista = entrega_dao.consultar_todas(sucursal)
    s()
    l(80)
    print(" LISTADO DE ENTREGAS")
    l(80)
    if not lista:
        print("No hay entregas registradas.")
        return
    encabezado(Entrega.encabezado())
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
    sucursal = auth.sucursal_permitida() # None para ADMIN, codigo de sucursal para VENDEDOR

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
                listar_entregas(entrega_dao, sucursal)
                ms()
            elif op == "2":
                fecha_ent = pedir_texto("Fecha programada de entrega (AAAA-MM-DD): ")
                confirmada = 1 if confirmar_accion("Entrega confirmada? (s/n): ") else 0

                print("\nEstados de entrega disponibles:")
                imprimir_tabla(Estado_Entrega.encabezado(), estado_entrega_dao.consultar_todas())
                estado_ent = pedir_texto("Codigo de estado de entrega (ej. PEN): ").upper()

                if sucursal is not None:
                    cod_suc = sucursal
                    print(f"\nSucursal asignada automaticamente: {cod_suc}")
                else:
                    print("\nSucursales disponibles:")
                    imprimir_tabla(Sucursal.encabezado(), sucursal_dao.consultar_todas())
                    cod_suc = pedir_texto("Codigo de sucursal: ").upper()

                print("\nRepartidores disponibles:")
                imprimir_tabla(Repartidor.encabezado(), repartidor_dao.consultar_todas())
                num_rep = pedir_entero("Numero de repartidor: ")

                print("\nDirecciones disponibles:")
                imprimir_tabla(Direccion.encabezado(), direccion_dao.consultar_todas())
                num_dir = pedir_entero("Numero de direccion: ")

                codigo = entrega_dao.agregar(Entrega(None, fecha_ent, confirmada, estado_ent, cod_suc, num_rep, num_dir))
                print(f"\nEntrega registrada correctamente con el codigo {codigo}.")
                ms()
            elif op == "3":
                listar_entregas(entrega_dao, sucursal)
                codigo = pedir_entero("\nCodigo de entrega a actualizar: ")
                if sucursal is not None and not entrega_dao.pertenece_a_sucursal(codigo, sucursal):
                    print("Esa entrega no pertenece a tu sucursal.")
                    ms()
                    continue
                print("1. Estado de entrega | 2. Confirmacion | 3. Repartidor | 4. Fecha entrega")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    imprimir_tabla(Estado_Entrega.encabezado(), estado_entrega_dao.consultar_todas())
                    entrega_dao.actualizar_estado_entrega(codigo, pedir_texto("Nuevo codigo de estado: ").upper())
                elif campo == "2":
                    entrega_dao.actualizar_entrega_confirmada(codigo, 1 if confirmar_accion("Entrega confirmada? (s/n): ") else 0)
                elif campo == "3":
                    imprimir_tabla(Repartidor.encabezado(), repartidor_dao.consultar_todas())
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
                imprimir_tabla(Estado_Pedido.encabezado(), estado_pedido_dao.consultar_todas())
                ms()
            elif op == "2":
                cod = pedir_texto("Codigo (3 letras, ej. DEV): ").upper()
                desc = pedir_texto("Descripcion: ")
                estado_pedido_dao.agregar(Estado_Pedido(cod, desc))
                print("Estado de pedido agregado.")
                ms()
            elif op == "3":
                imprimir_tabla(Estado_Entrega.encabezado(), estado_entrega_dao.consultar_todas())
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