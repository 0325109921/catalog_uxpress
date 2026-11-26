from mysql.connector import Error
from clases.sucursal import Sucursal
from clases.producto import Producto
from clases.catalogo import Catalogo
from clases.cat_prod import Cat_Prod
from clases.stock import Stock
from dao_crud.sucursal_dao import SucursalDAO
from dao_crud.producto_dao import ProductoDAO
from dao_crud.catalogo_dao import CatalogoDAO
from dao_crud.cat_prod_dao import Cat_ProdDAO
from dao_crud.stock_dao import StockDAO
from utils.autenticacion import ServicioAutenticacion
from utils.impresion import s, l, ms, limpiar_consola, encabezado
from utils.validaciones import pedir_texto, pedir_entero, pedir_flotante, confirmar_accion


# ==========================================
# SECCION 1: SUCURSALES
# ==========================================
def listar_sucursales(sucursal_dao: SucursalDAO, sucursal=None):
    """ Si se indica 'sucursal' solo muestra esa (usado para el vendedor) """
    lista = sucursal_dao.consultar_todas() if sucursal is None else sucursal_dao.consultar_por_codigo(sucursal)
    s()
    l(65)
    print(" LISTADO DE SUCURSALES")
    l(65)
    if not lista:
        print("No hay sucursales registradas.")
        return
    encabezado(Sucursal.encabezado())
    for suc in lista:
        print(suc)


def elegir_sucursal(sucursal_dao: SucursalDAO):
    """ Muestra las sucursales y pide un codigo valido. Devuelve None si el usuario cancela con Enter """
    listar_sucursales(sucursal_dao)
    while True:
        codigo = input("\nCodigo de sucursal (Enter para cancelar): ").strip().upper()
        if codigo == "":
            return None
        if sucursal_dao.consultar_por_codigo(codigo):
            return codigo
        print("Esa sucursal no existe. Intenta de nuevo.")


def gestionar_sucursales(sucursal_dao: SucursalDAO):
    while True:
        limpiar_consola()
        l(45)
        print(" GESTION DE SUCURSALES")
        l(45)
        print("1. Listar sucursales")
        print("2. Agregar sucursal")
        print("3. Actualizar sucursal")
        print("4. Eliminar sucursal")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_sucursales(sucursal_dao)
                ms()
            elif op == "2":
                codigo = pedir_texto("Codigo de sucursal (ej. S04): ").upper()
                nombre = pedir_texto("Nombre: ")
                calle = pedir_texto("Calle: ")
                numero = pedir_texto("Numero exterior: ")
                colonia = pedir_texto("Colonia: ")
                nueva = Sucursal(codigo, nombre, calle, numero, colonia)
                sucursal_dao.agregar(nueva)
                print("\nSucursal registrada correctamente.")
                ms()
            elif op == "3":
                listar_sucursales(sucursal_dao)
                codigo = pedir_texto("\nCodigo de sucursal a modificar: ").upper()
                print("1. Nombre | 2. Calle | 3. Numero | 4. Colonia")
                campo = input("Campo a actualizar: ").strip()
                if campo == "1":
                    sucursal_dao.actualizar_nombre(codigo, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    sucursal_dao.actualizar_dir_calle(codigo, pedir_texto("Nueva calle: "))
                elif campo == "3":
                    sucursal_dao.actualizar_dir_numero(codigo, pedir_texto("Nuevo numero: "))
                elif campo == "4":
                    sucursal_dao.actualizar_dir_colonia(codigo, pedir_texto("Nueva colonia: "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Sucursal actualizada.")
                ms()
            elif op == "4":
                listar_sucursales(sucursal_dao)
                codigo = pedir_texto("\nCodigo de sucursal a eliminar: ").upper()
                if confirmar_accion("Seguro que deseas eliminar esta sucursal? (s/n): "):
                    sucursal_dao.eliminar(codigo)
                    print("Sucursal eliminada.")
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
# SECCION 2: PRODUCTOS
# ==========================================
def listar_productos(producto_dao: ProductoDAO, sucursal=None):
    """ Si se indica 'sucursal' solo muestra los productos que esa sucursal maneja (usado para el vendedor) """
    lista = producto_dao.consultar_todas() if sucursal is None else producto_dao.consultar_por_sucursal(sucursal)
    s()
    l(65)
    print(" CATALOGO GENERAL DE PRODUCTOS" if sucursal is None else f" PRODUCTOS DE LA SUCURSAL {sucursal}")
    l(65)
    if not lista:
        print("No hay productos registrados.")
        return
    encabezado(Producto.encabezado())
    for prod in lista:
        print(prod)


def gestionar_productos(producto_dao: ProductoDAO):
    while True:
        limpiar_consola()
        l(45)
        print(" GESTION DE PRODUCTOS")
        l(45)
        print("1. Listar productos")
        print("2. Agregar producto")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_productos(producto_dao)
                ms()
            elif op == "2":
                sku = pedir_texto("SKU del producto (ej. P016): ").upper()
                nombre = pedir_texto("Nombre: ")
                descripcion = pedir_texto("Descripcion: ")
                nuevo = Producto(sku, nombre, descripcion)
                producto_dao.agregar(nuevo)
                print("\nProducto registrado correctamente.")
                ms()
            elif op == "3":
                listar_productos(producto_dao)
                sku = pedir_texto("\nSKU del producto a modificar: ").upper()
                print("1. Nombre | 2. Descripcion")
                campo = input("Campo a actualizar: ").strip()
                if campo == "1":
                    producto_dao.actualizar_nombre(sku, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    producto_dao.actualizar_descripcion(sku, pedir_texto("Nueva descripcion: "))
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Producto actualizado.")
                ms()
            elif op == "4":
                listar_productos(producto_dao)
                sku = pedir_texto("\nSKU del producto a eliminar: ").upper()
                if confirmar_accion("Seguro que deseas eliminar este producto? (s/n): "):
                    producto_dao.eliminar(sku)
                    print("Producto eliminado.")
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
# SECCION 3: CATALOGOS Y PRECIOS (CAT_PROD)
# ==========================================
def listar_catalogos(catalogo_dao: CatalogoDAO, sucursal=None):
    """ Lista los catalogos ordenados por sucursal. Si se indica 'sucursal' solo muestra los de esa sucursal """
    lista = catalogo_dao.consultar_todas(sucursal)
    s()
    l(65)
    print(" LISTADO DE CATALOGOS")
    l(65)
    if not lista:
        print("No hay catalogos registrados.")
        return
    encabezado(Catalogo.encabezado())
    for c in lista:
        print(c)


def consultar_catalogos_detalle(sucursal_dao: SucursalDAO, catalogo_dao: CatalogoDAO, sucursal=None):
    """ Con 'sucursal' (vendedor) se usa esa sucursal directamente; sin ella (admin) se pregunta cual """
    if sucursal is None:
        listar_sucursales(sucursal_dao)
        cod_suc = pedir_texto("\nIngresa el codigo de sucursal para ver sus catalogos: ").upper()
    else:
        cod_suc = sucursal
    lineas_cat = catalogo_dao.catalogos_sucursal(cod_suc)

    s()
    if not lineas_cat:
        print(f"No hay catalogos registrados para la sucursal {cod_suc}.")
        return

    print(f"Catalogos en sucursal {cod_suc}:")
    encabezado(CatalogoDAO.encabezado_catalogos_sucursal())
    for linea in lineas_cat:
        print(linea)

    if confirmar_accion("\nDeseas ver los productos y precios de un catalogo? (s/n): "):
        num_cat = pedir_entero("Numero de catalogo: ")
        if str(num_cat) not in catalogo_dao.lista_catalogos(cod_suc):
            print(f"\nEl catalogo #{num_cat} no pertenece a la sucursal {cod_suc}.")
            return
        productos = catalogo_dao.lista_productos(num_cat)
        s()
        if not productos:
            print("Ese catalogo no tiene productos asignados.")
        else:
            print(f"Productos del catalogo #{num_cat}:")
            encabezado(CatalogoDAO.encabezado_productos())
            for p in productos:
                print(p)


def gestionar_catalogos(
    sucursal_dao: SucursalDAO,
    producto_dao: ProductoDAO,
    catalogo_dao: CatalogoDAO,
    cat_prod_dao: Cat_ProdDAO,
):
    while True:
        limpiar_consola()
        l(50)
        print(" GESTION DE CATALOGOS Y PRECIOS")
        l(50)
        print("1. Listar todos los catalogos")
        print("2. Consultar catalogos y productos por sucursal")
        print("3. Crear nuevo catalogo")
        print("4. Actualizar catalogo")
        print("5. Asignar producto con precio a un catalogo")
        print("6. Actualizar precio de producto en catalogo")
        print("7. Quitar producto de un catalogo")
        print("8. Eliminar catalogo")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                listar_catalogos(catalogo_dao)
                ms()
            elif op == "2":
                consultar_catalogos_detalle(sucursal_dao, catalogo_dao)
                ms()
            elif op == "3":
                nombre = pedir_texto("Nombre del catalogo: ")
                inicio = pedir_texto("Vigencia inicio (AAAA-MM-DD): ")
                fin = input("Vigencia fin (AAAA-MM-DD o Enter si no tiene): ").strip()
                vigencia_fin = fin if fin != "" else None
                listar_sucursales(sucursal_dao)
                sucursal = pedir_texto("Codigo de sucursal: ").upper()
                nuevo = Catalogo(None, nombre, inicio, vigencia_fin, sucursal)
                num_cat = catalogo_dao.agregar(nuevo)
                print(f"\nCatalogo creado correctamente con el numero {num_cat}.")
                ms()
            elif op == "4":
                listar_catalogos(catalogo_dao)
                num_cat = pedir_entero("\nNumero de catalogo a actualizar: ")
                print("1. Nombre | 2. Vigencia inicio | 3. Vigencia fin | 4. Sucursal")
                campo = input("Campo a modificar: ").strip()
                if campo == "1":
                    catalogo_dao.actualizar_nombre(num_cat, pedir_texto("Nuevo nombre: "))
                elif campo == "2":
                    catalogo_dao.actualizar_vigencia_inicio(num_cat, pedir_texto("Nueva fecha inicio (AAAA-MM-DD): "))
                elif campo == "3":
                    fin = input("Nueva fecha fin (AAAA-MM-DD o Enter para vacio): ").strip()
                    catalogo_dao.actualizar_vigencia_fin(num_cat, fin if fin != "" else None)
                elif campo == "4":
                    catalogo_dao.actualizar_sucursal(num_cat, pedir_texto("Nuevo codigo sucursal: ").upper())
                else:
                    print("Opcion no valida.")
                    ms()
                    continue
                print("Catalogo actualizado.")
                ms()
            elif op == "5":
                listar_catalogos(catalogo_dao)
                num_cat = pedir_entero("\nNumero de catalogo: ")
                listar_productos(producto_dao)
                sku = pedir_texto("SKU del producto: ").upper()
                precio = pedir_flotante("Precio en este catalogo: ")
                cat_prod_dao.agregar(Cat_Prod(num_cat, sku, precio))
                print("Producto agregado al catalogo.")
                ms()
            elif op == "6":
                num_cat = pedir_entero("Numero de catalogo: ")
                sku = pedir_texto("SKU del producto: ").upper()
                precio = pedir_flotante("Nuevo precio: ")
                cat_prod_dao.actualizar_precio(num_cat, sku, precio)
                print("Precio actualizado.")
                ms()
            elif op == "7":
                num_cat = pedir_entero("Numero de catalogo: ")
                sku = pedir_texto("SKU del producto a quitar: ").upper()
                if confirmar_accion("Quitar producto del catalogo? (s/n): "):
                    cat_prod_dao.eliminar(num_cat, sku)
                    print("Producto retirado del catalogo.")
                ms()
            elif op == "8":
                num_cat = pedir_entero("Numero de catalogo a eliminar: ")
                if confirmar_accion("Seguro que deseas eliminar este catalogo? (s/n): "):
                    catalogo_dao.eliminar(num_cat)
                    print("Catalogo eliminado.")
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
# SECCION 4: INVENTARIO / STOCK
# ==========================================
def listar_stock(stock_dao: StockDAO, sucursal: str):
    """ Muestra solo el stock de la sucursal indicada, con el nombre del producto junto a su SKU """
    lista = stock_dao.consultar_por_sucursal(sucursal)
    s()
    l(75)
    print(f" EXISTENCIAS EN STOCK - SUCURSAL {sucursal}")
    l(75)
    if not lista:
        print(f"No hay registros de stock para la sucursal {sucursal}.")
        return
    encabezado(Stock.encabezado())
    for st in lista:
        print(st)


def gestionar_stock(stock_dao: StockDAO, sucursal_dao: SucursalDAO, producto_dao: ProductoDAO):
    while True:
        limpiar_consola()
        l(45)
        print(" GESTION DE STOCK")
        l(45)
        print("1. Consultar stock")
        print("2. Registrar stock inicial")
        print("3. Actualizar cantidad en stock")
        print("4. Eliminar registro de stock")
        print("0. Volver")

        op = input("\nElige una opcion: ").strip()

        try:
            if op == "1":
                cod_suc = elegir_sucursal(sucursal_dao)
                if cod_suc is None:
                    continue
                listar_stock(stock_dao, cod_suc)
                ms()
            elif op == "2":
                cod_suc = elegir_sucursal(sucursal_dao)
                if cod_suc is None:
                    continue
                listar_productos(producto_dao)
                sku = pedir_texto("SKU del producto: ").upper()
                cantidad = pedir_entero("Cantidad en stock: ")
                stock_dao.agregar(Stock(cod_suc, sku, cantidad))
                print("Stock registrado.")
                ms()
            elif op == "3":
                cod_suc = elegir_sucursal(sucursal_dao)
                if cod_suc is None:
                    continue
                listar_stock(stock_dao, cod_suc)
                sku = pedir_texto("\nSKU del producto: ").upper()
                cantidad = pedir_entero("Nueva cantidad en stock: ")
                stock_dao.actualizar_stock(cod_suc, sku, cantidad)
                print("Stock actualizado.")
                ms()
            elif op == "4":
                cod_suc = elegir_sucursal(sucursal_dao)
                if cod_suc is None:
                    continue
                listar_stock(stock_dao, cod_suc)
                sku = pedir_texto("\nSKU del producto: ").upper()
                if confirmar_accion("Eliminar registro de stock? (s/n): "):
                    stock_dao.eliminar(cod_suc, sku)
                    print("Registro eliminado.")
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
def menu_catalogos(conexion, auth: ServicioAutenticacion, solo_lectura=False):
    sucursal_dao = SucursalDAO(conexion)
    producto_dao = ProductoDAO(conexion)
    catalogo_dao = CatalogoDAO(conexion)
    cat_prod_dao = Cat_ProdDAO(conexion)
    stock_dao = StockDAO(conexion)
    sucursal_usuario = auth.sucursal_permitida() # None para ADMIN, codigo de sucursal para VENDEDOR

    if solo_lectura:
        while True:
            limpiar_consola()
            l(50)
            print(" CONSULTA DE CATALOGOS, PRODUCTOS Y STOCK")
            l(50)
            print("1. Consultar sucursales")
            print("2. Consultar productos")
            print("3. Consultar catalogos y precios por sucursal")
            print("4. Consultar stock disponible")
            print("0. Volver al menu principal")

            op = input("\nElige una opcion: ").strip()
            if op == "1":
                listar_sucursales(sucursal_dao, sucursal_usuario)
                ms()
            elif op == "2":
                listar_productos(producto_dao, sucursal_usuario)
                ms()
            elif op == "3":
                consultar_catalogos_detalle(sucursal_dao, catalogo_dao, sucursal_usuario)
                ms()
            elif op == "4":
                listar_stock(stock_dao, sucursal_usuario)
                ms()
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()
    else:
        auth.exigir_admin()
        while True:
            limpiar_consola()
            l(50)
            print(" MODULO: CATALOGOS, PRODUCTOS Y STOCK (ADMIN)")
            l(50)
            print("1. Sucursales")
            print("2. Productos")
            print("3. Catalogos y Precios")
            print("4. Stock por Sucursal")
            print("0. Volver al menu principal")

            op = input("\nElige una opcion: ").strip()
            if op == "1":
                gestionar_sucursales(sucursal_dao)
            elif op == "2":
                gestionar_productos(producto_dao)
            elif op == "3":
                gestionar_catalogos(sucursal_dao, producto_dao, catalogo_dao, cat_prod_dao)
            elif op == "4":
                gestionar_stock(stock_dao, sucursal_dao, producto_dao)
            elif op == "0":
                break
            else:
                print("Opcion no valida.")
                ms()