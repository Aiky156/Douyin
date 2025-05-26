import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import threading

class StorageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("U盘扩展器 - by: 南风梦西洲")
        
        # 设置窗口图标
        try:
            self.root.iconbitmap("logo.ico")
        except:
            print("无法加载窗口图标")
        
        # 设置初始窗口大小
        window_width = 500
        window_height = 400  # 调整初始高度为400
        
        # 获取屏幕尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # 计算窗口位置使其居中
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 允许自由调整窗口大小
        self.root.resizable(True, True)
        
        # 设置最小窗口大小
        self.root.minsize(300, 350)  # 调整最小高度为350
        
        # 创建主框架，使用权重使其能随窗口拉伸
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # 创建设备信息框架（水平布局）
        device_frame = tk.Frame(main_frame)
        device_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 左侧图标框架
        icon_frame = tk.Frame(device_frame)
        icon_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # 加载并显示磁盘图标
        try:
            icon_image = Image.open("disk.ico")
            # 调整图标大小
            icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack(pady=2)
        except Exception as e:
            print(f"无法加载图标: {e}")
            icon_label = tk.Label(
                icon_frame,
                text="💾",
                font=("Segoe UI Emoji", 48)
            )
            icon_label.pack(pady=2)
        
        # 右侧信息框架
        info_frame = tk.Frame(device_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 显示设备标签
        self.storage_label = tk.Label(
            info_frame,
            text="U盘 (E:)",
            font=("Microsoft YaHei", 12),
            anchor="w"
        )
        self.storage_label.pack(fill=tk.X, pady=(4, 2))
        
        # 存储容量进度条
        self.disk_progress = ttk.Progressbar(
            info_frame,
            orient="horizontal",
            mode="determinate",
            style="Disk.Horizontal.TProgressbar"
        )
        self.disk_progress.pack(fill=tk.X, pady=(2, 3))
        
        # 存储信息标签
        self.storage_info = tk.Label(
            info_frame,
            text="64 GB 可用，共 64 GB",
            font=("Microsoft YaHei", 11),
            fg="#666666",  # 设置文本颜色为灰色
            anchor="w"
        )
        self.storage_info.pack(fill=tk.X, pady=(2, 0))
        
        # 创建扩容进度框架
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(40, 0))
        
        # 扩容进度条
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X)
        
        # 进度文本标签
        self.progress_label = tk.Label(
            progress_frame,
            text="准备就绪",
            font=("Microsoft YaHei", 10),
            anchor="w"
        )
        self.progress_label.pack(fill=tk.X, pady=(5, 0))
        
        # 创建圆角按钮
        class RoundedButton(tk.Canvas):
            def __init__(self, parent, width, height, command, text, corner_radius=10, padding=0):
                super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent.cget('bg'))
                
                self.command = command
                
                # 创建圆角矩形
                self.create_rounded_rect(0, 0, width, height, corner_radius, fill='#FF6B6B', outline='#FF6B6B')
                
                # 创建文本
                self.create_text(width/2, height/2, text=text, fill='white', font=('Microsoft YaHei', 10))
                
                # 绑定事件
                self.bind('<Button-1>', self._on_click)
                self.bind('<Enter>', self._on_enter)
                self.bind('<Leave>', self._on_leave)
                
            def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
                points = [
                    x1+radius, y1,
                    x2-radius, y1,
                    x2, y1,
                    x2, y1+radius,
                    x2, y2-radius,
                    x2, y2,
                    x2-radius, y2,
                    x1+radius, y2,
                    x1, y2,
                    x1, y2-radius,
                    x1, y1+radius,
                    x1, y1
                ]
                return self.create_polygon(points, smooth=True, **kwargs)
                
            def _on_click(self, event):
                self.command()
                
            def _on_enter(self, event):
                self.configure(cursor='hand2')
                self.delete('all')
                self.create_rounded_rect(0, 0, self.winfo_width(), self.winfo_height(), 10, 
                                      fill='#FF8787', outline='#FF8787')
                self.create_text(self.winfo_width()/2, self.winfo_height()/2, 
                               text="开始扩容", fill='white', font=('Microsoft YaHei', 10))
                
            def _on_leave(self, event):
                self.configure(cursor='')
                self.delete('all')
                self.create_rounded_rect(0, 0, self.winfo_width(), self.winfo_height(), 10,
                                      fill='#FF6B6B', outline='#FF6B6B')
                self.create_text(self.winfo_width()/2, self.winfo_height()/2,
                               text="开始扩容", fill='white', font=('Microsoft YaHei', 10))
        
        # 使用自定义圆角按钮
        self.convert_button = RoundedButton(
            main_frame,
            width=200,
            height=40,
            command=self.start_conversion,
            text="开始扩容"
        )
        self.convert_button.pack(pady=(40, 30))
        
        # 设置进度条样式
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=12,  # 扩容进度条
            troughcolor='#E0E0E0',
            background='#4CAF50'
        )
        
        style.configure(
            "Disk.Horizontal.TProgressbar",
            thickness=8,  # 磁盘容量进度条
            troughcolor='#E0E0E0',
            background='#2196F3'
        )
        
        # 设置初始进度条值
        self.disk_progress["value"] = 0
        self.progress_bar["value"] = 0
        
        # 转换状态标志
        self.is_converting = False
        
    def start_conversion(self):
        if not self.is_converting:
            self.is_converting = True
            self.convert_button.configure(state='disabled')
            self.progress_label.config(text="正在准备...")
            # 启动转换线程
            threading.Thread(target=self.conversion_process, daemon=True).start()
    
    def conversion_process(self):
        # 模拟转换过程
        for i in range(101):
            if not self.is_converting:
                break
            self.progress_bar["value"] = i
            # 更新进度显示
            if i < 30:
                self.root.after(0, lambda: self.progress_label.config(text="正在扫描设备..."))
            elif i < 60:
                self.root.after(0, lambda: self.progress_label.config(text="正在扩容中..."))
            elif i < 90:
                self.root.after(0, lambda: self.progress_label.config(text="正在写入数据..."))
            time.sleep(0.03)  # 控制进度条速度
        
        # 完成转换
        if self.is_converting:
            self.root.after(0, self.complete_conversion)
    
    def complete_conversion(self):
        self.storage_info.config(text="67108864 KB 可用，共 67108864 KB")
        self.progress_bar["value"] = 100
        self.progress_label.config(text="扩容完成！")
        self.is_converting = False
        self.convert_button.configure(state='normal')
        # 显示完成提示
        messagebox.showinfo("完成", "扩容已完成！")
        # 重置进度
        self.progress_bar["value"] = 0
        self.progress_label.config(text="准备就绪")

if __name__ == "__main__":
    root = tk.Tk()
    app = StorageConverterApp(root)
    root.mainloop() 