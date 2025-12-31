#!/usr/bin/env python3
"""
Script de verificación de la instalación
Comprueba que todo está configurado correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"\n✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("  ⚠ Se recomienda Python 3.9 o superior")
        return False
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    required = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'pydantic',
        'pydantic_settings',
        'jose',
        'passlib'
    ]
    
    print("\n📦 Verificando dependencias:")
    all_ok = True
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} (falta instalar)")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Verificar archivo .env"""
    env_file = Path('.env')
    print("\n📄 Verificando configuración:")
    
    if env_file.exists():
        print("  ✓ .env existe")
        
        from app.core.config import settings
        
        checks = [
            ('DB_HOST', settings.DB_HOST),
            ('DB_PORT', settings.DB_PORT),
            ('DB_NAME', settings.DB_NAME),
            ('DB_USER', settings.DB_USER),
            ('SECRET_KEY', '***' if len(settings.SECRET_KEY) > 0 else 'VACIO'),
        ]
        
        for key, value in checks:
            status = '✓' if value else '❌'
            display = value if key == 'SECRET_KEY' or len(str(value)) < 30 else f"{str(value)[:30]}..."
            print(f"    {status} {key}: {display}")
        
        return True
    else:
        print("  ❌ .env no existe (ejecuta: copy .env.example .env)")
        return False

def check_database():
    """Verificar conexión a base de datos"""
    print("\n🗄️  Verificando base de datos:")
    
    try:
        from app.db.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("  ✓ Conexión a PostgreSQL OK")
            return True
            
    except Exception as e:
        print(f"  ❌ No se pudo conectar: {str(e)[:80]}")
        print("     Verifica que PostgreSQL esté corriendo e instala la BD con:")
        print("     python create_initial_user.py")
        return False

def check_models():
    """Verificar que los modelos se cargan correctamente"""
    print("\n📊 Verificando modelos:")
    
    try:
        from app.models.user import User
        from app.models.task import Task
        print("  ✓ User model")
        print("  ✓ Task model")
        return True
    except Exception as e:
        print(f"  ❌ Error al cargar modelos: {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE INSTALACIÓN - Technical Test API")
    print("=" * 70)
    
    checks = [
        ("Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Configuración", check_env_file),
        ("Modelos", check_models),
        ("Base de datos", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error verificando {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN:")
    print("=" * 70)
    
    for name, result in results:
        status = "✓ OK" if result else "❌ FALLA"
        print(f"  {status:8} - {name}")
    
    all_ok = all(result for _, result in results)
    
    print("=" * 70)
    
    if all_ok:
        print("\n🎉 ¡Todo está configurado correctamente!")
        print("\nPuedes iniciar la aplicación con:")
        print("  uvicorn app.main:app --reload")
        print("\nO leer la documentación en:")
        print("  http://127.0.0.1:8000/docs")
    else:
        print("\n⚠️  Hay algunos problemas. Revisa los mensajes arriba.")
        print("\nSi necesitas ayuda, lee README.md o QUICKSTART.md")
    
    print()
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
