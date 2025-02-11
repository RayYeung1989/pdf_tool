import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

def process_pdf(operation, files, temp_dir, progress_callback=None):
    try:
        if operation == 'split':
            output_path = os.path.join(temp_dir, 'splits')
            os.makedirs(output_path, exist_ok=True)
            interval = int(open(os.path.join(temp_dir, 'interval.txt')).read())
            result = split_pdf(files[0], interval, output_path, progress_callback)
        elif operation == 'merge':
            os.makedirs(temp_dir, exist_ok=True)
            result = merge_pdf(files, temp_dir, progress_callback)
        else:
            raise ValueError("无效的操作类型")
        
        return result

    finally:
        # 只清理源文件，保留处理结果
        for f in files:
            try:
                if os.path.exists(f) and f != result:
                    os.remove(f)
            except Exception as e:
                print(f"清理文件失败: {str(e)}")

def split_pdf(input_path, interval, output_dir, progress_callback=None):
    with open(input_path, 'rb') as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)
        processed_pages = 0
        
        page_iter = iter(reader.pages)
        
        for batch_index in range(0, total_pages, interval):
            writer = PdfWriter()
            try:
                for _ in range(interval):
                    writer.add_page(next(page_iter))
                    processed_pages += 1
                    if progress_callback:
                        progress_callback(processed_pages)
            except StopIteration:
                pass
            
            start = batch_index + 1
            end = min(batch_index + interval, total_pages)
            output_file = os.path.join(output_dir, f'split_{start:03d}-{end:03d}.pdf')
            
            with open(output_file, 'wb') as out_f:
                writer.write(out_f)
            
            del writer
    
    return output_file

def merge_pdf(files, output_dir, progress_callback=None):
    writer = PdfWriter()
    total_files = len(files)
    
    # 反转文件列表，因为 PyPDF2 是按照添加顺序来合并的
    files = files[::-1]
    
    for index, file in enumerate(files):
        with open(file, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)
            
            if progress_callback:
                progress_callback(index + 1)
    
    output_file = os.path.join(output_dir, 'merged.pdf')
    with open(output_file, 'wb') as f:
        writer.write(f)
    
    if progress_callback:
        progress_callback(total_files)
    
    return output_file
