# Nền tảng đặt và giao đồ ăn trực tuyến (Food App)

**Sinh viên thực hiện:** Trịnh Đình Thạch — MSV: 23110218 (Vai trò: Full-stack)

## Bản mô tả dự án sơ bộ (Project Charter Mini)

### 1. Mục tiêu
Xây dựng một trang web giúp sinh viên Đại học Việt Nhật (VJU) dễ dàng đặt đồ ăn nhanh chóng, tiện lợi, hỗ trợ giao tận nơi trong khuôn viên cơ sở Hòa Lạc nhằm tiết kiệm thời gian nghỉ trưa.

### 2. Phạm vi dự án
*   **Sẽ làm:** 
    *   Giao diện xem thực đơn, giỏ hàng, đặt món.
    *   **Tích hợp thanh toán trực tuyến qua thẻ ngân hàng/ví điện tử.**
    *   **Tính năng theo dõi lộ trình shipper thời gian thực (hiển thị bản đồ và vị trí giao hàng).**
*   **Không làm:** Không tích hợp hệ thống hóa đơn điện tử phức tạp của cơ quan thuế hoặc liên kết trực tiếp với ngân hàng nhà nước (sử dụng cổng thanh toán sandbox/mô phỏng).

### 3. Các bên liên quan
*   **Khách hàng:** Sinh viên, giảng viên và nhân viên VJU tại Hòa Lạc.
*   **Người cung cấp:** Căn tin trường hoặc các quán ăn lân cận.
*   **Nhóm phát triển:** Trịnh Đình Thạch (đảm nhiệm toàn bộ frontend, backend và testing).

### 4. Ba (3) ràng buộc
1.  **Ràng buộc thời gian:** Phải hoàn thành các mốc tính năng và báo cáo đúng thời hạn của môn học CSE3045.
2.  **Ràng buộc nguồn lực:** Dự án được thực hiện độc lập bởi 1 người nên quy mô tính năng phải được thu gọn, tập trung vào luồng đặt hàng cốt lõi.
3.  **Ràng buộc kỹ thuật:** Hệ thống bắt buộc phải được deploy và chạy ổn định trên máy chủ VPS do trường cấp (`sv25.bcse-vju.com`).
