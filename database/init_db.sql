CREATE DATABASE IF NOT EXISTS vju_food_db;
USE vju_food_db;

-- 1. Bảng Người dùng (Sinh viên, Người bán, Shipper)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('customer', 'seller', 'shipper') DEFAULT 'customer',
    full_name VARCHAR(100),
    phone VARCHAR(20)
);

-- 2. Bảng Món ăn & Đồ uống
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT,
    name VARCHAR(100) NOT NULL,
    category ENUM('food', 'drink') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(255),
    description TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- 3. Bảng Đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    shipper_id INT,
    delivery_area VARCHAR(100) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('cash', 'qr_code') NOT NULL,
    status ENUM('pending', 'accepted', 'shipping', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (shipper_id) REFERENCES users(id)
);

-- 4. Bảng Chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

USE food_db;

-- Bảng users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('customer', 'seller', 'shipper') NOT NULL DEFAULT 'customer',
    avatar_url VARCHAR(255) DEFAULT '/uploads/default-avatar.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Xóa tài khoản test cũ để làm sạch dữ liệu
DELETE FROM users WHERE username IN ('customer1', 'seller1', 'shipper1');

-- Tạo sẵn 3 tài khoản TEST với Email cố định và Mật khẩu là '123456'
INSERT INTO users (fullname, username, email, password_hash, role, avatar_url) VALUES
('Nguyễn Văn Khách', 'customer1', 'customer1@vju.ac.vn', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'customer', '/uploads/default-avatar.png'),
('Trần Thị Chủ Quán', 'seller1', 'seller1@vju.ac.vn', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'seller', '/uploads/default-avatar.png'),
('Lê Văn Shipper', 'shipper1', 'shipper1@vju.ac.vn', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeg6Lruj3vjPGga31lW', 'shipper', '/uploads/default-avatar.png');