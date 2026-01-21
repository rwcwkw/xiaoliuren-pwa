import pandas as pd
from lunardate import LunarDate

def _to_lunar_hour(hour: int) -> int:
    if hour in (0, 23):
        return 1
    else:
        return (hour + 1) // 2 + 1

def convert_lunar_time():
    now = pd.to_datetime('today')
    lunar_date = LunarDate.fromSolarDate(now.year, now.month, now.day)
    lunar_hour = _to_lunar_hour(now.hour) + 4

    hour_dict = {
        1: "子时", 2: "丑时", 3: "寅时", 4: "卯时",
        5: "辰时", 6: "巳时", 7: "午时", 8: "未时",
        9: "申时", 10: "酉时", 11: "戌时", 12: "亥时",
    }

    ShiChen = hour_dict[lunar_hour]
    return lunar_date, lunar_hour, ShiChen

def XiaoLiuRen():
    lunar_date, lunar_hour, ShiChen = convert_lunar_time()

    result_mth = lunar_date.month % 6
    result_day = (lunar_date.month + lunar_date.day - 1) % 6
    result_hour = (lunar_date.month + lunar_date.day + lunar_hour - 2) % 6

    LiuRen_dict = {
        1: "大安",
        2: "留连",
        3: "速喜",
        4: "赤口",
        5: "小吉",
        0: "空亡",
    }

    return {
        "lunar_month": lunar_date.month,
        "lunar_day": lunar_date.day,
        "shichen": ShiChen,
        "result": [
            LiuRen_dict[result_mth],
            LiuRen_dict[result_day],
            LiuRen_dict[result_hour]
        ]
    }