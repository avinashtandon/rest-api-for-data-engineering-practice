import asyncio
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.people import *
from app.models.catalog import *
from app.models.transactions import *
from app.models.location import *
from app.models.inventory import *
from app.models.user import User, RoleEnum
from app.core.config import settings
from app.core.security import get_password_hash

fake = Faker()

# Database URL pointing to docker network postgres
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/erp_db"
# If running inside docker, localhost should be replaced by 'db', but we will run this inside the 'api' container, so 'db' is correct.
# Wait, let's use the settings variable so it works automatically.
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def bulk_seed():
    print("Starting massive data generation (Target: ~60,000 rows)...")
    
    categories = []
    products = []
    customers = []
    orders = []
    payments = []
    users = []

    # 0. Generate 200 System Users
    print("Generating 200 System Users...")
    hashed_password = get_password_hash("Password123!")
    for _ in range(200):
        users.append(User(
            id=uuid.uuid4(),
            email=f"{uuid.uuid4().hex[:8]}_{fake.email()}",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            hashed_password=hashed_password,
            is_active=True,
            role=random.choice([RoleEnum.ADMIN, RoleEnum.MANAGER, RoleEnum.DATA_ENGINEER, RoleEnum.ANALYST, RoleEnum.VIEWER]),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        ))

    # 1. Generate 50 Categories
    print("Generating 50 Categories...")
    for _ in range(50):
        categories.append(Category(
            id=uuid.uuid4(),
            name=fake.word().capitalize() + " " + fake.word(),
            description=fake.catch_phrase(),
            created_at=datetime.utcnow()
        ))

    # 2. Generate 10,000 Products
    print("Generating 10,000 Products...")
    for _ in range(10000):
        products.append(Product(
            id=uuid.uuid4(),
            category_id=random.choice(categories).id,
            name=fake.word().capitalize() + " " + str(random.randint(100, 9999)),
            sku=fake.ean13(),
            description=fake.text(max_nb_chars=50),
            price=round(random.uniform(10, 1000), 2),
            weight=round(random.uniform(0.1, 50.0), 2),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        ))

    # 3. Generate 10,000 Customers
    print("Generating 10,000 Customers...")
    for _ in range(10000):
        customers.append(Customer(
            id=uuid.uuid4(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=f"{uuid.uuid4().hex[:8]}_{fake.email()}",
            phone=fake.phone_number()[:20],
            loyalty_tier=random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        ))

    # 4. Generate 20,000 Orders and 20,000 Payments
    print("Generating 20,000 Orders and 20,000 Payments...")
    for _ in range(20000):
        order_id = uuid.uuid4()
        order_total = round(random.uniform(50, 5000), 2)
        order_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
        
        orders.append(Order(
            id=order_id,
            customer_id=random.choice(customers).id,
            order_date=order_date,
            status=random.choice(["Pending", "Shipped", "Delivered", "Cancelled"]),
            total_amount=order_total,
            created_at=order_date
        ))
        
        payments.append(Payment(
            id=uuid.uuid4(),
            order_id=order_id,
            payment_date=order_date + timedelta(hours=random.randint(1, 48)),
            amount=order_total,
            payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            status="Completed",
            created_at=order_date + timedelta(hours=random.randint(1, 48))
        ))

    print(f"Total objects generated in memory: {len(categories) + len(products) + len(customers) + len(orders) + len(payments) + len(users)}")
    
    print("Bulk inserting into database... (This might take a minute)")
    async with AsyncSessionLocal() as session:
        session.add_all(users)
        session.add_all(categories)
        session.add_all(products)
        session.add_all(customers)
        # Flush to ensure foreign keys are available
        await session.flush()
        
        session.add_all(orders)
        await session.flush()
        
        session.add_all(payments)
        await session.commit()
        
    print("✅ Successfully inserted ~60,000 rows into the database!")

if __name__ == "__main__":
    asyncio.run(bulk_seed())
