import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
import mysql.connector

from backend.db import get_db_connection

app = FastAPI(title="VJU Food API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UPLOAD_DIR = "frontend/uploads"
IMAGE_DIR = "frontend/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    customer_id: int
    delivery_area: str
    payment_method: str
    items: List[OrderItemSchema]

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "VJU Food API đang hoạt động bình thường!"}

# --- API ĐĂNG KÝ (Có Upload Avatar) ---
@app.post("/api/register")
@app.post("/register")
async def register(
    fullname: str = Form(...),
    username: str = Form(...),
    email: str = Form(""),
    password: str = Form(...),
    role: str = Form(...),
    avatar: UploadFile = File(None)
):
    if role not in ['customer', 'seller', 'shipper']:
        raise HTTPException(status_code=400, detail="Vai trò không hợp lệ!")

    avatar_url = "/uploads/default-avatar.png"
    if avatar and avatar.filename:
        file_filename = f"{username}_{avatar.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        avatar_url = f"/uploads/{file_filename}"

    hashed_pwd = pwd_context.hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO users (fullname, username, email, password_hash, role, avatar_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (fullname, username, email, hashed_pwd, role, avatar_url))
        conn.commit()
        return {"message": "Đăng ký thành công!"}
    except mysql.connector.Error:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Tên đăng nhập hoặc Email đã tồn tại!")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# --- API ĐĂNG NHẬP ---
@app.post("/api/login")
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác!")

        is_valid = False
        try:
            is_valid = pwd_context.verify(password, user['password_hash'])
        except Exception:
            is_valid = (user['password_hash'] == password)

        if not is_valid:
            raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác!")

        display_name = user.get('fullname') or user.get('username')
        user_avatar = user.get('avatar_url') or '/uploads/default-avatar.png'

        return {
            "message": "Đăng nhập thành công!",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "fullname": display_name,
                "role": user['role'],
                "avatar_url": user_avatar
            },
            "user_id": user['id'],
            "fullname": display_name,
            "role": user['role'],
            "avatar_url": user_avatar
        }
    finally:
        cursor.close()
        conn.close()

# --- API LẤY DANH SÁCH MÓN ĂN ---
@app.get("/products")
@app.get("/api/products")
def get_products(search: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if search and search.strip():
            cursor.execute("SELECT * FROM products WHERE name LIKE %s AND is_available = TRUE", (f"%{search.strip()}%",))
        else:
            cursor.execute("SELECT * FROM products WHERE is_available = TRUE")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# --- API TẠO ĐƠN HÀNG ---
@app.post("/orders")
@app.post("/api/orders")
def create_order(order: CreateOrderSchema):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        total_amount = 0
        for item in order.items:
            cursor.execute("SELECT price FROM products WHERE id = %s", (item.product_id,))
            p = cursor.fetchone()
            if not p:
                raise HTTPException(status_code=404, detail=f"Món ID {item.product_id} không tồn tại")
            total_amount += float(p['price']) * item.quantity

        order_sql = "INSERT INTO orders (customer_id, delivery_area, total_amount, payment_method) VALUES (%s, %s, %s, %s)"
        cursor.execute(order_sql, (order.customer_id, order.delivery_area, total_amount, order.payment_method))
        order_id = cursor.lastrowid

        for item in order.items:
            item_sql = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(item_sql, (order_id, item.product_id, item.quantity))

        conn.commit()
        return {
            "message": "Đặt hàng thành công!",
            "order_id": order_id,
            "total_amount": total_amount,
            "payment_method": order.payment_method,
            "qr_code_url": f"https://img.vietqr.io/image/MB-0354123456-compact2.png?amount={int(total_amount)}&addInfo=VJUFOOD{order_id}" if order.payment_method == "qr_code" else None
        }
    except HTTPException as he:
        conn.rollback()
        raise he
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")