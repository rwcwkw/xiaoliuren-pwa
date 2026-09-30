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

# ── 小六壬 ──────────────────────────────────────────

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
    result_mth  = lunar_date.month % 6
    result_day  = (lunar_date.month + lunar_date.day - 1) % 6
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
        "lunar_day":   lunar_date.day,
        "shichen":     ShiChen,
        "result":      results,
    }

# ── 梅花易数 ─────────────────────────────────────────

BAGUA = {
    1: {"lines": [1,1,1], "name": "乾", "element": "金"},
    2: {"lines": [0,1,1], "name": "兑", "element": "金"},
    3: {"lines": [1,0,1], "name": "离", "element": "火"},
    4: {"lines": [0,0,1], "name": "震", "element": "木"},
    5: {"lines": [1,1,0], "name": "巽", "element": "木"},
    6: {"lines": [0,1,0], "name": "坎", "element": "水"},
    7: {"lines": [1,0,0], "name": "艮", "element": "土"},
    0: {"lines": [0,0,0], "name": "坤", "element": "土"},
}

# Lookup: lines tuple → bagua entry
LINES_TO_BAGUA = {
    tuple(v["lines"]): v for v in BAGUA.values()
}

GENERATES = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
OVERCOMES  = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

def _five_elements(e1, e2):
    if e1 == e2:
        return {"relation": "比和", "outcome": "中吉", "tone": "neutral",
                "detail": f"{e1}与{e2}相同，比和，势均力敌，中吉。"}
    if GENERATES[e1] == e2:
        return {"relation": "泄气", "outcome": "小凶", "tone": "inauspicious",
                "detail": f"{e1}生{e2}，体卦泄气于用卦，力量消耗，小凶。"}
    if GENERATES[e2] == e1:
        return {"relation": "得生", "outcome": "大吉", "tone": "auspicious",
                "detail": f"{e2}生{e1}，体卦得用卦所生，如得贵人相助，大吉。"}
    if OVERCOMES[e1] == e2:
        return {"relation": "克制", "outcome": "小吉", "tone": "auspicious",
                "detail": f"{e1}克{e2}，体卦克制用卦，主动有力，小吉。"}
    if OVERCOMES[e2] == e1:
        return {"relation": "受克", "outcome": "大凶", "tone": "inauspicious",
                "detail": f"{e2}克{e1}，体卦受用卦所克，受制于人，大凶。"}
    return {"relation": "无明显生克", "outcome": "平", "tone": "neutral", "detail": "无明显生克关系。"}

def MeiHuaYiShu(num1: int, num2: int):
    # Upper and lower trigrams of the present hexagram
    upper_key = num1 % 8
    lower_key = num2 % 8
    upper = BAGUA[upper_key]
    lower = BAGUA[lower_key]

    # Combine into 6-line hexagram (upper first)
    combined = upper["lines"] + lower["lines"]

    # Changing line (1-indexed from top, so index = 6 - changing_line)
    changing_line = (num1 + num2) % 6   # 0 = line 6 (bottom)
    change_idx    = 6 - changing_line   # array index

    # Future hexagram — flip the changing line
    future = combined[:]
    future[change_idx] = 1 - future[change_idx]
    new_upper_lines = tuple(future[0:3])
    new_lower_lines = tuple(future[3:6])
    new_upper = LINES_TO_BAGUA.get(new_upper_lines, upper)
    new_lower = LINES_TO_BAGUA.get(new_lower_lines, lower)

    # Determine 体卦 (entity) and 用卦 (event)
    # The trigram that did NOT change is the 体卦
    upper_changed = (tuple(upper["lines"]) != new_upper_lines)
    if upper_changed:
        ti  = lower        # 体卦 = lower (unchanged)
        yong = upper       # 用卦 = upper (changed)
        bian = new_upper   # 变卦 = new upper
    else:
        ti   = upper
        yong = lower
        bian = new_lower

    present_outcome = _five_elements(ti["element"], yong["element"])
    future_outcome  = _five_elements(ti["element"], bian["element"])

    return {
        # Present hexagram
        "upper":       {"name": upper["name"],    "element": upper["element"]},
        "lower":       {"name": lower["name"],    "element": lower["element"]},
        "changing_line": changing_line + 1,        # 1-indexed for display
        # Future hexagram
        "new_upper":   {"name": new_upper["name"],"element": new_upper["element"]},
        "new_lower":   {"name": new_lower["name"],"element": new_lower["element"]},
        # Roles
        "ti":          {"name": ti["name"],   "element": ti["element"]},
        "yong":        {"name": yong["name"], "element": yong["element"]},
        "bian":        {"name": bian["name"], "element": bian["element"]},
        # Outcomes
        "present_outcome": present_outcome,
        "future_outcome":  future_outcome,
    }
