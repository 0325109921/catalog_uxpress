""" Funciones de utilidad al momento de imprimir en consola"""
import os

def s():
    """ Imprime una linea vacia en consola.
        Usalo para separar textos """
    print("")

def l(n):
    """ Imprime una linea de '=' de una longitud de n carcateres """
    print("="*n)

def sls(n):
    """ Imprime una linea vacia, una linea de '=' de una longitud de n carcateres y una linea vacia.
        Usalo para separar temas en un texto. """
    s()
    l(n)
    s()

def ms():
    """ Crea un espacio que al presionar enter avanza a la siguiente seccion """
    esperar=input("Presione para continuar...")

def encabezado(columnas):
    """ Imprime la fila de titulos de una tabla y una linea de '-' del mismo largo debajo.
        Recibe el texto que devuelve el metodo encabezado() de cada clase. """
    print(columnas)
    print("-" * len(columnas))

def imprimir_tabla(columnas, filas, vacio="No hay registros."):
    """ Imprime el encabezado y despues cada fila. Si no hay filas muestra el mensaje 'vacio'. """
    if not filas:
        print(vacio)
        return
    encabezado(columnas)
    for fila in filas:
        print(fila)

def limpiar_consola():
    """Borra lo que se haya impreso antes en la consola.
       Utilizalo para separar partes en un menu y asi limitar la vision de los datos"""
    os.system("cls" if os.name == "nt" else "clear")

""" Para utilizar limpirar_consola() de manera efectiva se debe colocar al principio de un submenu
    y utilizar ms() al final para permitir al usuario ver los resultados de sus acciones"""