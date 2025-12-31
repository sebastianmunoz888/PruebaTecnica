
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash
from app.db.database import SessionLocal, Base
import logging

logger = logging.getLogger(__name__)

def database_exists():
    try:
        engine_postgres = create_engine(
            f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres",
            isolation_level="AUTOCOMMIT"
        )
        
        with engine_postgres.connect() as conn:
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
            )
            exists = result.fetchone() is not None
        
        engine_postgres.dispose()
        return exists
    except Exception as e:
        logger.error(f"Error al verificar base de datos: {e}")
        return False

def create_database():
    try:
        if database_exists():
            logger.info(f"Base de datos '{settings.DB_NAME}' ya existe")
            return
        
        logger.info(f"Creando base de datos '{settings.DB_NAME}'...")
        
        engine_postgres = create_engine(
            f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres",
            isolation_level="AUTOCOMMIT"
        )
        
        with engine_postgres.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
            logger.info(f"Base de datos '{settings.DB_NAME}' creada")
        
        engine_postgres.dispose()
        
    except Exception as e:
        logger.error(f"Error al crear base de datos: {e}")
        raise

def create_tables():
    try:
        from app.db.database import engine
        logger.info("Creando tablas...")
        
        from app.models import user, task
        
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"Error al crear tablas: {e}")
        raise

def create_initial_user():
    db = None
    try:
        db = SessionLocal()
        
        existing_user = db.query(User).filter(
            User.email == settings.INITIAL_USER_EMAIL
        ).first()
        
        if not existing_user:
            logger.info(f"Creando usuario inicial: {settings.INITIAL_USER_EMAIL}")
            hashed_password = get_password_hash(settings.INITIAL_USER_PASSWORD)
            initial_user = User(
                email=settings.INITIAL_USER_EMAIL,
                hashed_password=hashed_password
            )
            db.add(initial_user)
            db.commit()
            logger.info(f"Usuario inicial creado: {settings.INITIAL_USER_EMAIL}")
        else:
            logger.info(f"Usuario inicial ya existe")
        
    except Exception as e:
        logger.error(f"Error al crear usuario inicial: {e}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close()

def init_database():
    try:
        logger.info("Paso 1: Verificando base de datos...")
        create_database()
        
        logger.info("Paso 2: Creando tablas...")
        create_tables()
        
        logger.info("Paso 3: Creando usuario inicial...")
        create_initial_user()
        
        logger.info("Inicialización completada")
    except Exception as e:
        logger.error(f"Error en init_database: {e}")
        import traceback
        traceback.print_exc()
        raise
