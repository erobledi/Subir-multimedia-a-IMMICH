from pathlib import Path
import config


#// Librerías para usar en immich
import os
import time
import hashlib
from datetime import datetime, timezone

import requests





# ==========================
# UTILIDADES
# ==========================
def to_iso(dt_ts: float) -> str:
    return datetime.fromtimestamp(dt_ts, tz=timezone.utc).isoformat()


def obtener_mime(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    return "application/octet-stream"


def generar_device_asset_id(device_id: str, file_path: str) -> str:
    """
    ID estable para Immich.
    Si el archivo no cambia, Immich lo reconoce como ya existente.
    """
    p = os.path.abspath(file_path)
    st = os.stat(file_path)
    base = f"{device_id}|{p}|{st.st_size}|{int(st.st_mtime)}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


# ==========================
# VERIFICACIÓN EN SERVIDOR
# ==========================
def existe_en_servidor(immich_url: str, headers: dict, device_id: str, device_asset_id: str) -> bool:
    url = f"{immich_url}/api/assets/exist"
    payload = [{"deviceAssetId": device_asset_id, "deviceId": device_id}]

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code != 200:
            return False

        data = r.json()

        # Respuesta típica: lista de assets existentes
        if isinstance(data, list):
            return any(
                isinstance(x, dict) and x.get("deviceAssetId") == device_asset_id
                for x in data
            )

        # Variante: dict con lista interna
        if isinstance(data, dict):
            items = data.get("existing") or data.get("assets") or []
            if isinstance(items, list):
                return any(
                    isinstance(x, dict) and x.get("deviceAssetId") == device_asset_id
                    for x in items
                )

        return False

    except Exception:
        # Si falla la verificación, no bloqueamos la subida
        return False


# ==========================
# SUBIDA
# ==========================
def upload_file(
    immich_url: str,
    headers: dict,
    device_id: str,
    file_path: str,
    device_asset_id: str
) -> bool:
    url = f"{immich_url}/api/assets"

    stat = os.stat(file_path)
    created_at = to_iso(stat.st_ctime)
    modified_at = to_iso(stat.st_mtime)

    mime = obtener_mime(file_path)

    data = {
        "deviceAssetId": device_asset_id,
        "deviceId": device_id,
        "fileCreatedAt": created_at,
        "fileModifiedAt": modified_at,
        "isFavorite": "false",
        "isArchived": "false",
    }

    try:
        with open(file_path, "rb") as f:
            files = {"assetData": (os.path.basename(file_path), f, mime)}
            r = requests.post(
                url,
                headers=headers,
                data=data,
                files=files,
                timeout=120
            )

    except Exception as e:
        print(f"✖ Error de red o subida: {file_path}")
        print(f"    Detalle: {e}")
        return False

    if r.status_code in (200, 201):
        print(f"✔ Subido: {file_path}")
        return True

    print(f"✖ Error {r.status_code}: {file_path}")
    print(r.text)
    return False



# ==========================
# Subir archivos a Immich
# ==========================
def fun_subirArchivosImmich():
    archivoDatos = Path("datos.json")
    cfg = config.fun_leerArchivo(archivoDatos, debugJSON=True)

    if not cfg:
        raise SystemExit("No se pudo cargar la configuración.")

    immich_url = cfg["immich_url"]
    api_key = cfg["api_key"]
    
    local_folder = cfg["ruta_local"]
    #print(f"Ruta local: {local_folder}")

    if not os.path.isdir(local_folder):
        raise SystemExit(f"La ruta local no existe o no es una carpeta: {local_folder}")

    device_id = cfg.get("device_id", "windows-script-001")

    pausa_segundos = float(cfg.get("pausa_segundos", 0.7))

    headers = {"x-api-key": api_key}

    for root, _, files in os.walk(local_folder):
        for name in files:
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            path = os.path.join(root, name)
            device_asset_id = generar_device_asset_id(device_id, path)

            # 1) Verificar en Immich
            if existe_en_servidor(immich_url, headers, device_id, device_asset_id):
                print(f"↷ Ya existe en Immich (omitido): {path}")
                continue

            # 2) Subir
            upload_file(immich_url, headers, device_id, path, device_asset_id)

            # 3) Pausa
            if pausa_segundos > 0:
                time.sleep(pausa_segundos)

    print("Proceso finalizado.")



if __name__ == "__main__":
    fun_subirArchivosImmich()
    
    print("<======================= Programa finalizado. =======================>")