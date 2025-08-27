# auth/dependencies.py

import os
import httpx
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session

# Importa tus funciones y modelos (ajusta las rutas de importación según tu estructura)
from crud import get_user_by_email
from models import AtenasUser as User
from database import get_session

# Carga las variables de entorno
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# La caché de claves
cached_keys = None

# Esta es la herramienta de FastAPI para extraer el token del encabezado "Authorization"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_google_keys():
    """Obtiene y cachea las claves públicas de Google. (Tu función, sin cambios)"""
    global cached_keys
    if cached_keys is None:
        async with httpx.AsyncClient() as client:
            discovery_response = await client.get(GOOGLE_DISCOVERY_URL)
            discovery_response.raise_for_status()
            jwks_uri = discovery_response.json()["jwks_uri"]
            keys_response = await client.get(jwks_uri)
            keys_response.raise_for_status()
            cached_keys = keys_response.json()["keys"]
    return cached_keys

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    session: Annotated[Session, Depends(get_session)]
) -> User:
    """
    Dependencia que valida el token de Google, extrae el email y retorna 
    el usuario correspondiente de la base de datos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID no configurado.")

    try:
        keys = await get_google_keys()
        
        payload = jwt.decode(
            token=token,
            key=keys,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer="https://accounts.google.com"
        )
        
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Busca al usuario en tu base de datos usando el email del token
    user = get_user_by_email(session=session, email=email)
    
    if user is None:
        # Si el token es válido pero el usuario no está en tu BD, deniega el acceso.
        # Alternativamente, aquí podrías crear el usuario si quieres que se registre
        # automáticamente en el primer acceso.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no registrado en la aplicación")
        
    return user