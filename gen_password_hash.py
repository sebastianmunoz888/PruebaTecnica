#!/usr/bin/env python3
"""
Script para generar hash de contraseña usando bcrypt directamente
"""

import bcrypt

password = "admin123"
# Generar salt y hash
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
