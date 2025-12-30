from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.schemas.user import LoginRequest, Token
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.core.config import settings

# api de autenticacion (prefijo de la llamada)
router = APIRouter(prefix="/auth", tags=["authentication"])

# sufijo de la llamada
@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Autenticar al usuario
    user = authenticate_user(db, login_data.email, login_data.password)
    # Si la autenticacion falla, lanzar una excepcion
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Crear el token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Generar el token JWT
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # Retornar el token de acceso para probar por postman
    return {"access_token": access_token, "token_type": "bearer"}