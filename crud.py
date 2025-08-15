from sqlmodel import SQLModel, Session, create_engine
from datetime import datetime

def create_coffee_order(Session, user_id: int, coffee_id: int, quantity: int, date:datetime):
    from models import CoffeeOrder  # Import here to avoid circular imports
    coffee_order = CoffeeOrder(user_id=user_id, coffee_id=coffee_id, quantity=quantity, date=date)
    Session.add(coffee_order)
    Session.commit()
    Session.refresh(coffee_order)
    return coffee_order

def create_user(Session, name: str, lastname: str, email: str, cafes_restantes: int = 4):
    from models import AtenasUser  # Import local para evitar ciclos
    user = AtenasUser(
        name=name,
        lastname=lastname,
        email=email,
        cafes_restantes=cafes_restantes
    )
    Session.add(user)
    Session.commit()
    Session.refresh(user)
    return user