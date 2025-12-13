from pathlib import Path
import json

#// Librerías para usar en immich
import os
import uuid
from datetime import datetime, timezone
#import requests


def fun_leerArchivo(archivoDatos) -> bool:
    try:

        #// Si el archivo no existe, se piden los datos por pantalla y se crea el archivo.
        if not archivoDatos.exists():
            print("El archivo no existe.")
            
            #// Se pide por pantalla los siguientes datos.
            url = input("Introduce la URL del servidor Immich: ").strip()
            apiKey = input("Introduce la API key: ").strip()
            directorio = input("Introduce el directorio donde están los archivos multimedia: ").strip()
            deviceID = input("Introduce el Device ID (dejar vacío para generar uno nuevo): ").strip()
            if not deviceID:
                deviceID = "windows-script-001"


            '''
            print(f"URL: {url}")
            print(f"API Key: {apiKey}")
            print(f"Directorio: {directorio}")
            print(f"Devide ID: {deviceID}")
            '''

            if not url or not apiKey or not directorio:
                raise ValueError("Todos los campos son obligatorios")
            

            config = {
                "immich_url": url,
                "api_key": apiKey,
                "ruta_local": directorio,
                "device_id": deviceID
            }

            with open(archivoDatos, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            print("Archivo datos.json creado correctamente.")


        #// Si el archivo ya existe, se lee y se devuelven los datos.
        if archivoDatos.exists():
            with open(archivoDatos, "r", encoding="utf-8") as f:
            
                return json.load(f)     


    except Exception as e:
        print(f"Error al obtener la API key: {e}")
        return False


def mostrar_config(config: dict) -> None:
    #print(f"Existe API: {config}")


    print("\nConfiguración cargada:")
    print("-" * 30)
    print(f"Servidor Immich  : {config.get('immich_url')}")
    print(f"API Key          : {config.get('api_key')}")
    print(f"Ruta local       : {config.get('ruta_local')}")
    print(f"Nombre del equipo: {config.get('device_id')}")
    print("-" * 30)



if __name__ == "__main__":
    archivoDatos = Path("datos.json")  #// Ruta al archivo de la API key
    
    config = fun_leerArchivo(archivoDatos)

    mostrar_config(config)


