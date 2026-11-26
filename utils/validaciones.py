from datetime import datetime # libreria para trabajar con fechas y horas
"""
El objetivo de este archivo es servir como escudo entre el teclado del usuario
y la base de datos: si alguien escribe letras donde va un número o una fecha inventada, 
el programa no se cae con un error

"""

def pedir_texto(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip() # el .strip quita espacios accidentales al principio o al final
        if valor or not obligatorio:
            return valor
        print("Este campo no puede quedar vacio. Intenta de nuevo")


def pedir_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("Entrada invalida. Ingresa un numero entero")


def pedir_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Entrada invalida. Ingresa un numero decimal (ejemplo: 15.67)")


def pedir_fecha(mensaje: str = "Fecha (AAAA-MM-DD): ") -> str: # es el formato de mysql estandar para las fechas (YYYY-MM-DD)
    while True:
        valor = input(mensaje).strip()
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            print("Formato inválido. Usa AAAA-MM-DD (ejemplo: 1997-07-10)")


def confirmar_accion(mensaje: str = "¿Confirmar operacion? (s/n): ") -> bool:
    while True:
        resp = input(mensaje).strip().lower() # el .lower ayuda convierte la respuesta eb minusculas
        if resp in ("s", "si", "sí"):
            return True
        if resp in ("n", "no"):
            return False
        print("Responde 's' para si o 'n' para no")