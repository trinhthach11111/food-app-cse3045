import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # Mật khẩu MySQL trên VPS của bạn
        database="food_db"               # BẮT BUỘC phải là food_db
    )
    return connection