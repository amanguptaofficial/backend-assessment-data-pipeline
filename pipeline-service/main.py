from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
from models.customer import Customer
from services.ingestion import fetch_all_customers, upsert_customers
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/ingest")
def ingest_data(db: Session = Depends(get_db)):
    try:
        customers_data = fetch_all_customers()
        records_processed = upsert_customers(db, customers_data)
        
        return {
            "status": "success",
            "records_processed": records_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    
    customers = db.query(Customer).offset(skip).limit(limit).all()
    total = db.query(Customer).count()
    
    customers_list = []
    for customer in customers:
        customers_list.append({
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "date_of_birth": str(customer.date_of_birth) if customer.date_of_birth else None,
            "account_balance": float(customer.account_balance) if customer.account_balance else None,
            "created_at": customer.created_at.isoformat() if customer.created_at else None
        })
    
    return {
        "data": customers_list,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "date_of_birth": str(customer.date_of_birth) if customer.date_of_birth else None,
        "account_balance": float(customer.account_balance) if customer.account_balance else None,
        "created_at": customer.created_at.isoformat() if customer.created_at else None
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
