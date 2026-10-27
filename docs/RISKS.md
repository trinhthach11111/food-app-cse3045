\# Sổ đăng ký rủi ro (Risk Register) - Food App



| ID | Rủi ro (Nguyên nhân → Sự kiện → Hậu quả) | Xác suất | Tác động | Ưu tiên | Chiến lược \& Hành động kiểm soát | Người phụ trách | Trạng thái |

|---|---|---|---|---|---|---|---|

| \*\*R1\*\* (Kỹ thuật) | \*\*Nguyên nhân:\*\* Dùng SQLite ở môi trường web.<br>\*\*Sự kiện:\*\* Nhiều kết nối ghi dữ liệu cùng lúc gây lỗi `database is locked`.<br>\*\*Hậu quả:\*\* Mất đơn hàng của khách, crash hệ thống. | Trung bình | Cao | \*\*Cao\*\* | \*\*Giảm thiểu (Mitigate):\*\* Sử dụng cơ chế hàng đợi (Queue) đã làm ở HW2 để xử lý đơn hàng tuần tự; cân nhắc đổi sang PostgreSQL nếu cần. | Trịnh Đình Thạch | Đang theo dõi |

| \*\*R2\*\* (Kỹ thuật) | \*\*Nguyên nhân:\*\* Cấu hình VPS/Linux chưa chuẩn.<br>\*\*Sự kiện:\*\* Cổng mạng (Port) bị tường lửa chặn hoặc xung đột.<br>\*\*Hậu quả:\*\* Ứng dụng không thể truy cập từ bên ngoài. | Thấp | Rất cao | \*\*Cao\*\* | \*\*Tránh (Avoid):\*\* Chuẩn hóa file cấu hình và test trên máy ảo local trước khi deploy lên `sv25.bcse-vju.com`. | Trịnh Đình Thạch | Đang theo dõi |

| \*\*R3\*\* (Kỹ thuật) | \*\*Nguyên nhân:\*\* Thuật toán tìm kiếm/lọc món ăn chưa tối ưu.<br>\*\*Sự kiện:\*\* API load quá lâu khi danh sách món ăn lớn.<br>\*\*Hậu quả:\*\* Trải nghiệm người dùng kém (Lag). | Thấp | Trung bình | \*\*Vừa\*\* | \*\*Giảm thiểu (Mitigate):\*\* Giới hạn số lượng hiển thị (Pagination), thêm chỉ mục (Index) cho CSDL. | Trịnh Đình Thạch | Đang theo dõi |

| \*\*R4\*\* (Con người) | \*\*Nguyên nhân:\*\* Dự án chỉ có 1 thành viên.<br>\*\*Sự kiện:\*\* Quá tải khối lượng công việc (Full-stack, QA, Docs).<br>\*\*Hậu quả:\*\* Trễ tiến độ (Sprint 0, 1). | Cao | Cao | \*\*Rất Cao\*\* | \*\*Chấp nhận \& Kiểm soát:\*\* Áp dụng chặt chẽ WBS/Gantt; ưu tiên làm các tính năng cốt lõi (MVP) trước, cắt bỏ tính năng phụ. | Trịnh Đình Thạch | Kích hoạt |

| \*\*R5\*\* (Con người) | \*\*Nguyên nhân:\*\* Lịch thi các môn học khác (An toàn thông tin, Machine Learning) dày đặc.<br>\*\*Sự kiện:\*\* Quỹ thời gian code bị giảm sút.<br>\*\*Hậu quả:\*\* Không kịp test CI hoặc viết báo cáo. | Cao | Trung bình | \*\*Cao\*\* | \*\*Giảm thiểu (Mitigate):\*\* Code dứt điểm từng module nhỏ mỗi tối; không dồn việc vào sát deadline nộp báo cáo. | Trịnh Đình Thạch | Kích hoạt |

| \*\*R6\*\* (Phạm vi) | \*\*Nguyên nhân:\*\* Phát sinh nhiều ý tưởng mới trong quá trình code.<br>\*\*Sự kiện:\*\* Scope creep (phạm vi phình to).<br>\*\*Hậu quả:\*\* Không thể hoàn thành dự án trong khuôn khổ môn học. | Trung bình | Cao | \*\*Cao\*\* | \*\*Tránh (Avoid):\*\* Bám sát đúng Backlog Sprint 0; chỉ nâng cấp sau khi bản MVP đã chạy ổn định. | Trịnh Đình Thạch | Đóng băng |

