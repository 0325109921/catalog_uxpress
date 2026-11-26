from pathlib import Path

""" Path absoluto para importar ascii-art.txt"""
RUTA_LOGO = Path(__file__).resolve().parent / "ascii-art.txt"

def imprimir_logo():
    """ Metodo que imprime el arte ascii dle logo del proyecto """
    try:
        print(RUTA_LOGO.read_text(encoding="utf-8"))
    except FileNotFoundError:
        # El logo es solo decoracion: si falta el archivo, el programa no se detendra.
        print("CATALOG UXPRESS")