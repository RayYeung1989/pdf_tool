# 使用 Python 3.8 作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=backend/app.py \
    FLASK_ENV=production

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY backend ./backend
COPY frontend ./frontend

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 创建用于存储上传文件的目录
RUN mkdir -p temp_uploads && chmod 777 temp_uploads

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:app"] 