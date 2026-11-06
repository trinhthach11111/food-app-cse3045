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