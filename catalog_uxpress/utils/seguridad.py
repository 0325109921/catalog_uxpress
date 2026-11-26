import hashlib
import hmac
import os

ITERACIONES = 200_000


def generar_hash(password):
    """Devuelve 'algoritmo$iteraciones$sal$hash' listo para guardar en la BD."""
    sal = os.urandom(16)
    derivado = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), sal, ITERACIONES)
    return f"pbkdf2_sha256${ITERACIONES}${sal.hex()}${derivado.hex()}"


def verificar_password(password, almacenado):
    """True si la contrasena escrita coincide con el hash guardado."""
    try:
        _, iteraciones, sal_hex, hash_hex = almacenado.split("$")
        derivado = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"),
            bytes.fromhex(sal_hex), int(iteraciones))
    except ValueError:
        return False
    return hmac.compare_digest(derivado.hex(), hash_hex)
