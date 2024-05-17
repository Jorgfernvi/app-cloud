from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel

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

