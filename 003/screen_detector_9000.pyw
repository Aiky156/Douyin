import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import math
import random
import time
import os
import ctypes

class ScreenDetector9000:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("屏幕状态超级量子计算机人工智能检测器 - by: 南风梦西洲")
        
        # 设置全屏
        self.root.attributes('-fullscreen', True)
        # 添加 Esc 键退出全屏的功能
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        self.root.configure(bg='#1a1a2e')
        
        # 设置窗口图标
        icon_path = r"C:\Users\Aikey\Desktop\fa\003\logo.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # 加载字体
        font_path = r"C:\Users\Aikey\Desktop\fa\003\kz.ttf"
        if os.path.exists(font_path):
            try:
                ctypes.windll.gdi32.AddFontResourceW(font_path)
                self.title_font = ('站酷高端黑', 24)
                self.text_font = ('站酷高端黑', 16)
                self.final_font = ('站酷高端黑', 32)  # 添加最终结论使用的大号字体
            except:
                self.title_font = ('Microsoft YaHei', 24)
                self.text_font = ('Microsoft YaHei', 16)
                self.final_font = ('Microsoft YaHei', 32)
        else:
            self.title_font = ('Microsoft YaHei', 24)
            self.text_font = ('Microsoft YaHei', 16)
            self.final_font = ('Microsoft YaHei', 32)
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题标签
        self.title_label = tk.Label(
            self.main_frame,
            text="屏幕状态超级量子计算机人工智能检测器",
            font=self.title_font,
            fg='#2196F3',
            bg='#1a1a2e'
        )
        self.title_label.pack(pady=10)
        
        # 加载并显示标志
        logo_path = r"C:\Users\Aikey\Desktop\fa\003\550w.png"
        if os.path.exists(logo_path):
            # 加载图片
            original_image = Image.open(logo_path)
            # 调整图片大小
            logo_size = (180, 180)
            resized_image = original_image.resize(logo_size, Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(resized_image)
            
            # 创建标志标签
            self.logo_label = tk.Label(
                self.main_frame,
                image=self.logo_image,
                bg='#1a1a2e'
            )
            self.logo_label.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(
            self.main_frame,
            text="初始化量子检测引擎...",
            font=self.text_font,
            fg='#2196F3',
            bg='#1a1a2e'
        )
        self.status_label.pack(pady=20)
        
        # 创建画布
        self.canvas = tk.Canvas(
            self.main_frame,
            width=700,
            height=400,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # 进度条
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#1a1a2e',
            background='#2196F3',
            thickness=10
        )
        
        self.progress = ttk.Progressbar(
            self.main_frame,
            style="Custom.Horizontal.TProgressbar",
            length=700,
            mode='determinate'
        )
        self.progress.pack(pady=20)
        
        # 动画状态
        self.current_step = 0
        self.particles = []
        self.animation_frame = 0
        
        # 检测步骤
        self.steps = [
            ("正在扫描显示器电子流动状态...", 3000),
            ("分析像素点能量激活情况...", 4000),
            ("检测到屏幕发光粒子活跃度...", 3000),
            ("计算显示器光量子纠缠态...", 3500),
            ("启动薛定谔的显示器悖论检验...", 3000),
            ("最终结论：屏幕是亮着的！", 2000)
        ]
        
        # 开始检测过程
        self.start_detection()
        
    def start_detection(self):
        self.next_step()
        self.update_animation()
        
    def next_step(self):
        if self.current_step < len(self.steps):
            step_text, duration = self.steps[self.current_step]
            # 如果是最后一步，使用大号字体
            if self.current_step == len(self.steps) - 1:
                self.status_label.config(text=step_text, font=self.final_font)
            else:
                self.status_label.config(text=step_text, font=self.text_font)
            self.progress['value'] = (self.current_step + 1) * (100 / len(self.steps))
            self.root.after(duration, self.next_step)
            self.current_step += 1
            
    def update_animation(self):
        self.canvas.delete('all')
        self.animation_frame += 1
        
        if self.current_step == 0:
            self.draw_electron_flow()
        elif self.current_step == 1:
            self.draw_pixel_energy()
        elif self.current_step == 2:
            self.draw_photon_activity()
        elif self.current_step == 3:
            self.draw_quantum_state()
        elif self.current_step == 4:  # 薛定谔的显示器悖论检验
            self.draw_schrodinger_paradox()
        elif self.current_step == 5:  # 最终结论
            self.draw_final_result()
            
        self.root.after(50, self.update_animation)
        
    def draw_electron_flow(self):
        # 电子流动效果
        for i in range(10):
            x = (self.animation_frame * 5 + i * 70) % 700
            y = 200 + math.sin(x * 0.05) * 50
            
            # 电子
            self.canvas.create_oval(
                x-10, y-10, x+10, y+10,
                fill='#4CAF50',
                outline='#2196F3',
                width=2
            )
            # 轨迹
            self.canvas.create_line(
                x-20, y, x+20, y,
                fill='#2196F3',
                width=1,
                dash=(3,2)
            )
        
    def draw_pixel_energy(self):
        cell_size = 30
        for row in range(0, 400, cell_size):
            for col in range(0, 700, cell_size):
                energy = math.sin(row * 0.1 + col * 0.1 + self.animation_frame * 0.1)
                color = f'#{int(abs(energy) * 127 + 128):02x}ff00'
                
                self.canvas.create_rectangle(
                    col, row,
                    col + cell_size - 2,
                    row + cell_size - 2,
                    fill=color,
                    outline=''
                )
        
    def draw_photon_activity(self):
        if len(self.particles) < 100:
            self.particles.append({
                'x': random.randint(0, 700),
                'y': random.randint(0, 400),
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'size': random.uniform(2, 4),
                'intensity': random.random()
            })
            
        for particle in self.particles:
            x, y = particle['x'], particle['y']
            size = particle['size']
            intensity = particle['intensity']
            
            # 光子效果
            color = f'#{int(intensity * 255):02x}ff{int(intensity * 255):02x}'
            self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline='white'
            )
            
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            if particle['x'] < 0 or particle['x'] > 700:
                particle['dx'] *= -1
            if particle['y'] < 0 or particle['y'] > 400:
                particle['dy'] *= -1
                
    def draw_quantum_state(self):
        # 量子态叠加效果
        center_x = 350
        center_y = 200
        max_radius = 150
        
        # 在顶部显示概率文本
        probability = abs(math.sin(self.animation_frame * 0.05))
        self.canvas.create_text(
            center_x,
            30,  # 固定在顶部
            text=f"粒子活跃度: {probability:.2%}",
            font=self.text_font,
            fill='#2196F3'
        )
        
        for i in range(10):
            radius = max_radius - i * 15
            phase = self.animation_frame * 0.1 + i * 0.5
            
            x = center_x + math.cos(phase) * radius
            y = center_y + math.sin(phase) * radius
            
            self.canvas.create_oval(
                x-5, y-5, x+5, y+5,
                fill='#2196F3',
                outline='#4CAF50',
                width=2
            )
            
            # 量子轨道
            self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline='#2196F3',
                width=1,
                dash=(5,5)
            )
        
    def draw_schrodinger_paradox(self):
        # 画布中心点
        center_x = 350
        center_y = 200
        
        # 在顶部显示概率文本
        probability = abs(math.sin(self.animation_frame * 0.05))
        self.canvas.create_text(
            center_x,
            30,  # 固定在顶部
            text=f"量子叠加概率: {probability:.2%}",
            font=self.text_font,
            fill='#2196F3'
        )
        
        # 绘制两个交错的圆形，代表叠加态
        radius = 100 + math.sin(self.animation_frame * 0.1) * 20
        
        # 第一个状态："开"
        alpha = abs(math.sin(self.animation_frame * 0.05))
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline='#4CAF50',
            width=2,
            dash=(5, 5)
        )
        self.canvas.create_text(
            center_x,
            center_y - 10,
            text="开",
            font=self.text_font,
            fill='#4CAF50'
        )
        
        # 第二个状态："关"
        beta = abs(math.cos(self.animation_frame * 0.05))
        offset = 30 * math.sin(self.animation_frame * 0.1) * 2
        self.canvas.create_oval(
            center_x - radius + offset,
            center_y - radius - offset,
            center_x + radius + offset,
            center_y + radius - offset,
            outline='#FF5252',
            width=2,
            dash=(5, 5)
        )
        self.canvas.create_text(
            center_x + offset,
            center_y - 10 - offset,
            text="关",
            font=self.text_font,
            fill='#FF5252'
        )
        
        # 添加量子跳跃粒子效果
        num_particles = 16  # 增加粒子数量
        for i in range(num_particles):
            base_angle = self.animation_frame * 0.1 + i * (2 * math.pi / num_particles)
            
            # 添加随机跳动效果
            jump = math.sin(self.animation_frame * 0.3 + i * 0.5) * 15
            random_offset = random.uniform(-5, 5)
            
            # 计算粒子位置
            particle_radius = radius + jump + random_offset
            wave_x = center_x + math.cos(base_angle) * particle_radius
            wave_y = center_y + math.sin(base_angle) * particle_radius
            
            # 粒子大小随时间变化
            size = 4 + math.sin(self.animation_frame * 0.2 + i) * 2
            
            # 粒子颜色在绿色和红色之间渐变
            color_mix = abs(math.sin(base_angle + self.animation_frame * 0.05))
            r = int(255 * (1 - color_mix))  # 红色分量
            g = int(255 * color_mix)        # 绿色分量
            color = f'#{r:02x}{g:02x}ff'
            
            # 绘制主粒子
            self.canvas.create_oval(
                wave_x - size,
                wave_y - size,
                wave_x + size,
                wave_y + size,
                fill=color,
                outline='#ffffff',
                width=1
            )
            
            # 添加粒子轨迹效果
            trail_length = 3
            for t in range(trail_length):
                trail_angle = base_angle - t * 0.2
                trail_x = center_x + math.cos(trail_angle) * particle_radius
                trail_y = center_y + math.sin(trail_angle) * particle_radius
                trail_size = size * (1 - t/trail_length)
                
                self.canvas.create_oval(
                    trail_x - trail_size,
                    trail_y - trail_size,
                    trail_x + trail_size,
                    trail_y + trail_size,
                    fill=color,
                    outline='',
                    stipple='gray50'  # 使轨迹半透明
                )
        
        # 添加概率波函数
        points = []
        for x in range(-50, 51):
            wave = math.sin(x * 0.2 + self.animation_frame * 0.1) * 20
            points.extend([center_x + x * 3, center_y + radius + 50 + wave])
        
        self.canvas.create_line(
            points,
            fill='#2196F3',
            width=2,
            smooth=True
        )
        
    def draw_final_result(self):
        # 显示最终结论时的动画效果
        center_x = 350
        center_y = 200
        
        # 绘制一个明亮的圆形光晕
        radius = 100 + math.sin(self.animation_frame * 0.1) * 10
        glow_radius = radius + 20
        
        # 外部光晕
        self.canvas.create_oval(
            center_x - glow_radius,
            center_y - glow_radius,
            center_x + glow_radius,
            center_y + glow_radius,
            fill='#1a1a2e',
            outline='#4CAF50',
            width=2
        )
        
        # 内部光圈
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill='#1a1a2e',
            outline='#2196F3',
            width=3
        )
        
        # 添加一些装饰性的光点
        for i in range(8):
            angle = self.animation_frame * 0.1 + i * math.pi / 4
            x = center_x + math.cos(angle) * (radius + 10)
            y = center_y + math.sin(angle) * (radius + 10)
            
            size = 5 + math.sin(self.animation_frame * 0.2 + i) * 2
            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill='#4CAF50',
                outline=''
            )
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ScreenDetector9000()
    app.run() 