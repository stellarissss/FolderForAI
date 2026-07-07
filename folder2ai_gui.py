#这是本项目的核心前端代码
import os

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import folder2ai_core as core

class Folder2AIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 文件夹结构化工具 (Folder2AI)")
        self.root.geometry("650x450")
        self.root.resizable(False, False)
        
        # 设置窗口图标（可选，如果有ico文件）
        # self.root.iconbitmap("icon.ico")
        
        self.folder_path = tk.StringVar()
        self.save_path = tk.StringVar()
        self.clean_data_var = tk.BooleanVar(value=True)

        self.create_widgets()
        
    def create_widgets(self):
        # 标题
        tk.Label(self.root, text="stellaris小工具之文件夹结构化工具", font=("微软雅黑", 14, "bold")).pack(pady=15)
        
        # 选择文件夹
        frame1 = tk.Frame(self.root)
        frame1.pack(fill="x", padx=20, pady=5)
        tk.Label(frame1, text="选择文件夹：", font=("微软雅黑", 10)).pack(side="left")
        tk.Entry(frame1, textvariable=self.folder_path, font=("微软雅黑", 10), width=40).pack(side="left", padx=5)
        tk.Button(frame1, text="浏览...", font=("微软雅黑", 10), command=self.browse_folder).pack(side="left")
        
        # 选择保存位置
        frame2 = tk.Frame(self.root)
        frame2.pack(fill="x", padx=20, pady=5)
        tk.Label(frame2, text="输出文件名：", font=("微软雅黑", 10)).pack(side="left")
        tk.Entry(frame2, textvariable=self.save_path, font=("微软雅黑", 10), width=40).pack(side="left", padx=5)
        tk.Button(frame2, text="浏览...", font=("微软雅黑", 10), command=self.browse_save).pack(side="left")
        
        # 默认保存名称
        self.save_path.set(os.path.join(os.path.expanduser("~"), "Desktop", "项目结构化输出.txt"))

        # 数据清洗选项
        frame_clean = tk.Frame(self.root)
        frame_clean.pack(fill="x", padx=20, pady=10)
        tk.Checkbutton(
            frame_clean,
            text="启用数据清洗（自动识别乱码并替换为[无法识别]）",
            variable=self.clean_data_var,
            font=("微软雅黑", 10)
        ).pack(side="left")

        # 生成按钮
        self.btn_generate = tk.Button(
            self.root, text="🚀 一键生成", font=("微软雅黑", 12, "bold"), 
            bg="#4CAF50", fg="white", relief="flat", width=20, height=2,
            command=self.start_generation
        )
        self.btn_generate.pack(pady=15)
        
        # 日志/状态显示框
        self.log_box = scrolledtext.ScrolledText(self.root, width=75, height=8, font=("微软雅黑", 9))
        self.log_box.pack(padx=20, pady=5)
        self.log("准备就绪。请选择要结构化的文件夹。")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="选择要结构化的文件夹")
        if folder:
            self.folder_path.set(folder)
            # 自动更新默认输出文件名
            folder_name = os.path.basename(folder)
            default_save = os.path.join(os.path.dirname(folder), f"{folder_name}_context.txt")
            self.save_path.set(default_save)
            self.log(f"已选择文件夹: {folder}")

    def browse_save(self):
        file = filedialog.asksaveasfilename(
            title="选择输出位置", 
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file:
            self.save_path.set(file)
            self.log(f"输出路径设为: {file}")

    def start_generation(self):
        src = self.folder_path.get()
        dst = self.save_path.get()
        
        if not src or not os.path.isdir(src):
            messagebox.showerror("错误", "请选择一个有效的文件夹！")
            return
        if not dst:
            messagebox.showerror("错误", "请指定输出文件路径！")
            return
            
        self.btn_generate.config(state="disabled", text="生成中...")
        self.log(f"正在处理: {src} ...")
        
        # 在子线程中执行，防止大文件夹导致界面卡死
        thread = threading.Thread(target=self.run_task, args=(src, dst))
        thread.start()
        
    def run_task(self, src, dst):
        try:
            result = core.generate_output(src, clean_data=self.clean_data_var.get())
            with open(dst, "w", encoding="utf-8") as f:
                f.write(result)
            self.log("✅ 生成完成！")
            self.root.after(0, lambda: messagebox.showinfo("成功", f"文件已成功保存到:\n{dst}"))
        except Exception as e:
            self.log(f"❌ 发生错误: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"生成失败:\n{str(e)}"))
        finally:
            self.root.after(0, lambda: self.btn_generate.config(state="normal", text="🚀 一键生成"))

    def log(self, msg):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")

if __name__ == "__main__":
    root = tk.Tk()
    app = Folder2AIApp(root)
    root.mainloop()
