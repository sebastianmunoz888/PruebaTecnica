from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import auth, tasks
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al inicio
    logger.info("=" * 70)
    logger.info("INICIANDO APLICACIÓN - Technical Test API")
    logger.info("=" * 70)
    
    try:
        from app.db.init_db import init_database
        init_database()
        logger.info("=" * 70)
        logger.info("✓ Base de datos inicializada correctamente")
        logger.info("=" * 70)
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"❌ ERROR al inicializar la base de datos: {e}")
        logger.error("=" * 70)
        import traceback
        traceback.print_exc()
    
    yield
    
    # Código que se ejecuta al cerrar (si necesitas cleanup)
    logger.info("Cerrando aplicación...")


app = FastAPI(
    title="Technical Test API",
    description="API REST con FastAPI y PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
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