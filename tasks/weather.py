#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新加坡天气推送
使用新加坡政府免费 API (data.gov.sg)
"""

import os
import requests
from datetime import datetime

# 默认区域：新加坡国立大学所在区域
DEFAULT_AREA = os.environ.get("WEATHER_AREA", "Queenstown")

# API 地址
FORECAST_2H_URL = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
FORECAST_24H_URL = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"


def get_2h_forecast(area: str = None) -> dict:
    """获取2小时天气预报"""
    area = area or DEFAULT_AREA
    try:
        resp = requests.get(FORECAST_2H_URL, timeout=10)
        data = resp.json()

        forecasts = data.get("items", [{}])[0].get("forecasts", [])
        for f in forecasts:
            if f.get("area") == area:
                return {
                    "area": area,
                    "forecast": f.get("forecast", "Unknown"),
                    "time": data.get("items", [{}])[0].get("valid_period", {}).get("start", "")
                }

        # 如果找不到指定区域，返回第一个
        if forecasts:
            return {
                "area": forecasts[0].get("area", "Unknown"),
                "forecast": forecasts[0].get("forecast", "Unknown"),
                "time": data.get("items", [{}])[0].get("valid_period", {}).get("start", ""),
                "note": f"未找到 {area}，显示 {forecasts[0].get('area')}"
            }
    except Exception as e:
        print(f"获取2小时预报异常: {e}")

    return None


def get_24h_forecast() -> dict:
    """获取24小时天气预报"""
    try:
        resp = requests.get(FORECAST_24H_URL, timeout=10)
        data = resp.json()

        general = data.get("items", [{}])[0].get("general", {})
        periods = data.get("items", [{}])[0].get("periods", [])

        return {
            "temperature": {
                "low": general.get("temperature", {}).get("low", "N/A"),
                "high": general.get("temperature", {}).get("high", "N/A"),
            },
            "humidity": {
                "low": general.get("relative_humidity", {}).get("low", "N/A"),
                "high": general.get("relative_humidity", {}).get("high", "N/A"),
            },
            "forecast": general.get("forecast", "Unknown"),
            "periods": periods
        }
    except Exception as e:
        print(f"获取24小时预报异常: {e}")

    return None


def format_weather_message(area: str = None) -> str:
    """格式化天气消息"""
    area = area or DEFAULT_AREA
    today = datetime.now().strftime("%Y-%m-%d")

    forecast_2h = get_2h_forecast(area)
    forecast_24h = get_24h_forecast()

    lines = [f"<b>新加坡天气 - {today}</b>", ""]

    if forecast_24h:
        temp = forecast_24h["temperature"]
        humidity = forecast_24h["humidity"]
        lines.append(f"温度: {temp['low']}°C - {temp['high']}°C")
        lines.append(f"湿度: {humidity['low']}% - {humidity['high']}%")
        lines.append(f"全天: {forecast_24h['forecast']}")
        lines.append("")

    if forecast_2h:
        lines.append(f"<b>{forecast_2h['area']} 近期:</b>")
        lines.append(f"{forecast_2h['forecast']}")

    return "<br>".join(lines)


def run(area: str = None) -> str:
    """
    执行天气查询并返回格式化消息

    Args:
        area: 区域名称，默认使用环境变量 WEATHER_AREA 或 Queenstown

    Returns:
        格式化的天气消息
    """
    print("=" * 50)
    print("新加坡天气查询")
    print("=" * 50)

    return format_weather_message(area)
