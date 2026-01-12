#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番剧更新提醒
使用 Bangumi API 获取每日放送
"""

import os
import requests
from datetime import datetime

# 用户追番列表（番剧名称，模糊匹配）
# 可通过环境变量配置，用逗号分隔
WATCHLIST_STR = os.environ.get("BANGUMI_WATCHLIST", "")
WATCHLIST = [x.strip() for x in WATCHLIST_STR.split(",") if x.strip()]

# Bangumi API
CALENDAR_URL = "https://api.bgm.tv/calendar"

# 星期映射
WEEKDAY_MAP = {
    0: "周一",
    1: "周二",
    2: "周三",
    3: "周四",
    4: "周五",
    5: "周六",
    6: "周日",
}


def get_calendar() -> list:
    """获取每日放送表"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; DailyTasks/1.0)"
        }
        resp = requests.get(CALENDAR_URL, headers=headers, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"获取放送表异常: {e}")
    return []


def get_today_bangumi() -> list:
    """获取今日放送的番剧"""
    calendar = get_calendar()
    if not calendar:
        return []

    # 今天是星期几 (0=周一, 6=周日)
    today_weekday = datetime.now().weekday()
    # Bangumi API 的星期 (1=周一, 7=周日)
    bgm_weekday = today_weekday + 1

    for day in calendar:
        if day.get("weekday", {}).get("id") == bgm_weekday:
            return day.get("items", [])

    return []


def filter_watchlist(bangumi_list: list) -> list:
    """筛选追番列表中的番剧"""
    if not WATCHLIST:
        return bangumi_list  # 未配置追番列表则返回全部

    matched = []
    for bangumi in bangumi_list:
        name = bangumi.get("name", "")
        name_cn = bangumi.get("name_cn", "")

        for watch_name in WATCHLIST:
            if watch_name.lower() in name.lower() or watch_name.lower() in name_cn.lower():
                matched.append(bangumi)
                break

    return matched


def format_bangumi_message() -> str:
    """格式化番剧消息"""
    today = datetime.now()
    weekday = WEEKDAY_MAP.get(today.weekday(), "")
    date_str = today.strftime("%Y-%m-%d")

    today_bangumi = get_today_bangumi()
    filtered = filter_watchlist(today_bangumi)

    lines = [f"<b>番剧更新 - {date_str} {weekday}</b>", ""]

    if not today_bangumi:
        lines.append("获取放送表失败")
        return "<br>".join(lines)

    if WATCHLIST and not filtered:
        lines.append("今日追番列表中没有更新")
        lines.append("")
        lines.append(f"<small>追番: {', '.join(WATCHLIST)}</small>")
        return "<br>".join(lines)

    # 显示番剧列表
    if WATCHLIST:
        lines.append(f"<b>今日更新 ({len(filtered)} 部):</b>")
    else:
        lines.append(f"<b>今日全部更新 ({len(filtered)} 部):</b>")

    for bangumi in filtered[:10]:  # 最多显示10部
        name_cn = bangumi.get("name_cn") or bangumi.get("name", "未知")
        rating = bangumi.get("rating", {}).get("score", "N/A")

        air_info = ""
        if bangumi.get("air_date"):
            air_info = f" ({bangumi['air_date']})"

        lines.append(f"• {name_cn} ⭐{rating}{air_info}")

    if len(filtered) > 10:
        lines.append(f"... 还有 {len(filtered) - 10} 部")

    return "<br>".join(lines)


def run() -> str:
    """
    执行番剧更新查询

    Returns:
        格式化的番剧更新消息
    """
    print("=" * 50)
    print("番剧更新提醒")
    print("=" * 50)

    return format_bangumi_message()
