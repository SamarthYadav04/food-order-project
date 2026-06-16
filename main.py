import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
from models import Base, Food, User, Order
from schemas import FoodCreate, UserCreate, UserLogin, OrderCreate

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer


# ==========================
# DATABASE
# ==========================

Base.metadata.create_all(bind=engine)

# ==========================
# JWT SETTINGS
# ==========================

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ==========================
# PASSWORD FUNCTIONS
# ==========================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# ==========================
# JWT TOKEN FUNCTIONS
# ==========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            return {"message": "Invalid Token"}

        return email

    except JWTError:
        return {"message": "Invalid Token"}
        

        



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/me")
def get_me(
    current_user: str = Depends(get_current_user)
):
    return {
        "logged_in_user": current_user
    }

# ==========================
# DATABASE DEPENDENCY
# ==========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ==========================
# HOME
# ==========================

@app.get("/")
def home():

    return {
        "message": "Food Order Backend Connected"
    }

# ==========================
# REGISTER
# ==========================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already registered"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }

# ==========================
# LOGIN
# ==========================

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        return {
            "message": "Invalid Email"
        }

    if not verify_password(
        user.password,
        db_user.password
    ):
        return {
            "message": "Invalid Password"
        }

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@app.post("/orders")
def place_order(
    order: OrderCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    new_order = Order(
        user_email=current_user["email"],
        food_name=order.food_name,
        quantity=order.quantity,
        total_price=order.total_price
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": new_order.id
    }

@app.get("/orders")
def get_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    orders = db.query(Order).filter(
        Order.user_email == current_user["email"]
    ).all()

    return orders
# ==========================
# CREATE FOOD
# ==========================

@app.post("/foods")
def create_food(
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    new_food = Food(
        food_name=food.food_name,
        price=food.price,
        description=food.description,
        image_url=food.image_url
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return {
        "message": "Food Added Successfully",
        "food_id": new_food.id
    }

# ==========================
# GET ALL FOODS
# ==========================

@app.get("/foods")
def get_foods(
    db: Session = Depends(get_db)
):

    foods = db.query(Food).all()

    return foods

# ==========================
# GET FOOD BY ID
# ==========================

@app.get("/foods/{food_id}")
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):

    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        return {
            "message": "Food not found"
        }

    return food

# ==========================
# UPDATE FOOD
# ==========================

@app.put("/foods/{food_id}")
def update_food(
    food_id: int,
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    existing_food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not existing_food:
        return {
            "message": "Food not found"
        }

    existing_food.food_name = food.food_name
    existing_food.price = food.price
    existing_food.description = food.description
    existing_food.image_url = food.image_url

    db.commit()

    return {
        "message": "Food updated successfully"
    }

# ==========================
# DELETE FOOD
# ==========================

@app.delete("/foods/{food_id}")
def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    food = db.query(Food).filter(
        Food.id == food_id
    ).first()

    if not food:
        return {"message": "Food not found"}

    db.delete(food)
    db.commit()

    return {"message": "Food deleted successfully"}