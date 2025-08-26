# routers/auth.py
from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from pydantic import BaseModel
import httpx 
import os
from dotenv import load_dotenv

load_dotenv()

# Instancia del router
router = APIRouter()

# Configura tu client_id de Google
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Endpoint de Google que contiene las claves públicas para la validación
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Almacenar las claves públicas en caché
cached_keys = None

async def get_google_keys():
    """Obtiene las claves públicas de Google y las almacena en caché."""
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

class TokenData(BaseModel):
    id_token: str

@router.post("/login/google", tags=["auth"])
async def google_login(token_data: TokenData):
    """
    Endpoint para autenticar un usuario con el ID Token de Google.
    """
    if not CLIENT_ID:
        raise HTTPException(status_code=500, detail="Variable de entorno GOOGLE_CLIENT_ID no configurada.")
        
    id_token = token_data.id_token
    
    try:
        keys = await get_google_keys()
        
        payload = jwt.decode(
            token=id_token,
            key=keys,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            issuer="https://accounts.google.com"
        )
        
        sub = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name")
        
        if not sub:
            raise HTTPException(status_code=400, detail="ID Token inválido: 'sub' no encontrado.")

        # Puedes usar el `sub` para buscar al usuario en tu base de datos
        # y generar una sesión interna para tu aplicación (ej. un token JWT propio).
        
        return {
            "message": "Autenticación exitosa",
            "user_id": sub,
            "email": email,
            "full_name": name,
            "jwt_payload": payload 
        }
        
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token de autenticación inválido: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")