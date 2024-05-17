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

@app.post("/login")
def login_user(user: schemas.UserLogin):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (user.username, user.password))
    result = cursor.fetchone()
    if result is None:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = "some_generated_token"  # Generate a real token here
    cursor.execute("INSERT INTO tokens (user_id, token) VALUES (%s, %s)", (result['id'], token))
    db.commit()
    db.close()
    return {"token": token}

@app.post("/register")
def register_user(user: schemas.UserRegister):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (user.username, user.password, user.email))
    db.commit()
    db.close()
    return {"message": "User registered successfully"}

