from flask import Flask, render_template, request, send_file, Response
import os
import sys
from PyPDF2 import PdfReader
import zipfile
from io import BytesIO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from processor import process_pdf
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="../frontend/templates")
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "temp_uploads")
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100MB限制


@app.route("/")
def index():
    return render_template("index.html")


# 进度存储字典
progress_store = {}


@app.route("/progress/<batch_id>")
def get_progress(batch_id):
    return str(progress_store.get(batch_id, 0))


@app.route("/process", methods=["POST"])
def handle_pdf():
    try:
        operation = request.form.get("operation")
        if not operation:
            return "未指定操作类型", 400
            
        files = request.files.getlist("files")
        if not files:
            return "未上传文件", 400

        # 创建临时目录
        batch_id = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(uuid.uuid4())[:6]
        temp_dir = os.path.join(app.config["UPLOAD_FOLDER"], batch_id)
        os.makedirs(temp_dir, exist_ok=True)

        # 保存分页间隔参数
        if operation == "split":
            interval = request.form.get("interval", "1")
            interval_path = os.path.join(temp_dir, "interval.txt")
            with open(interval_path, "w") as f:
                f.write(interval)

        # 保存上传文件
        saved_files = []
        for file in files:
            if file and file.filename.endswith(".pdf"):
                filename = os.path.join(temp_dir, file.filename)
                file.save(filename)
                saved_files.append(filename)
        
        if not saved_files:
            return "没有有效的PDF文件", 400

        # 初始化进度
        progress_store[batch_id] = 0

        # 启动异步处理
        def process_task():
            try:
                if operation == "split":
                    total = len(PdfReader(saved_files[0]).pages)
                else:
                    total = len(saved_files)
                    
                result_file = process_pdf(
                    operation,
                    saved_files,
                    temp_dir,
                    progress_callback=lambda p: update_progress(batch_id, p, total),
                )
                progress_store[batch_id] = 100
            except Exception as e:
                print(f"处理错误: {str(e)}")  # 添加错误日志
                progress_store[batch_id] = -1  # 错误状态码
                raise e

        from threading import Thread
        Thread(target=process_task).start()

        return {"batch_id": batch_id}

    except Exception as e:
        print(f"请求处理错误: {str(e)}")  # 添加错误日志
        return str(e), 500


@app.route("/result/<batch_id>")
def get_result(batch_id):
    temp_dir = os.path.join(app.config["UPLOAD_FOLDER"], batch_id)
    result_file = os.path.join(
        temp_dir, "merged.pdf" if "merge" in batch_id else "splits"
    )
    return {"download_url": f"/process/{batch_id}/result"}


@app.route("/process/<batch_id>/result")
def download_result(batch_id):
    temp_dir = os.path.join(app.config["UPLOAD_FOLDER"], batch_id)
    if "merge" in batch_id:
        result_file = os.path.join(temp_dir, "merged.pdf")
        return send_file(result_file, as_attachment=True, download_name="merged.pdf")
    else:
        # 创建内存中的zip文件
        memory_file = BytesIO()
        splits_dir = os.path.join(temp_dir, "splits")
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 获取所有分割后的PDF文件并按名称排序
            split_files = sorted(os.listdir(splits_dir))
            for filename in split_files:
                if filename.endswith('.pdf'):
                    file_path = os.path.join(splits_dir, filename)
                    zf.write(file_path, filename)  # 将文件添加到zip中
        
        # 将指针移到文件开头
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'split_pdfs_{batch_id}.zip'
        )


def update_progress(batch_id, processed, total):
    progress_store[batch_id] = min(int((processed / total) * 100), 100)


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
