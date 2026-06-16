from pydantic import BaseModel

# Food Schema
class FoodCreate(BaseModel):
    food_name: str
    price: float
    description: str
    image_url: str


# User Register Schema
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# User Login Schema
class UserLogin(BaseModel):
    email: str
    password: str

class OrderCreate(BaseModel):
    food_name: str
    quantity: int
    total_price: float