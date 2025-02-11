# PDF工具助手

一个简单实用的PDF文件处理工具，提供PDF文件分割和合并功能。

## 功能特点

- PDF文件分割：可以按指定页数间隔分割PDF文件
- PDF文件合并：可以将多个PDF文件合并为一个文件
- 简洁的Web界面
- 实时处理进度显示
- 支持批量处理
- 支持大文件处理（单个文件最大100MB）

## 安装要求

- Python 3.8+
- Flask
- PyPDF2
- Docker（可选，用于容器化部署）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/RayYeung1989/pdf_tool.git
cd pdf_tool
```

2. 选择安装方式：

### 方式一：直接安装
```bash
pip install -r requirements.txt
python backend/app.py
```

### 方式二：Docker 部署
```bash
# 构建镜像
docker build -t pdf-tool .

# 运行容器
docker run -d -p 5000:5000 --name pdf-tool pdf-tool

# 如需持久化存储，可以添加卷挂载
docker run -d -p 5000:5000 -v /path/to/local/storage:/app/temp_uploads --name pdf-tool pdf-tool
```

3. 打开浏览器访问：
```
http://localhost:5000
```

## 使用说明

### PDF分割
1. 在网页界面选择"分割PDF"
2. 上传需要分割的PDF文件（最大100MB）
3. 设置分割间隔页数
4. 点击"开始处理"
5. 处理完成后下载分割后的文件（ZIP格式）

### PDF合并
1. 在网页界面选择"合并PDF"
2. 上传需要合并的多个PDF文件（每个文件最大100MB）
3. 点击"开始处理"
4. 处理完成后下载合并后的PDF文件

## 注意事项

- 单个文件大小限制为100MB
- 支持批量处理多个文件
- 临时文件会保存在temp_uploads目录中
- 建议在生产环境中使用Docker部署

## 许可证

MIT License 