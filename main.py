from conexion import Conexion
from menus.menu_principal import iniciar_sistema



def main():
    gestor_conexion = Conexion("localhost", "root", "", "catalog_uxpress")
    conexion_activa = gestor_conexion.conectar()

    if not conexion_activa:
        return

    try:
        iniciar_sistema(conexion_activa)

    finally: # hace que aunque ocurra un error inesperado, se cierre correctamente la conexion
        gestor_conexion.cerrar()


if __name__ == "__main__":
    main()