from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_reports"

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
    # Aquí puedes agregar la lógica para analizar las transacciones y devolver un resultado
    return {"user_id": user_id, "analysis": "Resultados del análisis financiero"}

@app.post("/transactions")
def create_transaction(transaction: schemas.Transaction):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO transactions (user_id, amount, transaction_type, category) VALUES (%s, %s, %s, %s)",
                   (transaction.user_id, transaction.amount, transaction.transaction_type, transaction.category))
    db.commit()
    transaction_id = cursor.lastrowid
    db.close()
    return {"transaction_id": transaction_id, "message": "Transacción creada correctamente"}

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, transaction: schemas.Transaction):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE transactions SET user_id = %s, amount = %s, transaction_type = %s, category = %s WHERE id = %s",
                   (transaction.user_id, transaction.amount, transaction.transaction_type, transaction.category, transaction_id))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return {"message": "Transacción actualizada correctamente"}

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return {"message": "Transacción eliminada correctamente"}

