import httpx
import random
from faker import Faker
import time
import sys
from uuid import UUID

API_URL = "http://localhost:8000/api/v1"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "SecurePassword123!"

fake = Faker()
client = httpx.Client(timeout=30.0)

def login():
    print("Logging in...")
    # Add retry logic because Chaos middleware might trigger a 500 error!
    for attempt in range(5):
        try:
            response = client.post(f"{API_URL}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            if response.status_code == 200:
                token = response.json()["data"]["access_token"]
                client.headers.update({"Authorization": f"Bearer {token}"})
                print("Login successful.")
                return
        except Exception:
            pass
        time.sleep(1)
    print("Failed to login. Exiting.")
    sys.exit(1)

def robust_post(endpoint: str, data: dict):
    # Handles Chaos Middleware errors & rate limiting
    for attempt in range(5):
        try:
            res = client.post(f"{API_URL}{endpoint}", json=data)
            if res.status_code in [200, 201]:
                return res.json()["data"]
            elif res.status_code == 429:
                print("Rate limited, sleeping...")
                time.sleep(2)
        except Exception:
            pass
        time.sleep(0.5)
    print(f"Failed to POST to {endpoint} after retries.")
    return None

def generate_catalog():
    print("Generating Categories and Products...")
    category_ids = []
    for _ in range(5):
        cat = robust_post("/catalog/categories", {
            "name": fake.word().capitalize() + " " + fake.word(),
            "description": fake.catch_phrase()
        })
        if cat: category_ids.append(cat["id"])

    product_ids = []
    for _ in range(50):
        if not category_ids: break
        prod = robust_post("/catalog/products", {
            "category_id": random.choice(category_ids),
            "name": fake.word().capitalize() + " " + fake.word(),
            "sku": fake.ean13(),
            "description": fake.text(),
            "price": round(random.uniform(10, 1000), 2),
            "cost_price": round(random.uniform(5, 500), 2),
            "brand": fake.company(),
            "weight": round(random.uniform(0.1, 50.0), 2)
        })
        if prod: product_ids.append(prod["id"])
    return product_ids

def generate_people():
    print("Generating Customers...")
    customer_ids = []
    for _ in range(50):
        cust = robust_post("/people/customers", {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number()[:20],
            "customer_type": random.choice(["Retail", "Wholesale", "Corporate"])
        })
        if cust: customer_ids.append(cust["id"])
    return customer_ids

def generate_transactions(customer_ids, product_ids):
    print("Generating Orders...")
    for _ in range(100):
        if not customer_ids or not product_ids: break
        
        # 1. Create Order
        order = robust_post("/transactions/orders", {
            "customer_id": random.choice(customer_ids),
            "order_date": fake.date_time_this_year().isoformat(),
            "status": random.choice(["Pending", "Shipped", "Delivered", "Cancelled"]),
            "total_amount": round(random.uniform(50, 5000), 2)
        })
        
        if not order: continue
        
        # 2. Create Payment
        robust_post("/transactions/payments", {
            "order_id": order["id"],
            "payment_date": fake.date_time_this_year().isoformat(),
            "amount": order["total_amount"],
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            "status": "Completed"
        })

def main():
    login()
    product_ids = generate_catalog()
    customer_ids = generate_people()
    generate_transactions(customer_ids, product_ids)
    print("Data generation complete!")

if __name__ == "__main__":
    main()
