from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from router import auth
from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field
from router.auth import get_current_user
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(auth.router)

class TransactionCreate(BaseModel):
    title: str
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    type: Literal['income', 'expense'] = Field(..., description="Type of the transaction")
    category: str = Field(...,description="Category of the transaction")
    date: str


class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0, description="Amount must be greater than zero")
    type: Optional[Literal['income', 'expense']] = Field(None, description="Type of the transaction")
    category: Optional[str] = Field(None, description="Category of the transaction")
    date: Optional[str] = None


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
def hello(db: db_dependency):
    return {"message": "Welcome to the FastAPI Expense Tracker!"}

@app.post("/transactions")
def create_transaction(transaction: TransactionCreate, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_transaction = models.Transactions(**transaction.model_dump(), owner_id=user.get("user_id"))
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return JSONResponse(status_code=201, content={"message": "Transaction created successfully", "transaction": {"id": new_transaction.id, "title": new_transaction.title, "amount": new_transaction.amount, "type": new_transaction.type, "category": new_transaction.category, "date": new_transaction.date, "owner_id": new_transaction.owner_id}})

@app.get("/transactions")
def get_transactions(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(models.Transactions).filter(models.Transactions.owner_id == user.get("user_id")).all()

@app.get("/transactions/filter")
def filter_transactions(type: str, category: str, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(models.Transactions).filter(models.Transactions.owner_id == user.get("user_id"), models.Transactions.type == type, models.Transactions.category == category).all()

@app.get("/transactions/{transaction_id}")
def get_specific_transaction(transaction_id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id, models.Transactions.owner_id == user.get("user_id")).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    existing_transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id, models.Transactions.owner_id == user.get("user_id")).first()
    if existing_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in transaction.model_dump(exclude_unset=True).items():
        setattr(existing_transaction, key, value)
    db.commit()
    db.refresh(existing_transaction)
    return JSONResponse(status_code=200, content={"message": "Transaction updated successfully", "transaction": {"id": existing_transaction.id, "title": existing_transaction.title, "amount": existing_transaction.amount, "type": existing_transaction.type, "category": existing_transaction.category, "date": existing_transaction.date, "owner_id": existing_transaction.owner_id}})


@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id, models.Transactions.owner_id == user.get("user_id")).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Transaction deleted successfully"})