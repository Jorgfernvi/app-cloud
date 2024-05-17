from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRouter
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_bank"

def get_db_connection():
    return mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )


router = APIRouter()

@router.post("/")
def apply_for_loan(loan: schemas.LoanApplication):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO loans (user_id, amount, term, status) VALUES (%s, %s, %s, 'pending')", 
                   (loan.user_id, loan.amount, loan.term))
    db.commit()
    loan_id = cursor.lastrowid
    db.close()
    return {"loan_id": loan_id, "message": "Loan application submitted successfully"}

@router.get("/{loan_id}/status")
def get_loan_status(loan_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT status FROM loans WHERE id = %s", (loan_id,))
    loan = cursor.fetchone()
    db.close()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"loan_id": loan_id, "status": loan['status']}

@router.post("/{loan_id}/payment")
def make_loan_payment(loan_id: int, payment: schemas.LoanPayment):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO loan_payments (loan_id, amount) VALUES (%s, %s)", (loan_id, payment.amount))
    db.commit()
    db.close()
    return {"message": "Payment made successfully"}
