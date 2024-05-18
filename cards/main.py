from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_cards"

def get_db_connection():
    return mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )

@app.post("/cards")
def create_card(card: schemas.Card):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO cards (user_id, card_number, card_type, balance) VALUES (%s, %s, %s, %s)", 
                   (card.user_id, card.card_number, card.card_type, card.balance))
    db.commit()
    card_id = cursor.lastrowid
    db.close()
    return {"card_id": card_id, "message": "Card created successfully"}

@app.put("/cards/{card_id}/block")
def block_card(card_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE cards SET status = 'blocked' WHERE id = %s", (card_id,))
    db.commit()
    db.close()
    return {"message": "Card blocked successfully"}

@app.get("/cards/{card_id}/transactions")
def get_card_transactions(card_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions WHERE card_id = %s", (card_id,))
    transactions = cursor.fetchall()
    db.close()
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this card")
    return {"card_id": card_id, "transactions": transactions}

@app.get("/cards/{card_id}")
def get_card(card_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cards WHERE id = %s", (card_id,))
    card = cursor.fetchone()
    db.close()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.put("/cards/{card_id}")
def update_card(card_id: int, card: schemas.Card):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE cards SET user_id = %s, card_number = %s, card_type = %s, balance = %s WHERE id = %s",
                   (card.user_id, card.card_number, card.card_type, card.balance, card_id))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card updated successfully"}

@app.delete("/cards/{card_id}")
def delete_card(card_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cards WHERE id = %s", (card_id,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"message": "Card deleted successfully"}

