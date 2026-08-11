from test.test_main import client
from main import app
from fastapi import status
from router.auth import get_current_user
from database import SessionLocal
from models import Transactions


def override_get_current_user():
    return {'user_id': 1, 'username': 'testuser'}


app.dependency_overrides[get_current_user] = override_get_current_user

def test_transaction():
    db = SessionLocal()
    db.query(Transactions).filter(Transactions.id == 99).delete()

    transaction = Transactions(
        id=99,
        title='Testing',
        amount=100.0,
        type='income',
        category='Test',
        date='2023-01-01',
        owner_id=1
    )
    db.add(transaction)
    db.commit()


def test_read_transaction():
    response = client.get("/transactions")
    assert response.status_code == status.HTTP_200_OK

def test_read_specific_transaction():
    response = client.get("/transactions/99")
    assert response.status_code == status.HTTP_200_OK

def test_create_transaction():
    transaction_data = {
        "title": "Test Transaction",
        "amount": 50.0,
        "type": "income",
        "category": "Test",
        "date": "2023-01-01"
    }
    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Transaction created successfully"

def test_update_transaction():
    update_data = {
        "title": "Updated"
    }
    response = client.put("/transactions/99", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Transaction updated successfully"

def test_delete_transaction():
    response = client.delete("/transactions/99")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Transaction deleted successfully"
