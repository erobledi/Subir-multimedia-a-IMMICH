import os
from pathlib import Path
import config

def comprobar_ruta_local():
    # Cargar la configuración usando config.py
    archivoDatos = Path("datos.json")
    cfg = config.fun_leerArchivo(archivoDatos, debugJSON=True)

    if not cfg:
        raise SystemExit("No se pudo cargar la configuración desde datos.json")

    # Obtener la ruta local desde la configuración
    local_folder = cfg["ruta_local"]

    # Verificar si la ruta es accesible
    if not os.path.isdir(local_folder):
        raise SystemExit(f"La ruta local no existe o no es un directorio: {local_folder}")

    # Intentar listar el contenido de la carpeta
    try:
        archivos = os.listdir(local_folder)
        print(f"Contenido de '{local_folder}':")
        for archivo in archivos:
            print(f" - {archivo}")
    except Exception as e:
        raise SystemExit(f"Error al acceder a la ruta local: {e}")

if __name__ == "__main__":
    comprobar_ruta_local()
