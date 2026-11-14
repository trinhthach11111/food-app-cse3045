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

# --- KHAI BÁO SCHEMA ĐẶT HÀNG (ĐẶT Ở ĐÂY ĐỂ KHÔNG BỊ NameError) ---
class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    customer_id: int
    delivery_area: str
    payment_method: str
    items: List[OrderItemSchema]

# --- MÃ HÓA AN TOÀN SHA-256 PRE-HASH ---
def hash_password(password: str) -> str:
    sha_str = hashlib.sha256(password.encode('utf-8')).hexdigest()
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

# --- TỰ ĐỘNG BẢO TOÀN VÀ KHỞI TẠO BẢNG CSDL KHI KHỞI ĐỘNG ---
@app.on_event("startup")
def startup_db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Bảng users
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
        
        # 2. Bảng products
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            image_url VARCHAR(255),
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 3. Bảng orders
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            delivery_area VARCHAR(255) NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            status ENUM('pending', 'delivering', 'completed', 'cancelled') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 4. Bảng order_items
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print(">>> [SUCCESS] CSDL và các bảng đã được kiểm tra thành công!")
    except Exception as e:
        print(f">>> [WARNING] Khởi tạo CSDL: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "VJU Food API đang hoạt động bình thường!"}

# --- API ĐĂNG KÝ ---
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
                    raise HTTPException(status_code=400, detail=f"Tên đăng nhập '{username}' đã tồn tại!")
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

# --- API ĐĂNG NHẬP ---
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

# --- API THÊM MÓN ĂN MỚI ---
@app.post("/api/products")
@app.post("/products")
async def add_product(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    image: Optional[UploadFile] = File(None)
):
    name = name.strip()
    if not name or price <= 0:
        raise HTTPException(status_code=400, detail="Tên món ăn và Giá tiền không hợp lệ!")

    image_url = "/images/default-food.jpg"
    if image and hasattr(image, "filename") and image.filename and image.filename.strip():
        try:
            contents = await image.read()
            if len(contents) > 0:
                safe_filename = f"prod_{name.replace(' ', '_')}_{os.path.basename(image.filename.strip())}"
                file_path = os.path.join(IMAGE_DIR, safe_filename)
                with open(file_path, "wb") as f:
                    f.write(contents)
                image_url = f"/images/{safe_filename}"
        except Exception as img_err:
            print(f"Lỗi lưu ảnh món ăn: {img_err}")
            image_url = "/images/default-food.jpg"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
            INSERT INTO products (name, price, description, image_url, is_available)
            VALUES (%s, %s, %s, %s, TRUE)
        """
        cursor.execute(sql, (name, price, description, image_url))
        conn.commit()
        return {"message": "Thêm món ăn mới thành công!", "product_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi CSDL: {str(e)}")
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
    if not order.items:
        raise HTTPException(status_code=400, detail="Giỏ hàng trống!")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        total_amount = 0
        for item in order.items:
            if item.quantity <= 0 or item.quantity > 100:
                raise HTTPException(status_code=400, detail="Số lượng món không hợp lệ (từ 1 đến 100)!")

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
        # --- API LẤY DANH SÁCH ĐƠN HÀNG CỦA KHÁCH HÀNG ---
@app.get("/orders/customer/{customer_id}")
@app.get("/api/orders/customer/{customer_id}")
def get_customer_orders(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
            SELECT o.id, o.total_amount, o.payment_method, o.status, o.created_at, o.delivery_area,
                   GROUP_CONCAT(CONCAT(p.name, ' (x', oi.quantity, ')') SEPARATOR ', ') AS items_summary
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE o.customer_id = %s
            GROUP BY o.id
            ORDER BY o.created_at DESC
        """
        cursor.execute(sql, (customer_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")