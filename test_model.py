import os
import sys
from utils.weather import get_weather_with_retry
from utils.horoscope import get_horoscope_with_retry
from utils.quotes import get_daily_quote


def test_modules():
    print("=== 测试模块功能 ===")

    # 测试天气功能
    print("\n测试天气功能:")
    try:
        weather = get_weather_with_retry("哈尔滨")
        print(f"天气信息: {weather}")
    except Exception as e:
        print(f"天气功能测试失败: {str(e)}")

        # 测试星座运势
    print("\n测试星座运势:")
    try:
        horoscope = get_horoscope_with_retry("射手座")
        print(f"星座运势: {horoscope}")
    except Exception as e:
        print(f"星座运势测试失败: {str(e)}")

        # 测试每日一句
    print("\n测试每日一句:")
    try:
        quote = get_daily_quote()
        print(f"每日一句: {quote}")
    except Exception as e:
        print(f"每日一句测试失败: {str(e)}")

        # 测试资源文件
    print("\n测试资源文件:")
    required_paths = [
        "assets/fonts/SimHei.ttf",
        "assets/images/morning",
        "assets/images/night"
    ]

    for path in required_paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                files = os.listdir(path)
                print(f"{path} 存在，包含文件: {files}")
            else:
                print(f"{path} 存在")
        else:
            print(f"警告: {path} 不存在!")


if __name__ == "__main__":
    test_modules()