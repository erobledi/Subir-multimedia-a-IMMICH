# Subir multimedia a Immich
🟡 En desarrollo

Script en Python para subir archivos multimedia (imágenes y vídeos) a un servidor **Immich** desde un entorno local (Windows).

El objetivo del proyecto es facilitar la carga masiva de archivos ubicados en una ruta local del sistema de forma automatizada, usando la API oficial de Immich.

---

## Características

- Uso de **API de Immich**
- Ejecución local en **Windows**
- Soporte para rutas locales (ej. `C:\imagenes`)
- Gestión de la clave API mediante archivo `.env`
- Proyecto simple, sin dependencias innecesarias

---

## Requisitos

- Python 3.13.7 o superior
- Acceso a un servidor Immich operativo (probado en v2.3.1)
- Clave API válida de Immich
- Conexión de red al servidor Immich

---

## Estructura del proyecto

/
├── main.py # Script principal
├── README.md # Documentación del proyecto
├── .gitignore # Archivos excluidos del repositorio
└── .env # Clave API (NO se sube a GitHub)



---

## Configuración

### 1. Clave API

La primera vez que se ejecuta el script, se creará automáticamente un archivo `.env` con el siguiente contenido:

```env
URL_IMMICH = "http://url_immich:2283"
API_KEY=TU_API_KEY_DE_IMMICH
DIRECTORIO = "ruta donde están los archivos multimedia"

