#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送通知模块
"""

import os
import requests

PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN", "")


def push_wechat(title: str, content: str, template: str = "html") -> bool:
    """
    PushPlus 微信推送

    Args:
        title: 消息标题
        content: 消息内容
        template: 模板类型 (html, txt, json, markdown)

    Returns:
        是否推送成功
    """
    if not PUSHPLUS_TOKEN:
        print("未配置 PUSHPLUS_TOKEN，跳过推送")
        return False

    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": template
    }

    try:
        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        if result.get("code") == 200:
            print(f"微信推送成功: {title}")
            return True
        else:
            print(f"微信推送失败: {result}")
            return False
    except Exception as e:
        print(f"微信推送异常: {e}")
        return False
