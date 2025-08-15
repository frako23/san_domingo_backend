from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables

# Importa tus routers de la API
from routers import coffee


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    - Se ejecuta al inicio para crear las tablas.
    - El 'yield' mantiene la aplicación en funcionamiento.
    - El código posterior se ejecuta al apagar la app.
    """
    create_db_and_tables()
    yield
    print("Application shutdown, closing database connection.")

app = FastAPI(lifespan=lifespan)

# Incluye los routers de tu aplicación
# El router de autenticación debe estar separado para una mejor organización
app.include_router(coffee.router)
