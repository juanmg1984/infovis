# Data360 CORS Proxy

Un proxy minimalista para usar **Data360 Embed** cuando el browser bloquea la API del Banco Mundial por CORS.

## Deploy en Render.com (gratis)

1. Subí estos archivos a un repositorio de GitHub
2. Creá una cuenta en [render.com](https://render.com)
3. "New Web Service" → conectá el repo → usa el `render.yaml` incluido
4. Copiá la URL del servicio (ej. `https://data360-proxy.onrender.com`)
5. En el Configurador de Data360 Embed → Configuración avanzada → pegá esa URL

## Uso local

```bash
pip install -r requirements.txt
uvicorn proxy:app --reload
# Disponible en http://localhost:8000
```
