from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from sqlalchemy import text # <-- IMPORTACIÓN NECESARIA

class CoffeeFlavor(str, Enum):
    vainilla = "vainilla"
    chocolate = "chocolate"
    galleta = "galleta"
    avellana = "avellana"

# Se define primero para poder referenciarlo sin comillas
class CoffeeType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: CoffeeFlavor = Field(index=True)

    # Relación: Un tipo de café puede estar en muchas órdenes
    orders: List["CoffeeOrder"] = Relationship(back_populates="coffee_type")


class AtenasUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    lastname: str
    email: str = Field(unique=True, index=True)
    cafes_restantes: int = 4
    fecha_de_creacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    fecha_de_modificacion: Optional[datetime] = Field(
        default=None, 
        nullable=True,
        sa_column_kwargs={"onupdate": text("CURRENT_TIMESTAMP")}
    )

    # Relación: Un usuario puede tener muchas órdenes de café
    orders: List["CoffeeOrder"] = Relationship(back_populates="user")


class CoffeeOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int
    date: datetime = Field(default_factory= lambda: datetime.now(timezone.utc), nullable=False) # <-- SUGERENCIA

    # Llaves foráneas
    user_id: int = Field(foreign_key="atenasuser.id")
    coffee_id: int = Field(foreign_key="coffeetype.id")

    # Relaciones de "vuelta"
    user: AtenasUser = Relationship(back_populates="orders")
    coffee_type: CoffeeType = Relationship(back_populates="orders")

class UserRead(SQLModel):
    id: int
    name: str
    email: str
    cafes_restantes: int
    fecha_de_creacion: datetime
    fecha_de_modificacion: Optional[datetime]

    class Config:
        from_attributes = True