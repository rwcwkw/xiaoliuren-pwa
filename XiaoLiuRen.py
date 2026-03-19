import pandas as pd
from lunardate import LunarDate
from datetime import timedelta

def _to_lunar_hour(hour: int) -> int:
    if hour in (0, 23):
        return 1
    else:
        return (hour + 1) // 2 + 1

def convert_lunar_time():
    now = pd.to_datetime('today')
    lunar_date = LunarDate.fromSolarDate(now.year, now.month, now.day)
    if now.hour == 23:
        lunar_date = lunar_date + timedelta(1)
    lunar_hour = _to_lunar_hour(now.hour) + 4
    hour_dict = {
        1: "子时", 2: "丑时", 3: "寅时", 4: "卯时",
        5: "辰时", 6: "巳时", 7: "午时", 8: "未时",
        9: "申时", 10: "酉时", 11: "戌时", 12: "亥时",
    }
    ShiChen = hour_dict[lunar_hour]
    return lunar_date, lunar_hour, ShiChen

LIUREN_DATA = {
    1: {
        "name": "大安",
        "tone": "auspicious",
        "keywords": "平稳 · 安泰 · 顺遂",
        "meaning": "大安者，稳如泰山，百事皆宜。此卦主平安顺遂，凡事不必忧虑，静待自然成就。求财得财，问病渐愈，出行无碍。"
    },
    2: {
        "name": "留连",
        "tone": "neutral",
        "keywords": "迁延 · 缠绕 · 待时",
        "meaning": "留连者，事多缠绕，进退两难。此卦主事情拖延，宜耐心守候，切勿急躁强求。静以待变，时机自至。"
    },
    3: {
        "name": "速喜",
        "tone": "auspicious",
        "keywords": "喜讯 · 速成 · 进取",
        "meaning": "速喜者，喜从天降，好事将近。此卦主行事宜速不宜迟，把握时机则诸事可成。喜事、财运皆有佳兆。"
    },
    4: {
        "name": "赤口",
        "tone": "inauspicious",
        "keywords": "口舌 · 是非 · 慎言",
        "meaning": "赤口者，言多必失，是非易起。此卦主口舌纷扰，凡事宜谨言慎行，避免争执。忍一时风平浪静。"
    },
    5: {
        "name": "小吉",
        "tone": "auspicious",
        "keywords": "小吉 · 渐进 · 稳中求胜",
        "meaning": "小吉者，吉中带稳，小有所成。此卦主循序渐进，不可贪功冒进，踏实而为终有所获。"
    },
    0: {
        "name": "空亡",
        "tone": "inauspicious",
        "keywords": "落空 · 蛰伏 · 待机",
        "meaning": "空亡者，时机未至，诸事落空。此卦主蛰伏守静，不宜强行，宜养精蓄锐，静观其变，待时而动。"
    },
}

def XiaoLiuRen():
    lunar_date, lunar_hour, ShiChen = convert_lunar_time()
    result_mth = lunar_date.month % 6
    result_day = (lunar_date.month + lunar_date.day - 1) % 6
    result_hour = (lunar_date.month + lunar_date.day + lunar_hour - 2) % 6

    keys = [result_mth, result_day, result_hour]
    results = []
    for k in keys:
        d = LIUREN_DATA[k]
        results.append({
            "name": d["name"],
            "tone": d["tone"],
            "keywords": d["keywords"],
            "meaning": d["meaning"],
        })

    return {
        "lunar_month": lunar_date.month,
        "lunar_day": lunar_date.day,
        "shichen": ShiChen,
        "result": results,
    }