from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    food_name = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)    