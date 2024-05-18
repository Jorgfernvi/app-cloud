from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_loans"

def get_db_connection():
    return mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )

@app.post("/loans")
def apply_for_loan(loan: schemas.LoanApplication):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO loans (user_id, amount, term, status) VALUES (%s, %s, %s, 'pending')", 
                   (loan.user_id, loan.amount, loan.term))
    db.commit()
    loan_id = cursor.lastrowid
    db.close()
    return {"loan_id": loan_id, "message": "Loan application submitted successfully"}

@app.get("/loans/{user_id}")
def get_user_loans(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM loans WHERE user_id = %s", (user_id,))
    loans = cursor.fetchall()
    db.close()
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found for this user")
    return loans

@app.put("/loans/{loan_id}/status")
def update_loan_status(loan_id: int, status: schemas.LoanStatusUpdate):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE loans SET status = %s WHERE id = %s", (status.status, loan_id))
    db.commit()
    db.close()
    return {"message": "Loan status updated successfully"}

@app.get("/loans/{loan_id}/payments")
def get_loan_payments(loan_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM loan_payments WHERE loan_id = %s", (loan_id,))
    payments = cursor.fetchall()
    db.close()
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this loan")
    return payments

@app.get("/loans/pending")
def get_pending_loans():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM loans WHERE status = 'pending'")
    pending_loans = cursor.fetchall()
    db.close()
    if not pending_loans:
        raise HTTPException(status_code=404, detail="No pending loans found")
    return pending_loans
