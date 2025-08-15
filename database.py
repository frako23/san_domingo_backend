import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

# 🚨 ¡IMPORTANTE! Agrega esta línea para importar tus modelos
from models import AtenasUser, CoffeeType, CoffeeOrder

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    print("Creando tablas...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas con éxito.")

def get_session():
    with Session(engine) as session:
        yield session