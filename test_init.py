"""Script para crear las tablas de la base de datos"""
import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    print("=" * 70)
    print("CREANDO BASE DE DATOS Y TABLAS")
    print("=" * 70)
    
    try:
        logger.info("Importando módulos...")
        from app.db.init_db import init_database
        
        logger.info("Ejecutando inicialización...")
        init_database()
        
        print("=" * 70)
        print("✓ ÉXITO - Base de datos y tablas creadas correctamente")
        print("=" * 70)
        
    except Exception as e:
        print("=" * 70)
        print(f"❌ ERROR: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()