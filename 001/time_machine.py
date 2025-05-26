import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
from tkinter.font import Font

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, padding, color, text='', command=None, **kwargs):
        tk.Canvas.__init__(self, parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.color = color
        self.hover_color = '#FF8787'

        # 创建圆角矩形
        self.rect = self.round_rectangle(padding, padding, width-padding, height-padding, 
                                       corner_radius, fill=color, outline="")
        
        # 创建文本
        font = Font(family="微软雅黑", size=14, weight="bold")
        self.text = self.create_text(width/2, height/2, text=text, fill='white', font=font)

        # 绑定事件
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
    def round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
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
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color)

    def on_click(self, event):
        if self.command:
            self.command()

class TimeMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("时光穿越机 - by: 南风梦西洲")
        self.root.geometry("800x600")
        
        # 设置窗口图标
        try:
            self.root.iconbitmap(r"C:\Users\Aikey\Desktop\fa\logo.ico")
        except Exception as e:
            print(f"图标加载失败: {e}")
        
        # 设置背景
        self.canvas = tk.Canvas(root, width=800, height=600, bg='#f5f5f5')
        self.canvas.pack(fill="both", expand=True)
        
        # 创建主框架 - 使用圆角
        main_frame = tk.Frame(
            self.canvas, 
            bg='#ffffff',
            bd=0
        )
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # 标题标签
        title_label = tk.Label(
            main_frame,
            text="时光穿梭机",
            font=("微软雅黑", 36, "bold"),
            fg="#333333",
            bg='#ffffff',
            pady=30
        )
        title_label.pack()
        
        # 自定义下拉框样式
        style = ttk.Style()
        style.configure(
            "Rounded.TCombobox",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#333333",
            arrowcolor="#333333",
            borderwidth=0
        )
        
        # 创建圆角下拉框框架
        combo_frame = tk.Frame(main_frame, bg='#ffffff', padx=10, pady=5)
        combo_frame.pack(pady=20)
        
        self.time_options = [
            "1 小时",
            "2 小时",
            "3 秒钟",
            "10 年后",
            "100 年后"
        ]
        
        self.time_var = tk.StringVar()
        self.time_combobox = ttk.Combobox(
            combo_frame,
            textvariable=self.time_var,
            values=self.time_options,
            width=25,
            font=("微软雅黑", 14),
            style="Rounded.TCombobox",
            state="readonly"
        )
        self.time_combobox.set("请选择时间")
        self.time_combobox.pack(pady=10)
        
        # 使用自定义圆角按钮
        self.start_button = RoundedButton(
            main_frame,
            width=200,
            height=45,  
            corner_radius=22,
            padding=2,
            color='#FF6B6B',
            text='开始穿越',
            command=self.start_time_travel,
            bg='#ffffff'
        )
        self.start_button.pack(pady=30)
        
        # 修改进度条样式
        style.configure(
            "Rounded.Horizontal.TProgressbar",
            troughcolor='#E0E0E0',
            background='#FF6B6B',
            thickness=12,
            borderwidth=0,
            borderradius=10
        )
        
        self.progress = ttk.Progressbar(
            main_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="Rounded.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=30)

    def start_time_travel(self):
        if self.time_var.get() == "3 秒钟":
            self.start_button.configure(state="disabled")
            self.time_combobox.configure(state="disabled")
            
            self.progress["value"] = 0
            
            for i in range(100):
                self.progress["value"] = i + 1
                self.root.update()
                time.sleep(0.03)
                
            messagebox.showinfo("✨ 提示", "时空穿越成功！")
            
            self.start_button.configure(state="normal")
            self.time_combobox.configure(state="readonly")
        else:
            messagebox.showinfo("⚠️ 提示", "该功能暂未开放，请选择'3 秒钟'选项")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeMachine(root)
    root.mainloop() 