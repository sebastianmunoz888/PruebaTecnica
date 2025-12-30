from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, tasks
import os

# Configurar variables de entorno
if not os.getenv("DB_HOST"):
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "technical_test"
    os.environ["DB_USER"] = "postgres"
    os.environ["DB_PASSWORD"] = "postgres"
    os.environ["SECRET_KEY"] = "super_secret_key_change_this"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    os.environ["INITIAL_USER_EMAIL"] = "admin@example.com"
    os.environ["INITIAL_USER_PASSWORD"] = "admin123"

app = FastAPI(
    title="Technical Test API",
    description="API REST para gestión de tareas con autenticación JWT",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {
        "message": "API de Technical Test",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}