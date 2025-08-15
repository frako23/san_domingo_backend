from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel
from models import CoffeeOrder
from datetime import datetime
from crud import create_user
from typing import Annotated
from database import get_session
from pydantic import BaseModel

sessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.get("/get_coffee")
def get_coffee():
    return {"coffee": "Here is your coffee!"}

# Un modelo Pydantic para el cuerpo del pedido de la API
class CoffeeOrderInput(SQLModel):
    user_id: int
    coffee_id: int
    quantity: int
    date: datetime

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: str
    cafes_restantes: int = 4

@router.post("/order_coffee/", response_model=CoffeeOrder)
def order_coffee(order_data: CoffeeOrderInput, session: sessionDep):
    # 1. Crea una instancia del modelo de base de datos a partir de los datos recibidos
    coffee_order = CoffeeOrder.model_validate(order_data)
    
    # 2. Agrega el objeto a la sesión
    session.add(coffee_order)
    
    # 3. Confirma la transacción en la base de datos
    session.commit()
    
    # 4. Actualiza el objeto con el ID generado por la base de datos
    session.refresh(coffee_order)
    
    return coffee_order


@router.post("/create_user/")
def create_user_route(user_data: UserCreate, session: sessionDep):
    user = create_user(
        session,
        name=user_data.name,
        lastname=user_data.lastname,
        email=user_data.email,
        cafes_restantes=user_data.cafes_restantes
    )
    return user