# main.py
from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
# Importa tus routers de la API
from routers import routes
from routers import auth # <-- Importa el nuevo router de autenticación


# List of allowed origins for your frontend
origins = [
    "http://localhost",
    "http://localhost:5173",  # Your Vue.js frontend's origin
]

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

# Add the CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Your list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

# Incluye los routers de tu aplicación
app.include_router(routes.router)
app.include_router(auth.router, prefix="/api/v1") # <-- Incluye el router de autenticación