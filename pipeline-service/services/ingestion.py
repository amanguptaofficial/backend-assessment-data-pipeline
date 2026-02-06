import requests
from sqlalchemy.orm import Session
from models.customer import Customer
from datetime import datetime
import os

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://mock-server:5000")

def fetch_all_customers():
    all_customers = []
    page = 1
    limit = 10
    
    while True:
        response = requests.get(f"{FLASK_API_URL}/api/customers", params={"page": page, "limit": limit})
        response.raise_for_status()
        
        data = response.json()
        customers = data.get("data", [])
        
        if not customers:
            break
        
        all_customers.extend(customers)
        
        if len(all_customers) >= data.get("total", 0):
            break
        
        page += 1
    
    return all_customers

def upsert_customers(db: Session, customers_data):
    records_processed = 0
    
    for customer_data in customers_data:
        created_at_str = customer_data.get("created_at")
        if created_at_str:
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        else:
            created_at = None
        
        date_of_birth_str = customer_data.get("date_of_birth")
        if date_of_birth_str:
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
        else:
            date_of_birth = None
        
        existing_customer = db.query(Customer).filter(
            Customer.customer_id == customer_data["customer_id"]
        ).first()
        
        if existing_customer:
            existing_customer.first_name = customer_data["first_name"]
            existing_customer.last_name = customer_data["last_name"]
            existing_customer.email = customer_data["email"]
            existing_customer.phone = customer_data.get("phone")
            existing_customer.address = customer_data.get("address")
            existing_customer.date_of_birth = date_of_birth
            existing_customer.account_balance = customer_data.get("account_balance")
            existing_customer.created_at = created_at
        else:
            new_customer = Customer(
                customer_id=customer_data["customer_id"],
                first_name=customer_data["first_name"],
                last_name=customer_data["last_name"],
                email=customer_data["email"],
                phone=customer_data.get("phone"),
                address=customer_data.get("address"),
                date_of_birth=date_of_birth,
                account_balance=customer_data.get("account_balance"),
                created_at=created_at
            )
            db.add(new_customer)
        
        records_processed += 1
    
    db.commit()
    return records_processed
