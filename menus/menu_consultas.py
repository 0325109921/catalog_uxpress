from mysql.connector import Error
from dao_crud.sucursal_dao import SucursalDAO
from dao_crud.catalogo_dao import CatalogoDAO
from dao_crud.pedido_dao import PedidoDAO
from utils.impresion import s, l, ms, limpiar_consola
from utils.validaciones import pedir_texto, pedir_entero


def consulta_1_productos_catalogo(conexion):
    sucursal_dao = SucursalDAO(conexion)
    catalogo_dao = CatalogoDAO(conexion)

    print("\nSucursales disponibles:")
    for suc in sucursal_dao.consultar_todas():
        print(suc)
    cod_suc = pedir_texto("\nCodigo de sucursal (ej. S01): ").upper()

    print("\nCatalogos disponibles:")
    for cat in catalogo_dao.consultar_todas():
        print(cat)
    num_cat = pedir_entero("\nNumero de catalogo: ")

    consulta = """
        SELECT
            s.nombre,
            c.nombre,
            DATE_FORMAT(c.vigenciaInicio, '%d-%m-%Y'),
            IFNULL(DATE_FORMAT(c.vigenciaFin, '%d-%m-%Y'), 'Sin fin'),
            p.nombre,
            cp.precio,
            st.cantStock
        FROM catalogo AS c
        INNER JOIN sucursal AS s ON c.sucursal = s.codigoSucursal
        INNER JOIN cat_prod AS cp ON cp.catalogo = c.numCatalogo
        INNER JOIN producto AS p ON p.SKU = cp.producto
        INNER JOIN stock AS st ON st.producto = p.SKU AND st.sucursal = s.codigoSucursal
        WHERE s.codigoSucursal = %s AND c.numCatalogo = %s
    """
    cursor = conexion.cursor()
    cursor.execute(consulta, (cod_suc, num_cat))
    filas = cursor.fetchall()

    s()
    if not filas:
        print("No se encontraron productos para esa sucursal y catalogo.")
        return

    l(95)
    print(f" SUCURSAL: {filas[0][0]} | CATALOGO: {filas[0][1]}")
    print(f" VIGENCIA: {filas[0][2]} al {filas[0][3]}")
    l(95)
    print(f"| {'PRODUCTO':<50} | {'PRECIO':<14} | {'STOCK':<10} |")
    l(95)
    for _, _, _, _, prod, precio, stock in filas:
        print(f"| {prod:<50} | ${float(precio):<13.2f} | {stock:<10} |")
    l(95)


def consulta_2_info_pedido(conexion):
    pedido_dao = PedidoDAO(conexion)
    print("\nPedidos registrados:")
    for p in pedido_dao.consultar_todas():
        print(p)
    num_ped = pedir_entero("\nNumero de pedido a consultar: ")

    consulta = """
        SELECT
            p.numPedido,
            DATE_FORMAT(p.fecha, '%d-%m-%Y'),
            CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')),
            IFNULL(CONCAT(d.calle, ', ', d.numero, ', ', d.colonia), 'Sin direccion asignada'),
            CONCAT(v.nombrePila, ' ', v.primerApell, ' ', IFNULL(v.segundoApell, '')),
            pr.SKU,
            pr.nombre,
            pp.cantidad,
            pp.precioUnitario,
            pp.importe,
            p.subtotal,
            p.IVA,
            p.total
        FROM pedido AS p
        INNER JOIN cliente AS c ON p.cliente = c.numCliente
        LEFT JOIN entrega AS e ON p.entrega = e.codigo
        LEFT JOIN direccion AS d ON e.direccion = d.numDireccion
        INNER JOIN vendedor AS v ON p.vendedor = v.numEmpleado
        INNER JOIN ped_prod AS pp ON pp.pedido = p.numPedido
        INNER JOIN producto AS pr ON pp.producto = pr.SKU
        WHERE p.numPedido = %s
    """
    cursor = conexion.cursor()
    cursor.execute(consulta, (num_ped,))
    filas = cursor.fetchall()

    s()
    if not filas:
        print("No se encontro detalle de productos para ese pedido.")
        return

    enc = filas[0]
    l(92)
    print(f" PEDIDO #{enc[0]} | FECHA: {enc[1]}")
    print(f" CLIENTE: {enc[2]}")
    print(f" DIRECCION ENTREGA: {enc[3]}")
    print(f" VENDEDOR: {enc[4]}")
    l(92)
    print(f"| {'SKU':<8} | {'PRODUCTO':<37} | {'CANT':<5} | {'P. UNIT':<10} | {'IMPORTE':<10} |")
    l(92)
    for fila in filas:
        print(f"| {fila[5]:<8} | {fila[6]:<37} | {fila[7]:<5} | ${float(fila[8]):<9.2f} | ${float(fila[9]):<9.2f} |")
    l(92)
    print(f" SUBTOTAL: ${float(enc[10]):.2f} | IVA: ${float(enc[11]):.2f} | TOTAL: ${float(enc[12]):.2f}")
    l(92)


def consulta_3_pago_pedido(conexion):
    num_ped = pedir_entero("\nNumero de pedido para consultar sus pagos: ")

    consulta = """
        SELECT
            pg.numTransaccion,
            pg.numeroPago,
            DATE_FORMAT(pg.fecha, '%d-%m-%Y'),
            pg.pedido,
            CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')),
            pg.concepto,
            pg.monto
        FROM pago AS pg
        INNER JOIN cliente AS c ON pg.cliente = c.numCliente
        WHERE pg.pedido = %s
    """
    cursor = conexion.cursor()
    cursor.execute(consulta, (num_ped,))
    filas = cursor.fetchall()

    s()
    if not filas:
        print("No hay pagos registrados para ese pedido.")
        return

    l(85)
    print(f" PAGOS DEL PEDIDO #{filas[0][3]} | CLIENTE: {filas[0][4]}")
    l(85)
    print(f"| {'TRANSACCION':<12} | {'# PAGO':<7} | {'FECHA':<12} | {'CONCEPTO':<25} | {'MONTO':<12} |")
    l(85)
    for trans, num_p, fecha, _, _, conc, monto in filas:
        print(f"| {trans:<12} | {num_p:<7} | {fecha:<12} | {conc:<25} | ${float(monto):<11.2f} |")
    l(85)


def consulta_4_entrega_pedido(conexion):
    num_ped = pedir_entero("\nNumero de pedido para consultar su entrega: ")

    consulta = """
        SELECT
            e.codigo,
            p.numPedido,
            DATE_FORMAT(p.fecha, '%d-%m-%Y'),
            DATE_FORMAT(e.fechaEntrega, '%d-%m-%Y'),
            CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')),
            CONCAT(d.calle, ', ', d.numero, ', ', d.colonia),
            CONCAT(r.nombrePila, ' ', r.primerApell, ' ', IFNULL(r.segundoApell, ''))
        FROM pedido AS p
        INNER JOIN entrega AS e ON p.entrega = e.codigo
        INNER JOIN cliente AS c ON p.cliente = c.numCliente
        INNER JOIN direccion AS d ON e.direccion = d.numDireccion
        INNER JOIN repartidor AS r ON e.repartidor = r.numRepartidor
        WHERE p.numPedido = %s
    """
    cursor = conexion.cursor()
    cursor.execute(consulta, (num_ped,))
    fila = cursor.fetchone()

    s()
    if not fila:
        print("Ese pedido no tiene entrega asignada o no existe.")
        return

    l(75)
    print(" INFORMACION DE ENTREGA DEL PEDIDO")
    l(75)
    print(f" Numero de entrega   : {fila[0]}")
    print(f" Numero de pedido    : {fila[1]}")
    print(f" Fecha del pedido    : {fila[2]}")
    print(f" Fecha de entrega    : {fila[3]}")
    print(f" Cliente             : {fila[4]}")
    print(f" Direccion entrega   : {fila[5]}")
    print(f" Repartidor          : {fila[6]}")
    l(75)


def consulta_5_pedidos_sucursal_periodo(conexion):
    sucursal_dao = SucursalDAO(conexion)
    print("\nSucursales disponibles:")
    for suc in sucursal_dao.consultar_todas():
        print(suc)

    cod_suc = pedir_texto("\nCodigo de sucursal (ej. S01): ").upper()
    fecha_ini = pedir_texto("Fecha inicial (AAAA-MM-DD): ")
    fecha_fin = pedir_texto("Fecha final (AAAA-MM-DD): ")

    consulta = """
        SELECT
            s.nombre,
            p.numPedido,
            DATE_FORMAT(p.fecha, '%d-%m-%Y'),
            CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')),
            p.total,
            DATE_FORMAT(e.fechaEntrega, '%d-%m-%Y'),
            ee.descripcion
        FROM pedido AS p
        INNER JOIN catalogo AS cat ON p.catalogo = cat.numCatalogo
        INNER JOIN sucursal AS s ON cat.sucursal = s.codigoSucursal
        INNER JOIN cliente AS c ON p.cliente = c.numCliente
        INNER JOIN entrega AS e ON p.entrega = e.codigo
        INNER JOIN estado_entrega AS ee ON e.estadoEntrega = ee.codigo
        WHERE s.codigoSucursal = %s AND DATE(p.fecha) BETWEEN %s AND %s
        ORDER BY p.fecha
    """
    cursor = conexion.cursor()
    cursor.execute(consulta, (cod_suc, fecha_ini, fecha_fin))
    filas = cursor.fetchall()

    s()
    if not filas:
        print("No se encontraron pedidos en esa sucursal para ese rango de fechas.")
        return

    l(105)
    print(f" PEDIDOS DE SUCURSAL: {filas[0][0]} ({fecha_ini} a {fecha_fin}) | TOTAL REGISTROS: {len(filas)}")
    l(105)
    print(f"| {'PEDIDO':<6} | {'FECHA PED.':<12} | {'CLIENTE':<30} | {'MONTO TOTAL':<12} | {'ENTREGA':<12} | {'ESTADO':<16} |")
    l(105)
    for _, num_p, f_ped, cli, total, f_ent, est in filas:
        print(f"| {num_p:<6} | {f_ped:<12} | {cli:<30} | ${float(total):<11.2f} | {str(f_ent):<12} | {est:<16} |")
    l(105)


def menu_consultas(conexion):
    while True:
        limpiar_consola()
        l(60)
        print(" REPORTES Y CONSULTAS DEL SISTEMA")
        l(60)
        print("1. Productos de un catalogo de una sucursal")
        print("2. Informacion completa de un pedido")
        print("3. Informacion del pago de un pedido")
        print("4. Informacion de la entrega de un pedido")
        print("5. Pedidos por sucursal en un periodo de tiempo")
        print("0. Volver al menu principal")

        op = input("\nElige una consulta: ").strip()

        try:
            if op == "1":
                consulta_1_productos_catalogo(conexion)
                ms()
            elif op == "2":
                consulta_2_info_pedido(conexion)
                ms()
            elif op == "3":
                consulta_3_pago_pedido(conexion)
                ms()
            elif op == "4":
                consulta_4_entrega_pedido(conexion)
                ms()
            elif op == "5":
                consulta_5_pedidos_sucursal_periodo(conexion)
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
        except Error as e:
            print(f"\nError de base de datos: {e}")
            ms()