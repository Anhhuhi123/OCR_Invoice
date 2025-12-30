# 🚀 OCR Invoice API Server

Server API FastAPI để xử lý OCR hóa đơn - phát hiện và nhận diện văn bản, trích xuất thông tin tự động.

## 📋 Tổng quan

Hệ thống OCR Invoice sử dụng:
- **FastAPI**: Web framework với async support
- **PaddleOCR**: Detection (DBNet) + Recognition (CTC)
- **OpenCV**: Xử lý ảnh và visualization
- **Authentication**: API Key middleware bảo mật

**Chức năng chính:**
- Phát hiện vùng văn bản trong ảnh hóa đơn
- Nhận diện text từ các vùng đã phát hiện
- Trích xuất thông tin: nhà cung cấp, tổng tiền, đơn vị tiền tệ
- Visualize kết quả với bounding boxes

## 📁 Cấu trúc dự án và nhiệm vụ từng file

```
ocr_server/
├── app/
│   ├── main.py                      # FastAPI app, load models khi startup
│   │
│   ├── api/v1/
│   │   ├── endpoints/ocr.py         # 4 API endpoints chính
│   │   └── router.py                # Router tổng hợp endpoints
│   │
│   ├── core/
│   │   ├── config.py                # Cấu hình: đường dẫn models, tham số
│   │   ├── logger.py                # Logging system
│   │   └── middleware.py            # API Key authentication
│   │
│   ├── models/
│   │   ├── detector/
│   │   │   ├── model.py             # Load detection model
│   │   │   └── inference.py         # Inference detection
│   │   │
│   │   └── recognizer/
│   │       ├── model.py             # Load recognition model
│   │       └── inference.py         # Inference recognition + CTC decode
│   │
│   ├── services/
│   │   ├── ocr_service.py           # OCR pipeline: detection + recognition
│   │   └── image_service.py         # Image processing utilities
│   │
│   ├── schemas/ocr.py               # Pydantic response models
│   │
│   ├── utils/
│   │   ├── image.py                 # Expand polygon, extract bbox, visualize
│   │   └── pdf.py                   # PDF processing
│   │
│   └── dependencies/ocr.py          # Dependency injection
│
├── weights/
│   ├── Model_det_small/             # Detection model (DBNet)
│   └── Model_rec/                   # Recognition model (CTC)
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
└── test_api.py                      # Script test APIs
```

## 🚀 Hướng dẫn sử dụng

### 1. Cài đặt

```bash
# Clone repository
git clone https://github.com/Anhhuhi123/OCR_Invoice.git
cd ocr_server

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Cấu hình API key (tùy chọn)
cp .env.example .env
# Sửa API_KEY trong file .env
```

### 2. Chạy server
### 2.1. Bằng terminal
```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
### 2.2 Bằng Docker

```bash
# Build image
docker build -t ocr-api .

# Chạy container
docker run -p 8000:8000 ocr-api
```
Server chạy tại: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Test API

```bash
# Dùng test script
python test_api.py test_image.png

# Dùng curl
curl -X POST "http://localhost:8000/api/v1/ocr/invoice" \
  -H "X-API-Key: your-secret-key" \
  -F "file=@test_image.png"
```

## 📡 Các API

### 1. Trích xuất thông tin hóa đơn
```
POST /api/v1/ocr/invoice
Headers: X-API-Key: your-secret-key
Body: file (image)

Response:
{
  "supplier_name": "Công ty ABC",
  "total": "12500000",
  "currency": "VND"
}
```

### 2. Visualize với bounding boxes
```
POST /api/v1/ocr/invoice/visualize
Headers: X-API-Key: your-secret-key
Body: file (image)

Response: PNG image với bbox và text
```

### 3. Lấy raw bounding boxes
```
POST /api/v1/ocr/invoice/bboxes
Headers: X-API-Key: your-secret-key
Body: file (image)

Response:
{
  "results": [
    {
      "label": "Công ty ABC",
      "text": "Công ty ABC",
      "bbox": [x, y, w, h]
    }
  ]
}
```

### 4. Mock data (testing)
```
GET /api/v1/ocr/mock

Response:
{
  "supplier_name": "ACME Corporation",
  "total": "12500000",
  "currency": "VND"
}
```

---

**Repository**: https://github.com/Anhhuhi123/OCR_Invoice  
**Version**: 1.0.0
