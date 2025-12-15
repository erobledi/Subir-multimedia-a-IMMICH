import os
import uuid
from datetime import datetime, timezone
import requests

# ==========================
# CONFIGURACIÓN
# ==========================
IMMICH_URL = "https://tu-servidor-immich.com"        # URL del servidor Immich
API_KEY = "Clave_API_Aquí"                           # Clave API generada en Immich
LOCAL_FOLDER = r"C:\ruta\a\tus\archivos\multimedia"  # Carpeta local con fotos/videos a subir

# ID fijo del "dispositivo" (se mantiene estable para este PC/script)
DEVICE_ID = "windows-script-001"    # Sirve para identificar el origen de los archivos

HEADERS = {
    "x-api-key": API_KEY
}

def to_iso(dt_ts: float) -> str:
    # Immich espera formato ISO con zona horaria
    return datetime.fromtimestamp(dt_ts, tz=timezone.utc).isoformat()

def upload_file(file_path: str) -> None:
    url = f"{IMMICH_URL}/api/assets"

    # Metadatos del archivo
    stat = os.stat(file_path)
    created_at = to_iso(stat.st_ctime)   # en Windows suele ser creación real
    modified_at = to_iso(stat.st_mtime)

    # ID único por archivo (evita colisiones)
    device_asset_id = str(uuid.uuid4())

    # Detectar mime básico
    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        mime = "application/octet-stream"

    data = {
        "deviceAssetId": device_asset_id,
        "deviceId": DEVICE_ID,
        "fileCreatedAt": created_at,
        "fileModifiedAt": modified_at,
        # opcional, pero útil:
        "isFavorite": "false",
        "isArchived": "false",
    }

    with open(file_path, "rb") as f:
        files = {
            # nombre de campo esperado por Immich
            "assetData": (os.path.basename(file_path), f, mime)
        }

        r = requests.post(url, headers=HEADERS, data=data, files=files, timeout=120)

    if r.status_code in (200, 201):
        print(f"✔ Subido: {file_path}")
    else:
        print(f"✖ Error {r.status_code}: {file_path}")
        print(r.text)

def main():
    for root, _, files in os.walk(LOCAL_FOLDER):
        for name in files:
            if name.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, name)
                upload_file(path)

    print("Proceso finalizado.")

if __name__ == "__main__":
    main()
