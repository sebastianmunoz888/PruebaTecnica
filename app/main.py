from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, tasks


app = FastAPI(
    title="Technical Test API",
    description="API REST con FastAPI y PostgreSQL",
    version="1.0.0",
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
def read_root():
    return {
        "message": "API de Prueba Técnica - FastAPI",
        "version": "1.0.0",
        "status": "online",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "healthy",
        "database": "connected"
    }