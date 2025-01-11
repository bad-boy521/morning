# -*- coding: utf-8 -*-
import http.client
import urllib
import json
from datetime import datetime
import time


class HoroscopeCache:
    def __init__(self):
        self.cache = {}
        self.last_update = {}

    def get(self, constellation):
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        cache_key = f"{constellation}_{today}"

        if cache_key in self.cache:
            return self.cache[cache_key]
        return None

    def set(self, constellation, horoscope_data):
        today = datetime.now().strftime('%Y-%m-%d')
        cache_key = f"{constellation}_{today}"
        self.cache[cache_key] = horoscope_data
        self.last_update[cache_key] = datetime.now()

    # 创建全局缓存实例


horoscope_cache = HoroscopeCache()


def get_horoscope(constellation):
    """获取星座运势"""
    try:
        # 检查缓存
        cached_data = horoscope_cache.get(constellation)
        if cached_data:
            return cached_data

            # 星座名称转换字典
        constellation_map = {
            "白羊座": "aries",
            "金牛座": "taurus",
            "双子座": "gemini",
            "巨蟹座": "cancer",
            "狮子座": "leo",
            "处女座": "virgo",
            "天秤座": "libra",
            "天蝎座": "scorpio",
            "射手座": "sagittarius",
            "摩羯座": "capricorn",
            "水瓶座": "aquarius",
            "双鱼座": "pisces"
        }

        # 获取英文星座名
        en_constellation = constellation_map.get(constellation)
        if not en_constellation:
            return get_backup_horoscope(constellation)

            # 使用官方示例的请求方式
        conn = http.client.HTTPSConnection('apis.tianapi.com')
        params = urllib.parse.urlencode({
            'key': '04aaa47f72838b344d3b2bce788faadd',
            'astro': en_constellation
        })
        headers = {'Content-type': 'application/x-www-form-urlencoded'}

        conn.request('POST', '/star/index', params, headers)
        response = conn.getresponse()
        result = response.read()
        data = json.loads(result.decode('utf-8'))

        if data.get('code') == 200 and 'result' in data and 'list' in data['result']:
            fortune_list = data['result']['list']
            # 创建一个字典来存储运势信息
            fortune_dict = {item['type']: item['content'] for item in fortune_list}

            horoscope_text = (
                f"【{constellation}今日运势】\n"
                f"综合指数：{fortune_dict.get('综合指数', '暂无数据')}\n"
                f"爱情指数：{fortune_dict.get('爱情指数', '暂无数据')}\n"
                f"工作指数：{fortune_dict.get('工作指数', '暂无数据')}\n"
                f"财运指数：{fortune_dict.get('财运指数', '暂无数据')}\n"
                f"健康指数：{fortune_dict.get('健康指数', '暂无数据')}\n"
                f"幸运颜色：{fortune_dict.get('幸运颜色', '暂无数据')}\n"
                f"幸运数字：{fortune_dict.get('幸运数字', '暂无数据')}\n"
                f"贵人星座：{fortune_dict.get('贵人星座', '暂无数据')}\n"
                f"今日概述：{fortune_dict.get('今日概述', '暂无数据')}"
            )

            # 保存到缓存
            horoscope_cache.set(constellation, horoscope_text)
            return horoscope_text

        return get_backup_horoscope(constellation)

    except Exception as e:
        print(f"获取星座运势出错：{str(e)}")
        return get_backup_horoscope(constellation)
    finally:
        if 'conn' in locals():
            conn.close()


def get_backup_horoscope(constellation):
    """备用星座运势数据"""
    backup_data = {
        "白羊座": {
            "morning": "今日运势不错，精力充沛。建议把握上午时光，专注于重要工作。财运和事业运都不错，是谈判合作的好时机。感情方面可能有新的火花。",
            "afternoon": "下午适合与人社交，可能会有意外收获。工作上的付出将得到回报，但要注意控制情绪，避免冲动。",
            "evening": "晚间运势平稳，适合运动或放松。建议早点休息，注意身体健康。"
        },
        "射手座": {
            "morning": "早晨思维活跃，是规划和学习的好时机。财运方面可能有小的收获，适合投资理财。人际关系融洽，容易得到他人帮助。",
            "afternoon": "下午工作效率高，适合处理困难任务。感情方面可能有新的进展，单身者可能遇到心仪的对象。",
            "evening": "晚间适合社交活动，但要注意适度。健康方面要注意休息，避免熬夜。"
        }
    }

    # 如果星座不在备用数据中，使用默认数据
    if constellation not in backup_data:
        backup_data[constellation] = backup_data["射手座"]

        # 根据时间段返回不同的运势
    hour = datetime.now().hour
    if 5 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 18:
        period = "afternoon"
    else:
        period = "evening"

    return f"【{constellation}运势预报】\n{backup_data[constellation][period]}"


def get_horoscope_with_retry(constellation, max_retries=3):
    """带重试机制的星座运势获取函数"""
    for attempt in range(max_retries):
        try:
            return get_horoscope(constellation)
        except Exception as e:
            if attempt == max_retries - 1:  # 最后一次尝试
                print(f"获取星座运势失败，已重试{max_retries}次：{str(e)}")
                return get_backup_horoscope(constellation)
            time.sleep(1)  # 等待1秒后重试
    return get_backup_horoscope(constellation)


# 测试代码
if __name__ == "__main__":
    # 测试单个星座
    test_constellation = "射手座"
    print(f"\n测试获取{test_constellation}运势：")
    result = get_horoscope_with_retry(test_constellation)
    print(result)