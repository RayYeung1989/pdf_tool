import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF处理助手")
        
        # 创建主框架
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # 分割PDF界面
        self.split_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.split_frame, text='分割PDF')
        self._create_split_ui()

        # 合并PDF界面
        self.merge_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.merge_frame, text='合并PDF')
        self._create_merge_ui()

        # 创建输出目录
        self.output_dir = os.path.join(os.getcwd(), 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def _create_split_ui(self):
        # 文件选择
        ttk.Label(self.split_frame, text="选择PDF文件:").grid(row=0, column=0, padx=5, pady=5)
        self.split_file_path = tk.StringVar()
        ttk.Entry(self.split_frame, textvariable=self.split_file_path, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(self.split_frame, text="浏览...", command=self._select_split_file).grid(row=0, column=2)

        # 分割间隔
        ttk.Label(self.split_frame, text="分割间隔页数:").grid(row=1, column=0, padx=5, pady=5)
        self.interval = tk.IntVar(value=1)
        ttk.Spinbox(self.split_frame, from_=1, to=100, textvariable=self.interval, width=5).grid(row=1, column=1, sticky='w')

        # 执行按钮
        ttk.Button(self.split_frame, text="开始分割", command=self.split_pdf).grid(row=2, column=0, columnspan=3, pady=10)

        # 状态显示
        self.split_status = ttk.Label(self.split_frame, text="")
        self.split_status.grid(row=3, column=0, columnspan=3)

    def _create_merge_ui(self):
        # 文件列表
        self.merge_files = []
        self.listbox = tk.Listbox(self.merge_frame, width=50, height=6)
        self.listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # 按钮组
        ttk.Button(self.merge_frame, text="添加文件", command=self._add_merge_file).grid(row=1, column=0)
        ttk.Button(self.merge_frame, text="上移", command=lambda: self._move_item(-1)).grid(row=1, column=1)
        ttk.Button(self.merge_frame, text="下移", command=lambda: self._move_item(1)).grid(row=2, column=0)
        ttk.Button(self.merge_frame, text="删除", command=self._remove_item).grid(row=2, column=1)
        ttk.Button(self.merge_frame, text="开始合并", command=self.merge_pdf).grid(row=3, column=0, columnspan=2, pady=10)

        # 状态显示
        self.merge_status = ttk.Label(self.merge_frame, text="")
        self.merge_status.grid(row=4, column=0, columnspan=2)

    def _select_split_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if file_path:
            self.split_file_path.set(file_path)

    def split_pdf(self):
        input_path = self.split_file_path.get()
        interval = self.interval.get()
        
        if not input_path:
            messagebox.showerror("错误", "请选择要分割的PDF文件")
            return
            
        try:
            with open(input_path, 'rb') as f:
                reader = PdfReader(f)
                total_pages = len(reader.pages)
                
                for i in range(0, total_pages, interval):
                    writer = PdfWriter()
                    start = i + 1
                    end = min(i + interval, total_pages)
                    
                    for page_num in range(i, end):
                        writer.add_page(reader.pages[page_num])
                        
                    output_path = os.path.join(
                        self.output_dir,
                        f"split_{start:03d}-{end:03d}.pdf"
                    )
                    
                    with open(output_path, 'wb') as out_f:
                        writer.write(out_f)
                        
                messagebox.showinfo("完成", f"成功分割为{total_pages//interval +1}个文件")
                self.split_status.config(text=f"分割完成，保存至：{self.output_dir}")
                
        except Exception as e:
            messagebox.showerror("错误", f"分割失败：{str(e)}")

    def _add_merge_file(self):
        files = filedialog.askopenfilenames(
            filetypes=[("PDF文件", "*.pdf")],
            title="选择要合并的PDF文件"
        )
        if files:
            self.merge_files.extend(files)
            self.listbox.delete(0, tk.END)
            for file in self.merge_files:
                self.listbox.insert(tk.END, os.path.basename(file))

    def _move_item(self, direction):
        selected = self.listbox.curselection()
        if not selected:
            return
            
        index = selected[0]
        new_index = index + direction
        
        if 0 <= new_index < len(self.merge_files):
            # 交换列表中的位置
            self.merge_files[index], self.merge_files[new_index] = (
                self.merge_files[new_index], self.merge_files[index]
            )
            
            # 更新列表显示
            self.listbox.delete(index)
            self.listbox.insert(
                new_index,
                os.path.basename(self.merge_files[new_index])
            )

    def _remove_item(self):
        selected = self.listbox.curselection()
        if not selected:
            return
            
        index = selected[0]
        del self.merge_files[index]
        self.listbox.delete(index)

    def merge_pdf(self):
        if not self.merge_files:
            messagebox.showerror("错误", "请添加要合并的PDF文件")
            return
            
        output_path = os.path.join(
            self.output_dir,
            "merged_result.pdf"
        )
        
        try:
            writer = PdfWriter()
            
            for file in self.merge_files:
                with open(file, 'rb') as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        writer.add_page(page)
                        
            with open(output_path, 'wb') as f:
                writer.write(f)
                
            messagebox.showinfo("完成", f"文件合并成功：{output_path}")
            self.merge_status.config(text=f"合并完成：{output_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"合并失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()
