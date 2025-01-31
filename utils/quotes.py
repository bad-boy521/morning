import random
from datetime import datetime


class QuoteManager:
    def __init__(self):
        # 预设激励语录库
        self.quotes = [
            "每一个清晨都是新的开始，带着希望启程吧！",
            "生活中最美的事物往往是简单的日常。",
            "保持微笑，因为你永远不知道谁会爱上你的笑容。",
            "今天的付出是为了明天更好的收获。",
            "做最好的自己，成为更好的人。",
            "生活不是等待暴风雨过去，而是学会在雨中翩翩起舞。",
            "每一个今天都是明天的礼物。",
            "保持热爱，奔赴山海。",
            "愿你的每一天都充满阳光。",
            "简单的事重复做，重复的事用心做。",
            "不要辜负今天的太阳。",
            "温柔对待这个世界，这个世界也会温柔对待你。",
            "带着阳光般的微笑，走过漫漫人生路。",
            "心怀感恩，保持热爱。",
            "愿你的生活既有诗意也有远方。",
            "每个人都是自己人生的主角。",
            "生活总有不如意，但请保持乐观向上。",
            "今天的坚持，是为了明天的收获。",
            "保持善良，保持勇气，保持希望。",
            "生命中最重要的不是位置，而是方向。"
        ]

        # 节日祝福语库
        self.festival_quotes = {
            "0101": "新年快乐！愿新的一年充满希望和喜悦！",
            "0214": "情人节快乐！愿爱情甜蜜永恒！",
            "0308": "女神节快乐！愿你永远光芒万丈！",
            "0501": "劳动节快乐！辛勤付出，必有收获！",
            "0601": "儿童节快乐！愿我们永远保持童心！",
            "0707": "七夕快乐！愿你找到属于自己的那颗星！",
            "1001": "国庆节快乐！为祖国献上最真挚的祝福！",
            "1224": "平安夜快乐！愿你被温柔以待！",
            "1225": "圣诞节快乐！愿你的愿望都能实现！"
        }

    def get_daily_quote(self):
        """获取每日一句，包含节日祝福"""
        today = datetime.now().strftime('%m%d')

        # 如果是特殊节日，返回节日祝福
        if today in self.festival_quotes:
            return self.festival_quotes[today]

            # 否则随机返回一条激励语录
        return random.choice(self.quotes)

    # 创建全局唯一的QuoteManager实例


quote_manager = QuoteManager()


def get_daily_quote():
    """对外提供的获取每日一句的接口"""
    return quote_manager.get_daily_quote()