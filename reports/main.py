from fastapi import FastAPI, HTTPException
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

@app.get("/expenses")
def get_expense_report(user_id: int, category: str = None):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM transactions WHERE user_id = %s AND transaction_type = 'expense'"
    params = [user_id]
    if category:
        query += " AND category = %s"
        params.append(category)
    cursor.execute(query, tuple(params))
    transactions = cursor.fetchall()
    db.close()
    return {"user_id": user_id, "expenses": transactions}

@app.get("/income")
def get_income_report(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s AND transaction_type = 'income'", (user_id,))
    transactions = cursor.fetchall()
    db.close()
    return {"user_id": user_id, "income": transactions}

@app.get("/financial-analysis")
def get_financial_analysis(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()
    db.close()
    # Here you can add logic to analyze the transactions
    return {"user_id": user_id, "analysis": "Financial analysis results"}
