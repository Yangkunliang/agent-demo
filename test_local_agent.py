#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试本地好慷智能体
与本地FastAPI服务交互，测试三个核心场景
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USER_ID = "user_123"
MODEL = "haokang-agent"

# 发送请求
def send_chat_request(messages):
    """发送聊天请求"""
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "user": USER_ID
    }
    
    print(f"[DEBUG] 请求URL: {url}")
    print(f"[DEBUG] 请求头: {headers}")
    print(f"[DEBUG] 请求体: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"[DEBUG] 响应状态码: {response.status_code}")
    print(f"[DEBUG] 响应头: {response.headers}")
    
    try:
        response_json = response.json()
        print(f"[DEBUG] 响应体: {json.dumps(response_json, indent=2)}")
        return response_json
    except Exception as e:
        print(f"[DEBUG] 响应解析失败: {e}")
        print(f"[DEBUG] 原始响应: {response.text}")
        return {}


# 测试场景一：咨询类 - 查询笔记/知识
def test_query_service_notes():
    """测试查询服务笔记"""
    print("\n=== 场景一：查询服务笔记 ===")
    
    messages = [
        {
            "role": "user",
            "content": "上次服务的笔记是什么？"
        }
    ]
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: {messages[0]['content']}")
    print(f"智能体: {assistant_response}")
    print("=" * 50)

# 测试场景二：查询类 - 查询订单/人员
def test_query_orders():
    """测试查询订单"""
    print("\n=== 场景二：查询订单 ===")
    
    messages = [
        {
            "role": "user",
            "content": "我有哪些订单？"
        }
    ]
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: {messages[0]['content']}")
    print(f"智能体: {assistant_response}")
    print("=" * 50)

# 测试场景三：操作类 - 修改订单
def test_modify_order():
    """测试修改订单"""
    print("\n=== 场景三：修改订单 ===")
    
    # 第一步：请求修改订单
    messages = [
        {
            "role": "user",
            "content": "我想修改订单order_123的时间为2023-11-02 14:00"
        }
    ]
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: {messages[0]['content']}")
    print(f"智能体: {assistant_response}")
    
    # 第二步：确认修改
    messages.append({
        "role": "assistant",
        "content": assistant_response
    })
    messages.append({
        "role": "user",
        "content": "确认修改"
    })
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: 确认修改")
    print(f"智能体: {assistant_response}")
    print("=" * 50)

# 测试场景三：操作类 - 取消订单
def test_cancel_order():
    """测试取消订单"""
    print("\n=== 场景三：取消订单 ===")
    
    # 第一步：请求取消订单
    messages = [
        {
            "role": "user",
            "content": "我想取消订单order_124"
        }
    ]
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: {messages[0]['content']}")
    print(f"智能体: {assistant_response}")
    
    # 第二步：确认取消
    messages.append({
        "role": "assistant",
        "content": assistant_response
    })
    messages.append({
        "role": "user",
        "content": "确认取消"
    })
    
    response = send_chat_request(messages)
    assistant_response = response["choices"][0]["message"]["content"]
    
    print(f"用户: 确认取消")
    print(f"智能体: {assistant_response}")
    print("=" * 50)

# 测试健康检查
def test_health_check():
    """测试健康检查接口"""
    print("\n=== 健康检查 ===")
    
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    
    print(f"健康检查结果: {response.json()}")
    print(f"状态码: {response.status_code}")
    print("=" * 50)

# 主函数
def main():
    """主函数"""
    print("好慷智能体本地测试")
    print("=" * 50)
    
    # 测试健康检查
    test_health_check()
    
    # 测试三个场景
    test_query_service_notes()
    test_query_orders()
    test_modify_order()
    test_cancel_order()
    
    print("\n所有场景测试完成！")

if __name__ == "__main__":
    main()
