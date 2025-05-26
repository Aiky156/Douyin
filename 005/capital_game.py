import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import threading

class RoundedButton(tk.Canvas):
    """自定义圆角按钮类"""
    def __init__(self, parent, text, command=None, radius=15, bg="#FF6B6B", fg="white", 
                 hoverbg="#FF8A8A", width=120, height=35, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], 
                         highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.hoverbg = hoverbg
        self.command = command
        self.text = text
        self.width = width
        self.height = height

        # 绘制初始状态（背景）
        self._draw_rounded_rect(self.bg)
        # 绘制文字（确保始终在最上层）
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill="white", 
                                      font=("微软雅黑", 10, "bold"), tags=("text",))

        # 绑定事件
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw_rounded_rect(self, color):
        """只重绘矩形，保留文字"""
        self.delete("rect")  # 只删除矩形，不删除文字
        self.create_oval(0, 0, self.radius * 2, self.radius * 2, fill=color, outline=color, tags="rect")
        self.create_oval(self.width - self.radius * 2, 0, self.width, self.radius * 2, 
                        fill=color, outline=color, tags="rect")
        self.create_oval(0, self.height - self.radius * 2, self.radius * 2, self.height, 
                        fill=color, outline=color, tags="rect")
        self.create_oval(self.width - self.radius * 2, self.height - self.radius * 2, 
                        self.width, self.height, fill=color, outline=color, tags="rect")
        self.create_rectangle(self.radius, 0, self.width - self.radius, self.height, 
                             fill=color, outline=color, tags="rect")
        self.create_rectangle(0, self.radius, self.width, self.height - self.radius, 
                             fill=color, outline=color, tags="rect")
        # 确保文字在最上层
        self.tag_raise("text")

    def _on_enter(self, event):
        self._draw_rounded_rect(self.hoverbg)

    def _on_leave(self, event):
        self._draw_rounded_rect(self.bg)

    def _on_click(self, event):
        self._draw_rounded_rect("#E96060")

    def _on_release(self, event):
        self._draw_rounded_rect(self.hoverbg)
        if self.command:
            self.command()

class RoundedFrame(tk.Frame):
    """自定义圆角边框容器"""
    def __init__(self, parent, bg="#FFFFFF", radius=15, **kwargs):
        padding = kwargs.pop("padding", 0)
        if isinstance(padding, str):
            padding = tuple(map(int, padding.split()))
        if len(padding) == 1:
            padding = padding * 4
        kwargs["bg"] = parent["bg"]
        kwargs["highlightthickness"] = 0
        super().__init__(parent, **kwargs)
        
        self.padding = padding
        self.radius = radius
        self.bg = bg
        
        # 创建圆角背景
        self.canvas = tk.Canvas(self, bg=parent["bg"], highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 内部容器
        self.container = tk.Frame(self, bg=bg, highlightthickness=0)
        self.container.place(x=padding[0], y=padding[1], 
                            width=self.winfo_width()-padding[0]-padding[2],
                            height=self.winfo_height()-padding[1]-padding[3])
        
        self.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        width, height = event.width, event.height
        
        # 更新内部容器大小
        self.container.place(x=self.padding[0], y=self.padding[1], 
                            width=width-self.padding[0]-self.padding[2],
                            height=height-self.padding[1]-self.padding[3])
        
        # 重绘圆角背景
        self.canvas.delete("all")
        self.canvas.create_oval(0, 0, self.radius*2, self.radius*2, 
                                fill=self.bg, outline=self.bg)
        self.canvas.create_oval(width-self.radius*2, 0, width, self.radius*2, 
                                fill=self.bg, outline=self.bg)
        self.canvas.create_oval(0, height-self.radius*2, self.radius*2, height, 
                                fill=self.bg, outline=self.bg)
        self.canvas.create_oval(width-self.radius*2, height-self.radius*2, width, height, 
                                fill=self.bg, outline=self.bg)
        self.canvas.create_rectangle(self.radius, 0, width-self.radius, height, 
                                    fill=self.bg, outline=self.bg)
        self.canvas.create_rectangle(0, self.radius, width, height-self.radius, 
                                    fill=self.bg, outline=self.bg)
        # 将画布放到底层
        # 不使用参数，直接调用tkinter的lower方法
        self.canvas.lower()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("资本做局机 - by: 南风梦西洲")
        self.geometry("700x600")
        self.configure(bg="#F5F5F5")
        # 允许窗口自由拉伸
        self.minsize(600, 500)
        
        # 用于跟踪状态消息的计时器ID
        self.status_timer_id = None
        self.process_running = False
        
        # 设置应用图标
        try:
            # 使用绝对路径加载logo.ico
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print(f"图标已加载: {icon_path}")
            else:
                print(f"图标文件不存在: {icon_path}")
        except Exception as e:
            print(f"无法加载图标: {e}")
        
        # 创建主框架
        main_frame = tk.Frame(self, bg="#F5F5F5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置行列权重，使布局可以随窗口调整
        main_frame.columnconfigure(0, weight=1)
        for i in range(5):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(2, weight=1)  # 进度条区域可拉伸
        
        # 应用标题 - 垂直排列元素
        # 1. 标题
        title_frame = tk.Frame(main_frame, bg="#F5F5F5")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="资本做局机", 
                               font=("微软雅黑", 18, "bold"), bg="#F5F5F5", fg="#333333")
        title_label.pack(pady=5)
        
        # 2. 图片
        image_frame = tk.Frame(main_frame, bg="#F5F5F5")
        image_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # 创建图片区域框，固定大小为400*400像素
        image_frame_fixed = tk.Frame(image_frame, width=400, height=400, bg="#F5F5F5", highlightbackground="#CCCCCC", highlightthickness=1)
        image_frame_fixed.pack(pady=10)
        # 确保框架不会因为内容而改变大小
        image_frame_fixed.pack_propagate(False)
        
        # 创建一个画布作为容器，用于显示图片或文字
        canvas = tk.Canvas(image_frame_fixed, width=400, height=400, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # 默认显示文本提示
        text_id = canvas.create_text(200, 200, text="[图片区域 - 400x400]", font=("微软雅黑", 14), fill="#666666")
        
        # 尝试加载图片
        try:
            # 使用绝对路径加载a.png
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a.png")
            print(f"尝试加载图片: {image_path}")
            
            if os.path.exists(image_path):
                # 加载图片
                self.title_image = tk.PhotoImage(file=image_path)
                
                # 获取原始图片大小
                img_width = self.title_image.width()
                img_height = self.title_image.height()
                
                # 清除画布上的文本
                canvas.delete("all")
                
                # 尝试缩放图片以适应400x400的空间
                # 使用subsample方法缩小图片
                subsample_factor = 1  # 默认不缩放
                
                if img_width > 400 or img_height > 400:
                    # 计算需要缩小的倍数
                    width_factor = (img_width // 400) + 1 if img_width > 400 else 1
                    height_factor = (img_height // 400) + 1 if img_height > 400 else 1
                    subsample_factor = max(width_factor, height_factor)
                    
                    # 缩小图片
                    try:
                        # 注意：subsample必须是整数
                        self.title_image = self.title_image.subsample(subsample_factor, subsample_factor)
                        # 重新获取缩小后的尺寸
                        img_width = self.title_image.width()
                        img_height = self.title_image.height()
                        print(f"图片已缩小 {subsample_factor} 倍，新尺寸: {img_width}x{img_height}")
                    except Exception as e:
                        print(f"缩小图片失败: {e}")
                
                # 将缩小后的图片居中显示
                x_pos = (400 - img_width) // 2
                y_pos = (400 - img_height) // 2
                
                # 将图片放在画布上（居中）
                canvas.create_image(200, 200, anchor="center", image=self.title_image)
                print(f"图片成功加载，原始尺寸: {img_width}x{img_height}")
                
                # 添加400x400的参考线
                canvas.create_line(0, 0, 400, 0, fill="#CCCCCC")
                canvas.create_line(0, 400, 400, 400, fill="#CCCCCC")
                canvas.create_line(0, 0, 0, 400, fill="#CCCCCC")
                canvas.create_line(400, 0, 400, 400, fill="#CCCCCC")
            else:
                print(f"图片文件不存在: {image_path}")
                # 保留文本标签
        except Exception as e:
            print(f"无法加载标题图片: {e}")
        
        # 3. 进度条区域
        progress_frame = RoundedFrame(main_frame, bg="#FFFFFF", radius=15, padding="15")
        progress_frame.grid(row=2, column=0, sticky="nsew", pady=15)
        
        # 4. 创建按钮区域
        button_frame = tk.Frame(main_frame, bg="#F5F5F5")
        button_frame.grid(row=3, column=0, sticky="ew", pady=15)
        
        # 创建圆角按钮
        self.start_button = RoundedButton(button_frame, text="开始做局", command=self.start_process,
                                        width=200, height=50, fg="white")
        self.start_button.pack()
        
        progress_label = tk.Label(progress_frame.container, text="资本运作进度", font=("微软雅黑", 12),
                                bg="#FFFFFF", fg="#333333")
        progress_label.pack(anchor="w", pady=(0, 10))
        
        # 创建更粗的进度条
        self.progress_var = tk.DoubleVar()
        
        # 配置进度条样式
        style = ttk.Style()
        style.configure("Thick.Horizontal.TProgressbar", thickness=25)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame.container, 
            orient="horizontal", 
            length=400, 
            mode="determinate",
            style="Thick.Horizontal.TProgressbar",
            variable=self.progress_var
        )
        self.progress_bar.pack(fill=tk.X, expand=True, pady=10)
        
        # 创建状态标签
        self.status_label = tk.Label(progress_frame.container, text="准备就绪", font=("微软雅黑", 10),
                                   bg="#FFFFFF", fg="#666666")
        self.status_label.pack(pady=10)
        
        # 移除了页脚部分
    
    def start_process(self):
        """开始做局进程"""
        if self.process_running:
            return
            
        self.process_running = True
        self.start_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_label.config(text="资本正在运作中...")
        
        # 创建线程执行进度条更新
        threading.Thread(target=self.update_progress, daemon=True).start()
    
    def update_progress(self):
        """更新进度条"""
        for i in range(101):
            if not self.process_running:
                break
                
            # 更新进度条值
            self.progress_var.set(i)
            
            # 更新状态文本
            if i < 30:
                status = "正在收集用户数据..."
            elif i < 60:
                status = "正在计算最优剥削方案..."
            elif i < 90:
                status = "正在部署资本陷阱..."
            else:
                status = "即将完成..."
                
            # 使用主线程更新UI
            self.after(0, lambda s=status: self.status_label.config(text=s))
            
            # 延时，确保整个过程需要5秒
            time.sleep(5/100)
            
        # 完成后显示结果
        self.after(0, self.show_result)
    
    def show_result(self):
        """显示做局结果"""
        self.process_running = False
        self.start_button.config(state=tk.NORMAL)
        self.status_label.config(text="做局完成！")
        
        # 显示消息框
        messagebox.showinfo("做局成功", "做局成功！您的时间被资本浪费了整整5秒！")
    
    def show_status(self, message, duration=3000):
        """显示状态消息，并在指定时间后自动清除"""
        # 如果已经有计时器在运行，取消它
        if self.status_timer_id:
            self.after_cancel(self.status_timer_id)
            self.status_timer_id = None
        
        # 设置新的状态消息
        self.status_label.config(text=message)
        
        # 设置计时器在指定时间后清除消息
        self.status_timer_id = self.after(duration, self.clear_status)
    
    def clear_status(self):
        """清除状态消息"""
        self.status_label.config(text="")
        self.status_timer_id = None

if __name__ == "__main__":
    app = Application()
    app.mainloop()
