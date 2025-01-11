from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.morning_screen import MorningScreen
from screens.night_screen import NightScreen
import schedule
import time
from datetime import datetime
from threading import Thread
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)


class MorningReminderApp(App):
    def build(self):
        # 设置应用标题
        self.title = '每日提醒'

        # 创建带过渡动画的屏幕管理器
        self.screen_manager = ScreenManager(transition=FadeTransition())

        # 初始化屏幕
        self.morning_screen = MorningScreen(name='morning')
        self.night_screen = NightScreen(name='night')

        # 添加屏幕
        self.screen_manager.add_widget(self.morning_screen)
        self.screen_manager.add_widget(self.night_screen)

        # 根据当前时间设置初始屏幕
        self.set_initial_screen()

        # 设置定时任务
        self.setup_schedule()

        # 启动定时任务线程
        self.schedule_thread = Thread(target=self.run_schedule, daemon=True)
        self.schedule_thread.start()

        return self.screen_manager

    def set_initial_screen(self):
        """根据当前时间设置初始屏幕"""
        current_hour = datetime.now().hour
        if 6 <= current_hour < 21:  # 早上6点到晚上9点显示早安屏
            self.screen_manager.current = 'morning'
            logging.info("启动应用 - 显示早安屏")
        else:
            self.screen_manager.current = 'night'
            logging.info("启动应用 - 显示晚安屏")

    def setup_schedule(self):
        """设置定时任务"""
        try:
            # 早安屏时间设置
            schedule.every().day.at("06:00").do(self.show_morning_reminder)  # 早上6点
            schedule.every().day.at("08:00").do(self.update_morning_content)  # 早上8点更新内容

            # 晚安屏时间设置
            schedule.every().day.at("21:00").do(self.show_night_reminder)  # 晚上9点
            schedule.every().day.at("22:00").do(self.update_night_content)  # 晚上10点更新内容

            logging.info("定时任务设置成功")
        except Exception as e:
            logging.error(f"定时任务设置失败: {str(e)}")

    def run_schedule(self):
        """运行定时任务"""
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logging.error(f"定时任务执行错误: {str(e)}")
                time.sleep(60)  # 发生错误时等待1分钟后继续

    def show_morning_reminder(self):
        """显示早安屏"""
        Clock.schedule_once(lambda dt: self.switch_screen('morning'))
        logging.info("切换到早安屏")

    def show_night_reminder(self):
        """显示晚安屏"""
        Clock.schedule_once(lambda dt: self.switch_screen('night'))
        logging.info("切换到晚安屏")

    def update_morning_content(self):
        """更新早安屏内容"""
        Clock.schedule_once(lambda dt: self.morning_screen.update_content(0))
        logging.info("更新早安屏内容")

    def update_night_content(self):
        """更新晚安屏内容"""
        Clock.schedule_once(lambda dt: self.night_screen.update_content(0))
        logging.info("更新晚安屏内容")

    def switch_screen(self, screen_name):
        """切换屏幕"""
        if self.screen_manager.current != screen_name:
            self.screen_manager.current = screen_name

    def on_stop(self):
        """应用关闭时的清理工作"""
        logging.info("应用关闭")
        super().on_stop()


if __name__ == '__main__':
    try:
        # 设置窗口属性
        Window.size = (360, 800)  # 设置一个合适的窗口大小
        Window.clearcolor = (0, 0, 0, 1)  # 设置窗口背景色为黑色
        app = MorningReminderApp()
        app.run()
    except Exception as e:
        logging.critical(f"应用运行失败: {str(e)}")