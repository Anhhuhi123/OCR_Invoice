# Sử dụng Ubuntu 22.04 LTS làm base image
FROM ubuntu:22.04

# Thiết lập biến môi trường để tránh tương tác trong quá trình cài đặt
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Thiết lập working directory
WORKDIR /app

# Cài đặt Python 3.11 và các dependencies hệ thống cần thiết
# Layer này sẽ được cache nếu không có thay đổi
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    # Dependencies cho OpenCV
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    # Dependencies cho PaddlePaddle
    libgomp1 \
    libgthread-2.0-0 \
    # Build tools (cần cho một số Python packages)
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Tạo symlink python và pip để dùng Python 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    python3 -m pip install --upgrade pip setuptools wheel

# Copy requirements.txt trước để tận dụng Docker cache layer
# Layer này sẽ được cache nếu requirements.txt không thay đổi
COPY requirements.txt .

# Cài đặt Python dependencies với cache
# Layer này sẽ được cache nếu requirements.txt không thay đổi
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
# Layer này sẽ rebuild khi code thay đổi, nhưng dependencies đã được cache
COPY . .

# Tạo non-root user để chạy ứng dụng (best practice cho security)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Chuyển sang non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Health check để đảm bảo container đang chạy tốt
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Chạy ứng dụng FastAPI với uvicorn trên port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]