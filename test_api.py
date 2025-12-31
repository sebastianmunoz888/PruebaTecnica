#!/usr/bin/env python3
"""
Script de pruebas de la API
"""

import sys
from pathlib import Path
import requests
import json
from time import sleep

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Base URL de la API
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Prueba el endpoint de salud"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("\n✅ PRUEBA 1: Health Check")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            return True
    except Exception as e:
        print(f"\n❌ PRUEBA 1 FALLÓ: {e}")
        return False


def test_login():
    """Prueba el endpoint de login"""
    try:
        payload = {
            "email": "admin@example.com",
            "password": "admin123"
        }
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print("\n✅ PRUEBA 2: Login")
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Token type: {data.get('token_type')}")
            print(f"   Token: {data.get('access_token', '')[:50]}...")
            return data.get('access_token')
        else:
            print(f"\n❌ PRUEBA 2 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"\n❌ PRUEBA 2 FALLÓ: {e}")
        return None


def test_create_task(token):
    """Prueba crear una tarea"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "title": "Tarea de Prueba",
            "description": "Esta es una tarea de prueba para verificar que todo funciona",
            "status": "pending"
        }
        response = requests.post(
            f"{BASE_URL}/tasks/",
            json=payload,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 201:
            print("\n✅ PRUEBA 3: Crear Tarea")
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Task ID: {data.get('id')}")
            print(f"   Title: {data.get('title')}")
            print(f"   Status: {data.get('status')}")
            return data.get('id')
        else:
            print(f"\n❌ PRUEBA 3 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"\n❌ PRUEBA 3 FALLÓ: {e}")
        return None


def test_list_tasks(token):
    """Prueba listar tareas"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/tasks/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("\n✅ PRUEBA 4: Listar Tareas")
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Total tasks: {data.get('total', 0)}")
            print(f"   Page: {data.get('page', 1)}")
            if data.get('tasks'):
                print(f"   Primera tarea: {data['tasks'][0].get('title')}")
            return data
        else:
            print(f"\n❌ PRUEBA 4 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"\n❌ PRUEBA 4 FALLÓ: {e}")
        return None


def test_get_task(token, task_id):
    """Prueba obtener una tarea específica"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("\n✅ PRUEBA 5: Obtener Tarea por ID")
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   ID: {data.get('id')}")
            print(f"   Title: {data.get('title')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"\n❌ PRUEBA 5 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ PRUEBA 5 FALLÓ: {e}")
        return False


def test_update_task(token, task_id):
    """Prueba actualizar una tarea"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "title": "Tarea Actualizada",
            "status": "in_progress"
        }
        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}",
            json=payload,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("\n✅ PRUEBA 6: Actualizar Tarea")
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Nuevo título: {data.get('title')}")
            print(f"   Nuevo estado: {data.get('status')}")
            return True
        else:
            print(f"\n❌ PRUEBA 6 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ PRUEBA 6 FALLÓ: {e}")
        return False


def test_delete_task(token, task_id):
    """Prueba eliminar una tarea"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code in [200, 204]:
            print("\n✅ PRUEBA 7: Eliminar Tarea")
            print(f"   Status: {response.status_code}")
            print(f"   Message: Tarea eliminada exitosamente")
            return True
        else:
            print(f"\n❌ PRUEBA 7 FALLÓ: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ PRUEBA 7 FALLÓ: {e}")
        return False


def main():
    print("API tests")
    sleep(2)
    
    # Prueba 1: Health Check
    if not test_health():
        print("Server unavailable at http://127.0.0.1:8000")
        return False
    
    # Prueba 2: Login
    token = test_login()
    if not token:
        print("\n❌ No se pudo hacer login")
        return False
    
    # Prueba 3: Crear tarea
    task_id = test_create_task(token)
    
    # Prueba 4: Listar tareas
    test_list_tasks(token)
    
    # Prueba 5: Obtener tarea
    if task_id:
        test_get_task(token, task_id)
        
        # Prueba 6: Actualizar tarea
        test_update_task(token, task_id)
        
        # Prueba 7: Eliminar tarea
        test_delete_task(token, task_id)
    
    print("Tests completed")
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
