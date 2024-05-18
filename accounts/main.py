from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List

## Define los parámetros de conexión a la base de datos
host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_bank"

# Función para obtener una conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )

# Define tu modelo Pydantic
class Account(BaseModel):
    user_id: int
    name: str
    balance: float

# Crea la aplicación principal de FastAPI
app = FastAPI()

# Define la ruta para crear una cuenta
@app.post("/accounts/")
def create_account(account: Account):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO accounts (user_id, name, balance) VALUES (%s, %s, %s)", (account.user_id, account.name, account.balance))
    db.commit()
    account_id = cursor.lastrowid
    db.close()
    return {"account_id": account_id, "message": "Account created successfully"}

# Define la ruta para obtener el balance de una cuenta
@app.get("/accounts/{account_id}/balance")
def get_account_balance(account_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()
    db.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": result['balance']}

# Define la ruta para obtener todas las cuentas
@app.get("/accounts/", response_model=List[Account])
def get_all_accounts():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, balance FROM accounts")
    result = cursor.fetchall()
    db.close()
    return result

# Define la ruta para obtener una cuenta por ID
@app.get("/accounts/{account_id}")
def get_account(account_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, balance FROM accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()
    db.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

# Define la ruta para actualizar una cuenta
@app.put("/accounts/{account_id}")
def update_account(account_id: int, account: Account):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE accounts SET user_id = %s, name = %s, balance = %s WHERE id = %s",
                   (account.user_id, account.name, account.balance, account_id))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}

# Define la ruta para eliminar una cuenta
@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}
