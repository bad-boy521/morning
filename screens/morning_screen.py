from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from datetime import datetime
import random
import os
from utils.weather import get_weather_with_retry
from utils.horoscope import get_horoscope_with_retry
from utils.quotes import get_daily_quote


class MorningScreen(Screen):
    def __init__(self, **kwargs):
        super(MorningScreen, self).__init__(**kwargs)

        # 创建主布局为FloatLayout
        self.main_layout = FloatLayout()

        # 设置背景图片
        self.setup_background()

        # 创建内容布局
        self.content_layout = BoxLayout(
            orientation='vertical',
            padding=[30, 20],  # 增加左右padding
            spacing=15,  # 增加垂直间距
            size_hint=(0.9, 0.9),  # 控制内容区域宽度为90%
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # 居中显示
        )

        # 初始化各个组件
        self.setup_time_label()
        self.setup_greeting_label()
        self.setup_weather_label()
        self.setup_horoscope_label()
        self.setup_quote_label()

        # 将内容布局添加到主布局
        self.main_layout.add_widget(self.content_layout)

        # 将主布局添加到屏幕
        self.add_widget(self.main_layout)

        # 设置自动更新
        Clock.schedule_interval(self.update_content, 60)

    def setup_background(self):
        morning_images_path = 'assets/images/morning'
        background_images = [f for f in os.listdir(morning_images_path)
                             if f.endswith(('.jpg', '.png'))]
        if background_images:
            random_image = random.choice(background_images)
            background_path = os.path.join(morning_images_path, random_image)

            self.background = Image(
                source=background_path,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),  # 全屏显示
                pos_hint={'center_x': 0.5, 'center_y': 0.5}  # 居中显示
            )

            self.main_layout.add_widget(self.background)

    def setup_time_label(self):
        self.time_label = Label(
            text=datetime.now().strftime('%Y年%m月%d日 %H:%M'),
            font_name='SimHei',
            font_size='20sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=0.1,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='left'
        )
        self.content_layout.add_widget(self.time_label)

    def setup_greeting_label(self):
        self.greeting_label = Label(
            text="宝宝，早安啊，又是美妙的一天~",
            font_name='SimHei',
            font_size='24sp',  # 统一大标题字号
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=0.1,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            halign='left'
        )
        self.content_layout.add_widget(self.greeting_label)

    def setup_weather_label(self):
        self.weather_label = Label(
            text=self.get_weather_text(),
            font_name='SimHei',
            markup=True,  # 启用标记语言支持
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=0.25,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            text_size=(self.width * 0.85, None),  # 调整文本宽度
            halign='left',
            valign='middle'
        )
        self.content_layout.add_widget(self.weather_label)

    def setup_horoscope_label(self):
        self.horoscope_label = Label(
            text=self.get_horoscope_text(),
            font_name='SimHei',
            markup=True,  # 启用标记语言支持
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=0.35,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            text_size=(self.width * 0.85, None),  # 调整文本宽度
            halign='left',
            valign='middle'
        )
        self.content_layout.add_widget(self.horoscope_label)

    def setup_quote_label(self):
        self.quote_label = Label(
            text=self.get_quote_text(),
            font_name='SimHei',
            markup=True,  # 启用标记语言支持
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=0.2,
            outline_width=2,
            outline_color=(0, 0, 0, 1),
            text_size=(self.width * 0.85, None),  # 调整文本宽度
            halign='left',
            valign='middle'
        )
        self.content_layout.add_widget(self.quote_label)

    def get_weather_text(self):
        try:
            weather_info = get_weather_with_retry("哈尔滨")
            return f"[size=24sp]今日天气预报[/size]\n{weather_info}"  # 使用标记语言设置大标题
        except Exception as e:
            return "天气信息获取失败"

    def get_horoscope_text(self):
        try:
            horoscope_info = get_horoscope_with_retry("射手座")
            return f"[size=24sp]星座运势[/size]\n{horoscope_info}"  # 使用标记语言设置大标题
        except Exception as e:
            return "星座运势获取失败"

    def get_quote_text(self):
        try:
            quote = get_daily_quote()
            return f"[size=24sp]今日寄语[/size]\n{quote}"  # 使用标记语言设置大标题
        except Exception as e:
            return "每日寄语获取失败"

    def update_content(self, dt):
        self.time_label.text = datetime.now().strftime('%Y年%m月%d日 %H:%M')

        current_hour = datetime.now().hour
        if current_hour == 8:
            self.weather_label.text = self.get_weather_text()
            self.horoscope_label.text = self.get_horoscope_text()
            self.quote_label.text = self.get_quote_text()

    def on_enter(self):
        self.update_content(0)

    def on_size(self, *args):
        # 更新文本宽度
        width = self.width * 0.85
        self.weather_label.text_size = (width, None)
        self.horoscope_label.text_size = (width, None)
        self.quote_label.text_size = (width, None)