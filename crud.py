from sqlmodel import SQLModel, Session, create_engine, select
from datetime import datetime
from models import AtenasUser

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

def get_users(Session):
    from models import AtenasUser  # Import local para evitar ciclos
    users = Session.query(AtenasUser).all()
    return users

# El tipo de retorno "-> AtenasUser | None" es una buena práctica
def get_user_by_email(session: Session, email: str) -> AtenasUser | None:
    """
    Busca y retorna un usuario por su dirección de email usando la sintaxis de SQLModel.
    """
    # 1. Construye la consulta con select() y where()
    statement = select(AtenasUser).where(AtenasUser.email == email)
    
    # 2. Ejecuta la consulta en la sesión y obtén el primer resultado
    user = session.exec(statement).first()
    
    return user