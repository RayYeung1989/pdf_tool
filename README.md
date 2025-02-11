# PDF工具助手

一个简单实用的PDF文件处理工具，提供PDF文件分割和合并功能。

## 功能特点

- PDF文件分割：可以按指定页数间隔分割PDF文件
- PDF文件合并：可以将多个PDF文件合并为一个文件
- 简洁的Web界面
- 实时处理进度显示
- 支持批量处理

## 安装要求

- Python 3.8+
- Flask
- PyPDF2

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/pdf_tool.git
cd pdf_tool
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python backend/app.py
```

4. 打开浏览器访问：
```
http://localhost:5000
```

## 使用说明

### PDF分割
1. 在网页界面选择"分割PDF"
2. 上传需要分割的PDF文件
3. 设置分割间隔页数
4. 点击"开始处理"
5. 处理完成后下载分割后的文件（ZIP格式）

### PDF合并
1. 在网页界面选择"合并PDF"
2. 上传需要合并的多个PDF文件（注意上传顺序）
3. 点击"开始处理"
4. 处理完成后下载合并后的PDF文件

## 注意事项

- 上传文件大小限制为16MB
- 建议在开发环境中使用，生产环境请使用生产级WSGI服务器
- 临时文件会保存在temp_uploads目录中

## 许可证

MIT License 