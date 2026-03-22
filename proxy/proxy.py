# proxy.py — Data360 CORS Proxy
# Deploy gratuito en Render.com: https://render.com
# 1. Fork este repo en GitHub
# 2. Conectalo a Render como "Web Service" (Python)
# 3. Start command: uvicorn proxy:app --host 0.0.0.0 --port $PORT

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Data360 CORS Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

DATA360_BASE = "https://data360api.worldbank.org/data360"
TIMEOUT = 30.0

@app.get("/")
def root():
    return {"status": "ok", "service": "Data360 CORS Proxy", "docs": "/docs"}

@app.get("/data360/data")
async def proxy_data(request: Request):
    """Proxy GET /data360/data with all query params forwarded."""
    params = dict(request.query_params)
    url = f"{DATA360_BASE}/data"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.get(url, params=params)
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "application/json"),
    )

@app.get("/health")
def health():
    return {"status": "healthy"}
