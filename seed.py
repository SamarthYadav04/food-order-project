from database import SessionLocal, engine
from models import Base, User, Food, Order
from main import hash_password

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data
db.query(Order).delete()
db.query(User).delete()
db.query(Food).delete()
db.commit()

# Sample Users
users_data = [
    {"name": "John Doe", "email": "john@example.com", "password": "password123"},
    {"name": "Jane Smith", "email": "jane@example.com", "password": "password123"},
    {"name": "Admin User", "email": "admin@example.com", "password": "admin123"},
]

for user in users_data:
    hashed_password = hash_password(user["password"])
    new_user = User(
        name=user["name"],
        email=user["email"],
        password=hashed_password
    )
    db.add(new_user)
    print(f"✓ Added user: {user['email']}")

# Sample Foods
foods_data = [
    {"food_name": "Margherita Pizza", "price": 12.99, "description": "Classic pizza with tomato, mozzarella, and basil", "image_url": "/img/food/pizza.jpg"},
    {"food_name": "Caesar Salad", "price": 8.99, "description": "Fresh romaine lettuce with parmesan cheese and croutons", "image_url": "/img/food/salad.jpg"},
    {"food_name": "Burger", "price": 10.99, "description": "Juicy beef burger with lettuce, tomato, and pickles", "image_url": "/img/food/burger.jpg"},
    {"food_name": "Pasta Carbonara", "price": 13.99, "description": "Creamy pasta with bacon, eggs, and pecorino cheese", "image_url": "/img/food/pasta.jpg"},
    {"food_name": "Grilled Chicken Breast", "price": 14.99, "description": "Tender grilled chicken with herbs and lemon", "image_url": "/img/food/chicken.jpg"},
    {"food_name": "Fish and Chips", "price": 11.99, "description": "Crispy battered fish with golden fries", "image_url": "/img/food/fish.jpg"},
    {"food_name": "Pad Thai", "price": 9.99, "description": "Thai stir-fried noodles with peanuts and shrimp", "image_url": "/img/food/padthai.jpg"},
    {"food_name": "Sushi Roll Combo", "price": 15.99, "description": "Assorted fresh sushi rolls with soy sauce and wasabi", "image_url": "/img/food/sushi.jpg"},
    {"food_name": "Tacos (3 pieces)", "price": 9.99, "description": "Delicious Mexican tacos with your choice of meat", "image_url": "/img/food/tacos.jpg"},
    {"food_name": "Cheesecake", "price": 6.99, "description": "Creamy New York style cheesecake with berry topping", "image_url": "/img/food/cheesecake.jpg"},
]

for food in foods_data:
    new_food = Food(
        food_name=food["food_name"],
        price=food["price"],
        description=food["description"],
        image_url=food["image_url"]
    )
    db.add(new_food)
    print(f"✓ Added food: {food['food_name']} - ${food['price']}")

# Sample Orders
orders_data = [
    {"user_email": "john@example.com", "food_name": "Margherita Pizza", "quantity": 1, "total_price": 12.99},
    {"user_email": "jane@example.com", "food_name": "Caesar Salad", "quantity": 2, "total_price": 17.98},
    {"user_email": "john@example.com", "food_name": "Burger", "quantity": 1, "total_price": 10.99},
]

for order in orders_data:
    new_order = Order(
        user_email=order["user_email"],
        food_name=order["food_name"],
        quantity=order["quantity"],
        total_price=order["total_price"]
    )
    db.add(new_order)
    print(f"✓ Added order: {order['food_name']} for {order['user_email']}")

db.commit()
db.close()

print("\n✅ Database seeding completed successfully!")
