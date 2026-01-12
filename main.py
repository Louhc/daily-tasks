#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日任务主入口
- 米游社签到
- 天气推送
- 番剧更新提醒
"""

import os
from tasks import miyoushe, weather, bangumi
from utils.push import push_wechat


def main():
    print("=" * 60)
    print("每日任务开始")
    print("=" * 60)

    all_messages = []

    # 1. 米游社签到
    try:
        miyoushe_results = miyoushe.run()
        if miyoushe_results:
            all_messages.append("<b>【米游社签到】</b>")
            all_messages.extend(miyoushe_results)
            all_messages.append("")
    except Exception as e:
        print(f"米游社签到异常: {e}")
        all_messages.append(f"<b>【米游社签到】</b>")
        all_messages.append(f"执行异常: {e}")
        all_messages.append("")

    # 2. 天气推送
    try:
        weather_msg = weather.run()
        if weather_msg:
            all_messages.append("<b>【今日天气】</b>")
            all_messages.append(weather_msg)
            all_messages.append("")
    except Exception as e:
        print(f"天气推送异常: {e}")
        all_messages.append(f"<b>【今日天气】</b>")
        all_messages.append(f"执行异常: {e}")
        all_messages.append("")

    # 3. 番剧更新
    try:
        bangumi_msg = bangumi.run()
        if bangumi_msg:
            all_messages.append("<b>【番剧更新】</b>")
            all_messages.append(bangumi_msg)
            all_messages.append("")
    except Exception as e:
        print(f"番剧更新异常: {e}")
        all_messages.append(f"<b>【番剧更新】</b>")
        all_messages.append(f"执行异常: {e}")
        all_messages.append("")

    # 推送汇总消息
    if all_messages:
        summary = "<br>".join(all_messages)
        push_wechat("每日任务报告", summary)

    print("=" * 60)
    print("每日任务完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
