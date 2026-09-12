from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

# 1. Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="AI Used Car Price Prediction API",
    description="API dự đoán phân loại giá xe cũ dựa trên thuật toán Naive Bayes",
    version="1.0.0"
)

# 2. Xử lý đường dẫn tuyệt đối để load file mô hình .pkl
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "preprocessor.pkl"

# Load model và preprocessor khi import ứng dụng.
try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Load model và preprocessor thành công!")
except Exception as e:
    raise RuntimeError(
        f"Không thể load model/preprocessor từ {MODEL_PATH} và {PREPROCESSOR_PATH}: {e}"
    ) from e

# 3. Định nghĩa Pydantic Schema (Cấu trúc dữ liệu JSON đầu vào)
class CarInput(BaseModel):
    brand: str
    car_age: int
    mileage_km: float
    fuel_type: str
    transmission: str
    condition: str

# 4. Endpoint kiểm tra trạng thái Server (Health Check)
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AI Server Naive Bayes đang hoạt động bình thường!"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "ai"}

# 5. Endpoint chính xử lý Dự đoán (Prediction)
@app.post("/predict")
def predict_price(car: CarInput):
    # Kiểm tra xem mô hình đã sẵn sàng chưa
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Mô hình AI chưa được tải thành công!")
    
    try:
        # Chuyển dữ liệu JSON đầu vào thành pandas DataFrame
        input_data = pd.DataFrame([car.model_dump()])
        
        # Tiền xử lý dữ liệu (Encode + Impute) bằng preprocessor đã lưu
        encoded_data = preprocessor.transform(input_data)
        
        # Dự đoán nhãn (Dat / Re) và xác suất %
        prediction = model.predict(encoded_data)[0]
        probabilities = model.predict_proba(encoded_data)[0]
        
        # Định dạng bảng xác suất % trả về
        proba_dict = {str(cls): f"{prob * 100:.1f}%" for cls, prob in zip(model.classes_, probabilities)}
        
        return {
            "status": "success",
            "input_summary": car.model_dump(),
            "prediction": prediction.upper(),
            "probabilities": proba_dict
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi trong quá trình dự đoán: {str(e)}")