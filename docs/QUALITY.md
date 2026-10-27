\# Kế hoạch chất lượng (Quality Plan) - Food App



| Hạng mục chất lượng | Ngưỡng đạt đo được (Mục tiêu) | Biện pháp QA (Đảm bảo chất lượng) | Ca kiểm tra QC (Kiểm soát chất lượng) | Người phụ trách | Bằng chứng |

|---|---|---|---|---|---|

| \*\*1. Độ bao phủ mã kiểm thử (Test Coverage)\*\* | ≥ 80% đối với các module lõi (Backend API \& Queue). | Áp dụng TDD (Test-Driven Development); yêu cầu viết unit test mỗi khi thêm tính năng mới. | Chạy lệnh `pytest --cov` cục bộ và tự động qua GitHub Actions (CI) mỗi khi Push/Pull Request. | Trịnh Đình Thạch | Log xanh của GitHub Actions (CI) trên nhánh chính. |

| \*\*2. Thời gian phản hồi API (Performance)\*\* | ≤ 300ms cho 95% các yêu cầu xem menu và đặt món. | Tối ưu hóa truy vấn CSDL SQLite; thiết kế API gọn nhẹ bằng FastAPI. | Dùng Postman hoặc công cụ load test nhẹ để đo thời gian phản hồi (Response time) trên server VPS thật. | Trịnh Đình Thạch | Screenshot kết quả đo thời gian phản hồi từ Postman/Tab Network trình duyệt. |

| \*\*3. Tính khả dụng của Hệ thống (Uptime)\*\* | ≥ 98% trong suốt thời gian chấm đồ án. | Thiết lập service tự động khởi động lại ứng dụng (systemd) trên VPS Linux nếu bị crash. | Ping kiểm tra định kỳ vào IP server `sv25.bcse-vju.com`. | Trịnh Đình Thạch | Log của systemctl trên server VPS / Status page tĩnh. |

