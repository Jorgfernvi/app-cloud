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

@app.post("/transfer")
def transfer_funds(transfer_request: schemas.TransferRequest):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT id, balance FROM accounts WHERE id IN (%s, %s)",
                   (transfer_request.from_account, transfer_request.to_account))
    accounts = cursor.fetchall()

    if len(accounts) != 2:
        db.close()
        raise HTTPException(status_code=404, detail="One or both accounts not found")

    from_account_balance = next(acc['balance'] for acc in accounts if acc['id'] == transfer_request.from_account)
    to_account_balance = next(acc['balance'] for acc in accounts if acc['id'] == transfer_request.to_account)

    if from_account_balance < transfer_request.amount:
        db.close()
        raise HTTPException(status_code=400, detail="Insufficient funds")

    new_from_balance = from_account_balance - transfer_request.amount
    new_to_balance = to_account_balance + transfer_request.amount

    cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_from_balance, transfer_request.from_account))
    cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_to_balance, transfer_request.to_account))

    cursor.execute("INSERT INTO transactions (from_account, to_account, amount, transaction_type) VALUES (%s, %s, %s, 'internal')",
                   (transfer_request.from_account, transfer_request.to_account, transfer_request.amount))
    db.commit()
    db.close()

    return {"message": "Transfer successful"}

