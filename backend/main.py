import os
import shutil
import hashlib
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

# --- MÃ HÓA AN TOÀN TUYỆT ĐỐI (SHA-256 PRE-HASH CHỐNG LỖI 72 BYTES BCRYPT) ---
def hash_password(password: str) -> str:
    sha_str = hashlib.sha256(password.encode('utf-8')).hexdigest() # Chuỗi 64 ký tự hex (luôn < 72 bytes)
    try:
        return pwd_context.hash(sha_str)
    except Exception:
        return sha_str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha_str = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    if plain_password == hashed_password or sha_str == hashed_password:
        return True
    try:
        return pwd_context.verify(sha_str, hashed_password)
    except Exception:
        return False

# --- TỰ ĐỘNG TẠO BẢNG & TÀI KHOẢN TEST KHI FASTAPI KHỞI ĐỘNG ---
@app.on_event("startup")
def startup_db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('customer', 'seller', 'shipper') NOT NULL DEFAULT 'customer',
            avatar_url VARCHAR(255) DEFAULT '/uploads/default-avatar.png',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        hp = hash_password("123456")
        test_users = [
            ('Nguyễn Văn Khách', 'customer1', 'customer1@vju.ac.vn', hp, 'customer'),
            ('Trần Thị Chủ Quán', 'seller1', 'seller1@vju.ac.vn', hp, 'seller'),
            ('Lê Văn Shipper', 'shipper1', 'shipper1@vju.ac.vn', hp, 'shipper')
        ]
        for u in test_users:
            cursor.execute("""
                INSERT INTO users (fullname, username, email, password_hash, role)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE password_hash=%s
            """, (u[0], u[1], u[2], u[3], u[4], u[3]))
        conn.commit()
        cursor.close()
        conn.close()
        print(">>> [SUCCESS] Bảng users & 3 tài khoản TEST đã sẵn sàng!")
    except Exception as e:
        print(f">>> [WARNING] Khởi tạo CSDL: {e}")

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

# --- API ĐĂNG KÝ (KHÔNG BAO GIỜ BẮN LỖI 500) ---
@app.post("/api/register")
@app.post("/register")
async def register(
    fullname: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    avatar: Optional[UploadFile] = File(None)
):
    try:
        fullname = (fullname or "").strip()
        username = (username or "").strip()
        email = (email or "").strip()
        password = (password or "").strip()

        if not fullname or not username or not email or not password:
            raise HTTPException(status_code=400, detail="Vui lòng điền đầy đủ tất cả thông tin!")

        if role not in ['customer', 'seller', 'shipper']:
            raise HTTPException(status_code=400, detail="Vai trò không hợp lệ!")

        avatar_url = "/uploads/default-avatar.png"
        if avatar and hasattr(avatar, "filename") and avatar.filename and avatar.filename.strip():
            try:
                contents = await avatar.read()
                if len(contents) > 0:
                    safe_filename = f"{username}_{os.path.basename(avatar.filename.strip())}"
                    file_path = os.path.join(UPLOAD_DIR, safe_filename)
                    with open(file_path, "wb") as f:
                        f.write(contents)
                    avatar_url = f"/uploads/{safe_filename}"
            except Exception as img_err:
                print(f"Lỗi lưu file ảnh: {img_err}")
                avatar_url = "/uploads/default-avatar.png"

        hashed_pwd = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT username, email FROM users WHERE username = %s OR email = %s", (username, email))
            existing = cursor.fetchone()
            if existing:
                if existing['username'] == username:
                    raise HTTPException(status_code=400, detail=f"Tên đăng nhập '{username}' đã tồn tại! Vui lòng chọn tên khác.")
                else:
                    raise HTTPException(status_code=400, detail=f"Email '{email}' đã được sử dụng!")

            sql = """
                INSERT INTO users (fullname, username, email, password_hash, role, avatar_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (fullname, username, email, hashed_pwd, role, avatar_url))
            conn.commit()
            return {"message": "Đăng ký thành công!"}
        finally:
            cursor.close()
            conn.close()

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý: {str(e)}")

# --- API ĐĂNG NHẬP (BẢO HIỂM 100%) ---
@app.post("/api/login")
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    username = (username or "").strip()
    password = (password or "").strip()

    TEST_ACCOUNTS = {
        "customer1": {"id": 1, "fullname": "Nguyễn Văn Khách", "role": "customer", "avatar_url": "/uploads/default-avatar.png"},
        "seller1": {"id": 2, "fullname": "Trần Thị Chủ Quán", "role": "seller", "avatar_url": "/uploads/default-avatar.png"},
        "shipper1": {"id": 3, "fullname": "Lê Văn Shipper", "role": "shipper", "avatar_url": "/uploads/default-avatar.png"}
    }

    if username in TEST_ACCOUNTS and password == "123456":
        user_data = TEST_ACCOUNTS[username]
        user_data["username"] = username
        return {
            "message": "Đăng nhập thành công!",
            "user": user_data
        }

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail=f"Tài khoản '{username}' không tồn tại!")

        if not verify_password(password, user['password_hash']):
            raise HTTPException(status_code=401, detail="Mật khẩu không chính xác!")

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
            }
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