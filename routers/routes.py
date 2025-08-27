from fastapi import APIRouter, Depends
from sqlmodel import Session, SQLModel
from models import CoffeeOrder, UserRead
from datetime import datetime
from crud import create_user, get_users
from typing import Annotated
from database import get_session
from pydantic import BaseModel
from auth.dependencies import get_current_user
from models import AtenasUser as User, CoffeeOrder

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

@router.get("/get_users/")
def get_users_route( session: sessionDep):
    user = get_users(
        session,
    )
    return user

@router.get("/get_current_user", response_model=UserRead)
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Obtiene la información del usuario actualmente autenticado usando su JWT.
    
    Cómo funciona:
    1. FastAPI ve que este endpoint `Depends` on `get_current_user`.
    2. Ejecuta esa dependencia, la cual valida el token y busca al usuario en la BD.
    3. Si todo es correcto, inyecta el objeto `User` en el parámetro `current_user`.
    4. Si algo falla (token inválido, usuario no existe), la dependencia lanzará un error HTTP.
    """
    return current_user
