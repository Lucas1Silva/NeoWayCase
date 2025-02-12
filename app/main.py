# app/main.py
import time
from fastapi import FastAPI, Request
from app.api.routes import router as client_router
from app.core.config import settings
import aioredis

app = FastAPI(title=settings.APP_NAME)

# Inclui as rotas de clientes
app.include_router(client_router)

# Variável global para medir o up-time
start_time = time.time()

# Eventos de startup e shutdown para configurar o Redis
@app.on_event("startup")
async def startup_event():
    redis_url = settings.REDIS_URL
    app.state.redis = await aioredis.from_url(redis_url)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()

# Middleware para contar as requisições (armazena a contagem no Redis)
@app.middleware("http")
async def add_request_count(request: Request, call_next):
    redis = app.state.redis
    await redis.incr("request_count")
    response = await call_next(request)
    return response

# Endpoint de status: informa o up-time e a quantidade de requisições
@app.get("/status")
async def status():
    current_time = time.time()
    uptime = current_time - start_time
    redis = app.state.redis
    request_count = await redis.get("request_count")
    if request_count is None:
        request_count = 0
    else:
        request_count = int(request_count)
    return {
        "uptime": uptime,
        "request_count": request_count
    }

# Cria as tabelas no banco (caso não existam)
from app.core.database import engine
from app.models.init import Base
Base.metadata.create_all(bind=engine)
