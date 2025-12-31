#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本，直接测试好慷智能体的核心功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8000"
USER_ID = "user_123"
MODEL = "haokang-agent"

# 等待服务启动
time.sleep(3)

# 测试健康检查
def test_health():
    """测试健康检查接口"""
    print("\n=== 测试健康检查 ===")
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

# 发送聊天请求
def send_message(message):
    """发送聊天消息"""
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": message}],
        "user": USER_ID
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 简单测试场景
def test_scenarios():
    """测试三个核心场景"""
    # 场景一：查询服务笔记
    print("\n=== 场景一：查询服务笔记 ===")
    response = send_message("上次服务的笔记是什么？")
    print(f"用户: 上次服务的笔记是什么？")
    print(f"智能体: {response['choices'][0]['message']['content']}")
    
    # 场景二：查询订单
    print("\n=== 场景二：查询订单 ===")
    response = send_message("我有哪些订单？")
    print(f"用户: 我有哪些订单？")
    print(f"智能体: {response['choices'][0]['message']['content']}")
    
    # 场景三：修改订单
    print("\n=== 场景三：修改订单 ===")
    response = send_message("我想修改订单order_123的时间为2023-11-02 14:00")
    print(f"用户: 我想修改订单order_123的时间为2023-11-02 14:00")
    print(f"智能体: {response['choices'][0]['message']['content']}")
    
    # 确认修改
    response = send_message("确认修改")
    print(f"用户: 确认修改")
    print(f"智能体: {response['choices'][0]['message']['content']}")
    
    # 场景三：取消订单
    print("\n=== 场景三：取消订单 ===")
    response = send_message("我想取消订单order_124")
    print(f"用户: 我想取消订单order_124")
    print(f"智能体: {response['choices'][0]['message']['content']}")
    
    # 确认取消
    response = send_message("确认取消")
    print(f"用户: 确认取消")
    print(f"智能体: {response['choices'][0]['message']['content']}")

# 主函数
if __name__ == "__main__":
    print("好慷智能体简单测试")
    print("=" * 50)
    
    # 测试健康检查
    if test_health():
        # 测试场景
        test_scenarios()
        print("\n所有测试完成！")
    else:
        print("服务未启动，测试失败！")
