import requests
import json
from datetime import datetime, timedelta
import time
import os


class WeatherCache:
    def __init__(self):
        self.cache = {}
        self.last_update = {}

    def get(self, city):
        now = datetime.now()
        if city in self.cache:
            last_update = self.last_update[city]
            # 缓存1小时有效
            if now - last_update < timedelta(hours=1):
                return self.cache[city]
        return None

    def set(self, city, weather_data):
        self.cache[city] = weather_data
        self.last_update[city] = datetime.now()

    # 创建全局缓存实例


weather_cache = WeatherCache()


def get_weather(city):
    """
    获取指定城市的天气信息
    """
    try:
        # 使用你的和风天气API KEY
        API_KEY = "c7942bb6a1554dee8a09ad1c810c8a74"

        # 先检查缓存
        cached_weather = weather_cache.get(city)
        if cached_weather:
            return cached_weather

            # 获取城市ID
        location_url = "https://geoapi.qweather.com/v2/city/lookup"
        params = {
            'location': city,
            'key': API_KEY
        }

        response = requests.get(location_url, params=params, timeout=10)
        location_data = response.json()

        if location_data.get('code') == '200' and location_data.get('location'):
            city_id = location_data['location'][0]['id']

            # 获取天气信息
            weather_url = "https://devapi.qweather.com/v7/weather/now"
            params = {
                'location': city_id,
                'key': API_KEY
            }

            response = requests.get(weather_url, params=params, timeout=10)
            weather_data = response.json()

            if weather_data.get('code') == '200':
                now = weather_data['now']
                weather_text = (
                    f"{city}天气：{now['text']}，"
                    f"温度{now['temp']}℃，"
                    f"体感温度{now['feelsLike']}℃，"
                    f"湿度{now['humidity']}%，"
                    f"风向{now['windDir']}，"
                    f"风力{now['windScale']}级"
                )

                # 保存到缓存
                weather_cache.set(city, weather_text)
                return weather_text

        return get_backup_weather(city)

    except Exception as e:
        print(f"天气信息获取失败：{str(e)}")  # 打印错误信息以便调试
        return get_backup_weather(city)


def get_backup_weather(city):
    """当API无法访问时的备用天气数据"""
    now = datetime.now()
    backup_data = {
        "哈尔滨": {
            "spring": "晴朗，温度15℃，体感温度13℃，湿度45%，东北风2级",
            "summer": "多云，温度28℃，体感温度30℃，湿度60%，东南风3级",
            "autumn": "晴朗，温度18℃，体感温度16℃，湿度50%，西北风2级",
            "winter": "晴朗，温度-15℃，体感温度-18℃，湿度45%，北风3级"
        },
        "齐齐哈尔": {
            "spring": "多云，温度13℃，体感温度11℃，湿度50%，东风2级",
            "summer": "晴朗，温度26℃，体感温度28℃，湿度55%，东南风2级",
            "autumn": "多云，温度16℃，体感温度14℃，湿度55%，西风2级",
            "winter": "多云，温度-17℃，体感温度-20℃，湿度50%，东北风2级"
        }
    }

    # 根据月份判断季节
    month = now.month
    if month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    elif month in [9, 10, 11]:
        season = "autumn"
    else:
        season = "winter"

        # 如果城市不在备用数据中，返回哈尔滨的数据
    if city not in backup_data:
        city = "哈尔滨"

    return f"{city}天气：{backup_data[city][season]}"


def get_weather_with_retry(city, max_retries=3):
    """带重试机制的天气获取函数"""
    for attempt in range(max_retries):
        try:
            return get_weather(city)
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # 最后一次尝试
                print(f"获取天气信息失败，已重试{max_retries}次：{str(e)}")
                return get_backup_weather(city)
            time.sleep(1)  # 等待1秒后重试
    return get_backup_weather(city)


# 测试代码
if __name__ == "__main__":
    # 测试正常情况
    print("测试获取哈尔滨天气：")
    print(get_weather_with_retry("哈尔滨"))

    # 测试缓存
    print("\n测试缓存机制：")
    print(get_weather_with_retry("哈尔滨"))

    # 测试备用数据
    print("\n测试备用数据（使用不存在的城市）：")
    print(get_weather_with_retry("测试城市"))