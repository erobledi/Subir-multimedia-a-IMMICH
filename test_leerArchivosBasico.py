from pathlib import Path



def get_api_key() -> str:
    # Si el archivo existe, leer la clave
    if API_FILE.exists():
        return API_FILE.read_text(encoding="utf-8").strip()

    # Si no existe, pedirla y guardarla
    key = input("Introduce la API key: ").strip()

    if not key:
        raise ValueError("La API key no puede estar vacía")

    API_FILE.write_text(key, encoding="utf-8")
    return key


# Uso
API_KEY = get_api_key()
print("API key cargada correctamente.")


def fun_readAPI() -> bool:
    try:
        key = get_api_key()
        print(f"La API key es: {key}")
        return True
    except Exception as e:
        print(f"Error al obtener la API key: {e}")
        return False

if __name__ == "__main__":
    API_FILE = Path("api_key.txt")  #// Ruta al archivo de la API key
    
    existeAPI = fun_readAPI()