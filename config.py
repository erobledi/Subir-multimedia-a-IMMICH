from pathlib import Path
import json


def fun_validarInput(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("❌ Este campo no puede estar vacío. Inténtalo de nuevo.")


def fun_leerArchivo(archivoDatos, debugJSON=True) -> bool:
    '''
    Docstring para fun_leerArchivo
    
    :param archivoDatos: Ruta donde se guarda el archivo datos.json.
    :param debugJSON: Activar mensajes de depuración (True/False).
    :return: Descripción
    '''


    try:

        #// Si el archivo no existe, se piden los datos por pantalla y se crea el archivo.
        if not archivoDatos.exists():
            print("El archivo no existe.")
            
            #// Se pide por pantalla los siguientes datos.
            
            #// Url del servidor Immich:
            url = fun_validarInput("Introduce la URL del servidor Immich: ")
            
            #// API Key del servidor Immich:
            apiKey = fun_validarInput("Introduce la API key: ")
            
            #// Directorio local donde están los archivos multimedia:
            directorio = fun_validarInput("Introduce el directorio donde están los archivos multimedia: ")
            
            #// Device ID (identificador del equipo que sube los archivos):
            deviceID = input("Introduce el Device ID (dejar vacío para generar uno nuevo): ").strip()
            
            if not deviceID:
                deviceID = "windows-script-001"

            #// Pausa entre archivos (segundos):
            pausa_txt = fun_validarInput("Pausa entre archivos en segundos (por defecto 0.7): ").strip()
            try:
                pausa_segundos = float(pausa_txt) if pausa_txt else 0.7
            except ValueError:
                pausa_segundos = 0.7

            #// Verificar en el servidor si el archivo ya existe:
            verificar_txt = input("Verificar en servidor si ya existe (S/N, por defecto S): ").strip().lower()
            verificar_con_servidor = False if verificar_txt == "n" else True


            if not url or not apiKey or not directorio:
                raise ValueError("Todos los campos son obligatorios")
            

            config = {
                "immich_url": url,
                "api_key": apiKey,
                "ruta_local": directorio,
                "device_id": deviceID,
                "pausa_segundos": pausa_segundos,
                "verificar_con_servidor": verificar_con_servidor,
            }

            with open(archivoDatos, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            print("Archivo datos.json creado correctamente.")


        #// Si el archivo ya existe, se lee y se devuelven los datos.
        if archivoDatos.exists():
            with open(archivoDatos, "r", encoding="utf-8") as f:
                config = json.load(f)

            
                if debugJSON == True:
                    fun_mostrarConfig(config)

                return config     


    except Exception as e:
        print(f"Error al obtener la API key: {e}")
        return False


def fun_mostrarConfig(config: dict) -> None:
    #print(f"Existe API: {config}")


    print("\nConfiguración cargada:")
    print("-" * 30)
    print(f"Servidor Immich         : {config.get('immich_url')}")
    print(f"API Key                 : {config.get('api_key')}")
    print(f"Ruta local              : {config.get('ruta_local')}")
    print(f"Nombre del equipo       : {config.get('device_id')}")
    print(f"Pausa entre cada subida : {config.get('pausa_segundos')} segundos")
    print(f"Verificar con servidor  : {config.get('verificar_con_servidor')}")
    print("-" * 30)