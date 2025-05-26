import tkinter as tk
from tkinter import ttk, messagebox
import base64
import os

class AbaCipher:
    @staticmethod
    def encrypt(text):
        """将文本加密为阿巴序列"""
        # 将文本转换为base64编码
        text_bytes = text.encode('utf-8')
        base64_bytes = base64.b64encode(text_bytes)
        
        # 将每个字节的比特转换为阿巴序列
        result = ""
        for b in base64_bytes:
            # 每字节8位，拆分为8个阿巴字符
            for i in range(7, -1, -1):
                bit = (b >> i) & 1
                result += "阿" if bit == 0 else "巴"
        
        return result
    
    @staticmethod
    def decrypt(aba_text):
        """将阿巴序列解密为原始文本"""
        try:
            # 检查输入是否仅包含阿巴字符
            if not all(c in "阿巴" for c in aba_text):
                raise ValueError("输入文本包含非阿巴字符")
            
            # 将阿巴字符转换回二进制
            binary = ""
            for c in aba_text:
                binary += "0" if c == "阿" else "1"
            
            # 确保二进制长度是8的倍数
            if len(binary) % 8 != 0:
                # 移除末尾多余的位
                binary = binary[:-(len(binary) % 8)]
            
            # 将二进制转换为字节
            bytes_array = bytearray()
            for i in range(0, len(binary), 8):
                byte_str = binary[i:i+8]
                byte = int(byte_str, 2)
                bytes_array.append(byte)
            
            # Base64解码并转换为文本
            try:
                decoded_bytes = base64.b64decode(bytes_array)
                return decoded_bytes.decode('utf-8')
            except Exception as e:
                raise ValueError(f"Base64解码失败: {str(e)}")
            
        except Exception as e:
            messagebox.showerror("解密错误", f"无法解密：{str(e)}")
            return "解密失败，请确保输入正确的阿巴加密文本"

class RoundedButton(tk.Canvas):
    """自定义圆角按钮类 - 修复文字问题"""
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

class TextWithPlaceholder(tk.Text):
    """带占位符的文本框类"""
    def __init__(self, master=None, placeholder="请输入文本...", placeholder_color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.default_fg_color = self['fg']
        self.placeholder_showing = True

        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)
        self.bind("<Key>", self._on_key)

        self._show_placeholder()

    def _show_placeholder(self):
        """显示占位符"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self.placeholder)
        self.config(fg=self.placeholder_color)
        self.placeholder_showing = True

    def _remove_placeholder(self):
        """移除占位符"""
        if self.placeholder_showing:
            self.delete('1.0', tk.END)
            self.config(fg=self.default_fg_color)
            self.placeholder_showing = False

    def _focus_in(self, event):
        """获得焦点时，如果显示的是占位符则清除"""
        if self.placeholder_showing:
            self._remove_placeholder()

    def _focus_out(self, event):
        """失去焦点时，如果为空则显示占位符"""
        if not self.get('1.0', tk.END).strip():
            self._show_placeholder()

    def _on_key(self, event):
        """按键时，如果显示的是占位符则清除"""
        if self.placeholder_showing and event.char:
            self._remove_placeholder()

    def get_text(self):
        """获取文本内容（不包括占位符）"""
        if self.placeholder_showing:
            return ""
        return self.get('1.0', tk.END).strip()

    def set_text(self, text):
        """设置文本内容"""
        self._remove_placeholder()
        self.delete('1.0', tk.END)
        if text:
            self.insert('1.0', text)
        else:
            self._focus_out(None)

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
        self.canvas.lower()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("阿巴加密器 - by: 南风梦西洲")
        self.geometry("650x550")
        self.configure(bg="#F5F5F5")
        # 允许窗口自由拉伸
        self.minsize(500, 450)
        
        # 用于跟踪状态消息的计时器ID
        self.status_timer_id = None
        
        # 设置应用图标
        try:
            if os.path.exists("logo.ico"):
                self.iconbitmap("logo.ico")
        except Exception:
            pass  # 如果图标不存在或无法加载，使用默认图标
        
        # 创建主框架
        main_frame = tk.Frame(self, bg="#F5F5F5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置行列权重，使布局可以随窗口调整
        main_frame.columnconfigure(0, weight=1)
        for i in range(7):
            main_frame.rowconfigure(i, weight=0)
        main_frame.rowconfigure(1, weight=1)  # 输入框区域可拉伸
        main_frame.rowconfigure(3, weight=1)  # 输出框区域可拉伸
        
        # 应用标题
        title_frame = tk.Frame(main_frame, bg="#F5F5F5")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        title_label = tk.Label(title_frame, text="阿巴加密器", 
                              font=("微软雅黑", 18, "bold"), bg="#F5F5F5", fg="#333333")
        title_label.pack(pady=5)
        
        # 创建输入区域
        input_frame = RoundedFrame(main_frame, bg="#FFFFFF", radius=15, padding="15")
        input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        
        input_label = tk.Label(input_frame.container, text="输入文本", font=("微软雅黑", 12), 
                              bg="#FFFFFF", fg="#333333")
        input_label.pack(anchor="w", pady=(0, 10))
        
        # 使用带占位符的文本框替换原来的文本框
        self.input_text = TextWithPlaceholder(
            input_frame.container, 
            placeholder="请在此输入要加密或解密的文本...",
            placeholder_color="#AAAAAA",
            height=5, 
            width=50, 
            font=("微软雅黑", 11),
            bg="#FFFFFF", 
            fg="#333333", 
            relief="flat", 
            padx=5, 
            pady=5,
            wrap="word"
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加自定义滚动条
        input_scrollbar = ttk.Scrollbar(input_frame.container, command=self.input_text.yview)
        input_scrollbar.pack(side="right", fill="y")
        self.input_text.config(yscrollcommand=input_scrollbar.set)
        
        # 创建按钮区域
        button_frame = tk.Frame(main_frame, bg="#F5F5F5")
        button_frame.grid(row=2, column=0, sticky="ew", pady=15)
        
        # 配置按钮框架列权重
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # 创建圆角按钮，确保文字使用白色
        self.encrypt_button = RoundedButton(button_frame, text="加密", command=self.encrypt,
                                          width=150, height=40, fg="white")
        self.encrypt_button.grid(row=0, column=0, padx=10)
        
        self.decrypt_button = RoundedButton(button_frame, text="解密", command=self.decrypt,
                                          width=150, height=40, fg="white")
        self.decrypt_button.grid(row=0, column=1, padx=10)
        
        self.clear_button = RoundedButton(button_frame, text="清空", command=self.clear_all,
                                        width=150, height=40, fg="white")
        self.clear_button.grid(row=0, column=2, padx=10)
        
        # 创建输出区域
        output_frame = RoundedFrame(main_frame, bg="#FFFFFF", radius=15, padding="15")
        output_frame.grid(row=3, column=0, sticky="nsew", pady=15)
        
        output_label = tk.Label(output_frame.container, text="输出结果", font=("微软雅黑", 12),
                               bg="#FFFFFF", fg="#333333")
        output_label.pack(anchor="w", pady=(0, 10))
        
        # 同样使用带占位符的文本框
        self.output_text = TextWithPlaceholder(
            output_frame.container, 
            placeholder="加密或解密结果将显示在这里...",
            placeholder_color="#AAAAAA",
            height=5, 
            width=50, 
            font=("微软雅黑", 11),
            bg="#FFFFFF", 
            fg="#333333", 
            relief="flat", 
            padx=5, 
            pady=5,
            wrap="word"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加自定义滚动条
        output_scrollbar = ttk.Scrollbar(output_frame.container, command=self.output_text.yview)
        output_scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=output_scrollbar.set)
        
        # 创建复制按钮
        copy_frame = tk.Frame(main_frame, bg="#F5F5F5")
        copy_frame.grid(row=4, column=0, sticky="ew", pady=10)
        
        self.copy_button = RoundedButton(copy_frame, text="复制结果", command=self.copy_output,
                                       width=200, height=40, fg="white")
        self.copy_button.pack()
        
        # 创建状态标签
        status_frame = tk.Frame(main_frame, bg="#F5F5F5")
        status_frame.grid(row=5, column=0, sticky="ew", pady=5)
        
        self.status_label = tk.Label(status_frame, text="", font=("微软雅黑", 10),
                                   bg="#F5F5F5", fg="#666666")
        self.status_label.pack()
        
        # 创建版权信息
        footer_frame = tk.Frame(main_frame, bg="#F5F5F5")
        footer_frame.grid(row=6, column=0, sticky="ew", pady=(5, 0))
        
        footer_label = tk.Label(footer_frame, text="阿巴加密技术 · 安全保障", font=("微软雅黑", 9),
                               bg="#F5F5F5", fg="#999999")
        footer_label.pack()
    
    def encrypt(self):
        # 使用get_text方法获取文本（不含占位符）
        input_text = self.input_text.get_text()
        if input_text:
            encrypted = AbaCipher.encrypt(input_text)
            # 使用set_text方法设置文本
            self.output_text.set_text(encrypted)
            self.show_status("加密成功！")
        else:
            self.show_status("请输入要加密的文本！")
    
    def decrypt(self):
        # 使用get_text方法获取文本（不含占位符）
        input_text = self.input_text.get_text()
        if input_text:
            decrypted = AbaCipher.decrypt(input_text)
            # 使用set_text方法设置文本
            self.output_text.set_text(decrypted)
            self.show_status("解密成功！")
        else:
            self.show_status("请输入要解密的文本！")
    
    def copy_output(self):
        # 使用get_text方法获取文本（不含占位符）
        output_text = self.output_text.get_text()
        if output_text:
            self.clipboard_clear()
            self.clipboard_append(output_text)
            self.show_status("已复制到剪贴板！")
        else:
            self.show_status("没有可复制的内容！")
    
    def clear_all(self):
        # 清空两个文本框
        self.input_text.set_text("")
        self.output_text.set_text("")
        self.show_status("已清空所有内容")
    
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