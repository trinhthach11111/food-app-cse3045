import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",                 # Tên user MySQL của bạn (mặc định là root)
        database="vju_food_db"
    )
    return connection