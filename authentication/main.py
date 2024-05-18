from fastapi import FastAPI, HTTPException, Depends
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_authen"

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

@app.post("/verify-token")
def verify_token(token: schemas.TokenVerification):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM tokens WHERE token = %s", (token.token,))
    result = cursor.fetchone()
    db.close()
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": result['user_id']}

@app.post("/logout")
def logout_user(token: schemas.TokenVerification):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tokens WHERE token = %s", (token.token,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Logged out successfully"}

@app.put("/change-password")
def change_password(change_password_data: schemas.ChangePassword):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE id = %s AND password = %s", (change_password_data.user_id, change_password_data.old_password))
    result = cursor.fetchone()
    if result is None:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (change_password_data.new_password, change_password_data.user_id))
    db.commit()
    db.close()
    return {"message": "Password changed successfully"}

@app.post("/recover-password")
def recover_password(recover_password_data: schemas.RecoverPassword):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (recover_password_data.email,))
    result = cursor.fetchone()
    if result is None:
        db.close()
        raise HTTPException(status_code=404, detail="Email not found")
    # Generate a recovery token and send it via email
    recovery_token = "some_generated_recovery_token"  # Generate a real recovery token here
    cursor.execute("INSERT INTO recovery_tokens (user_id, token) VALUES (%s, %s)", (result['id'], recovery_token))
    db.commit()
    db.close()
    # Simulate sending email
    print(f"Sending recovery email with token: {recovery_token}")
    return {"message": "Recovery email sent"}



