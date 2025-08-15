from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
from enum import Enum

class CoffeeFlavor(str, Enum):
    vainilla = "vainilla"
    chocolate = "chocolate"
    galleta = "galleta"
    avellana = "avellana"

class AtenasUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    lastname: str
    email: str
    cafes_restantes: int = 4

class CoffeeType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: CoffeeFlavor = Field(index=True)

class CoffeeOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="atenasuser.id")
    coffee_id: int = Field(foreign_key="coffeetype.id")
    quantity: int
    date: datetime 
