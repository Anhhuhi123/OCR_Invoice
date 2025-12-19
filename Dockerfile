# Sử dụng Python 3.7 làm base image
FROM python:3.7-slim

# Thiết lập working directory
WORKDIR /app

# Cài đặt các dependencies hệ thống cần thiết cho OpenCV và PaddlePaddle
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt trước để tận dụng Docker cache
# Nếu requirements.txt không thay đổi, Docker sẽ sử dụng cache layer
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng FastAPI với uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]