from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "44.218.163.17"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_noti"

def get_db_connection():
    return mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )

@app.post("/notifications")
def create_notification(notification: schemas.Notification):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO notifications (user_id, message, status) VALUES (%s, %s, 'unread')", 
                   (notification.user_id, notification.message))
    db.commit()
    notification_id = cursor.lastrowid
    db.close()
    return {"notification_id": notification_id, "message": "Notification created successfully"}

@app.get("/notifications/{user_id}")
def get_notifications(user_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE user_id = %s", (user_id,))
    notifications = cursor.fetchall()
    db.close()
    return {"user_id": user_id, "notifications": notifications}

@app.get("/notifications/{notification_id}")
def get_notification(notification_id: int):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE id = %s", (notification_id,))
    notification = cursor.fetchone()
    db.close()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.put("/notifications/{notification_id}/read")
def mark_notification_as_read(notification_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE notifications SET status = 'read' WHERE id = %s", (notification_id,))
    db.commit()
    db.close()
    return {"message": "Notification marked as read"}

@app.put("/notifications/{user_id}/read")
def mark_all_notifications_as_read(user_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE notifications SET status = 'read' WHERE user_id = %s", (user_id,))
    db.commit()
    db.close()
    return {"message": "All notifications marked as read for user with ID: {}".format(user_id)}

@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
    db.commit()
    db.close()
    return {"message": "Notification deleted successfully"}

