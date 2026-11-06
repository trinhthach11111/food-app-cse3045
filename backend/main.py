#from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from backend.db import get_db_connection

app = FastAPI(title="VJU Food API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
class UserRegister(BaseModel):
    username: str
    password: str
    role: str
    full_name: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    customer_id: int
    delivery_area: str
    payment_method: str  # 'cash' hoặc 'qr_code'
    items: List[OrderItemSchema]

# --- Route Trang chủ (Health Check) ---
@app.get("/")
def read_root():
    return {"status": "online", "message": "VJU Food Backend API is running!"}

# --- API Đăng ký / Đăng nhập ---
@app.post("/register")
def register(user: UserRegister):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, password_hash, role, full_name, phone) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (user.username, user.password, user.role, user.full_name, user.phone))
        conn.commit()
        return {"message": "Đăng ký thành công!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Lỗi đăng ký hoặc Username đã tồn tại")
    finally:
        cursor.close()
        conn.close()

@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, username, role, full_name FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (user.username, user.password))
        account = cursor.fetchone()
        if account:
            return {"message": "Đăng nhập thành công", "user": account}
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")
    finally:
        cursor.close()
        conn.close()

# --- API Danh sách & Tìm kiếm món ăn ---
@app.get("/products")
def get_products(search: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if search:
            query = "SELECT * FROM products WHERE name LIKE %s AND is_available = TRUE"
            cursor.execute(query, (f"%{search}%",))
        else:
            query = "SELECT * FROM products WHERE is_available = TRUE"
            cursor.execute(query)
        products = cursor.fetchall()
        return products
    finally:
        cursor.close()
        conn.close()

# --- API Tạo đơn hàng & Thanh toán ---
@app.post("/orders")
def create_order(order: CreateOrderSchema):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Tính tổng tiền từ CSDL
        total_amount = 0
        for item in order.items:
            cursor.execute("SELECT price FROM products WHERE id = %s", (item.product_id,))
            p = cursor.fetchone()
            if not p:
                raise HTTPException(status_code=404, detail=f"Món ID {item.product_id} không tồn tại")
            total_amount += float(p['price']) * item.quantity

        # Tạo bản ghi đơn hàng
        order_sql = "INSERT INTO orders (customer_id, delivery_area, total_amount, payment_method) VALUES (%s, %s, %s, %s)"
        cursor.execute(order_sql, (order.customer_id, order.delivery_area, total_amount, order.payment_method))
        order_id = cursor.lastrowid

        # Thêm chi tiết món ăn
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
        # Khai báo phục vụ các file giao diện HTML/CSS/JS tại đường dẫn gốc "/"
#app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")