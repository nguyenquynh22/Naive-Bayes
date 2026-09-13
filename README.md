# Car Price Valuation Service - Naive Bayes Pipeline 🚗

Hệ thống microservice phân loại và đánh giá mức giá xe cũ (Ví dụ: **DAT** / **Re**) dựa trên mô hình **Naive Bayes**. Dữ liệu được mã hóa và chuẩn hóa qua `preprocessor.pkl`, hệ thống được đóng gói hoàn chỉnh bằng **Docker Compose** và public ra ngoài internet thông qua **ngrok**.

> **⚠️ Lưu ý:** Mô hình được xây dựng cho mục đích tham khảo và định giá sơ bộ, không thay thế hoàn toàn cho thẩm định viên chuyên nghiệp.

---

## 📁 Cấu trúc Thư mục Dự án

```text
ML/
├── app/                  # AI Microservice (Port 8001)
│   ├── main.py           # FastAPI Server load mô hình & xử lý dự đoán
│   ├── model.pkl         # Mô hình Naive Bayes đã train
│   └── preprocessor.pkl   # Pipeline tiền xử lý (Categorical Encoder & Scaler)
├── backend/              # Backend Gateway (Port 8000)
│   └── main.py           # FastAPI Proxy tiếp nhận & chuyển tiếp request
├── .dockerignore         # Các file bỏ qua khi build Docker image
├── .env                  # Biến môi trường (Ngrok Token, Service URLs)
├── docker-compose.yml    # Cấu hình khởi chạy đa container (Backend, AI Server, Ngrok)
├── Dockerfile            # Dockerfile build môi trường Python
├── ngrok.yml             # Cấu hình tunnel public tự động cho 2 luồng port
├── requirements.txt      # Thư viện Python phụ thuộc
└── README.md             # Tài liệu hướng dẫn dự án
```
# Test:
http://localhost:4040
https://unaltered-eagle-wackiness.ngrok-free.dev/predict

Các endpoint public:

- `/docs`
- `/health`
- `POST /predict`
```text
{
"brand": "Honda",
"car_age": 2,
"mileage_km": 45000.0,
"fuel_type": "Gasoline",
"transmission": "Automatic",
"condition": "Good"
}
```

# 200
```text
{
"status": "success",
"input_summary": {
"brand": "Honda",
"car_age": 2,
"mileage_km": 45000,
"fuel_type": "Gasoline",
"transmission": "Automatic",
"condition": "Good"
},
"prediction": "DAT",
"probabilities": {
"Dat": "98.0%",
"Re": "2.0%"
}
}
```
