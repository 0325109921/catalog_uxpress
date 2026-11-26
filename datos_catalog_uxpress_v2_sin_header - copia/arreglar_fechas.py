import csv
from datetime import datetime

archivos = [
    ("15_entrega.csv", 1, "%Y-%m-%d"),           # columna 1 es fechaEntrega (DATE)
    ("18_pedido.csv", 1, "%Y-%m-%d %H:%M:%S"),   # columna 1 es fecha (DATETIME)
    ("20_pago.csv", 2, "%Y-%m-%d %H:%M:%S"),     # columna 2 es fecha (DATETIME)
]

formatos_entrada = [
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%m/%d/%Y %H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y %H:%M:%S",
]

def convertir_fecha(texto, formato_salida):
    texto = texto.strip()
    for fmt in formatos_entrada:
        try:
            dt = datetime.strptime(texto, fmt)
            return dt.strftime(formato_salida)
        except ValueError:
            continue
    return texto  # si ya estaba en formato YYYY-MM-DD, la deja igual

for nombre, col_idx, fmt_salida in archivos:
    with open(nombre, "r", encoding="utf-8", newline="") as f:
        filas = list(csv.reader(f))

    for fila in filas:
        if len(fila) > col_idx:
            fila[col_idx] = convertir_fecha(fila[col_idx], fmt_salida)

    with open(nombre, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(filas)

    print(f"Listo: {nombre}")