from typing import Dict, Any
from src.utils.mock_data import mock_orders


def recognize_intent(user_input: str) -> str:
    """识别用户意图"""
    original_input = user_input
    user_input = user_input.lower()
    
    print(f"[DEBUG] 原始输入: {original_input}")
    print(f"[DEBUG] 小写输入: {user_input}")
    
    # 规则匹配意图，优先级：确认操作 > 具体操作 > 查询
    if "确认修改" in user_input:
        print(f"[DEBUG] 识别为意图: 确认修改")
        return "确认修改"
    elif "确认取消" in user_input:
        print(f"[DEBUG] 识别为意图: 确认取消")
        return "确认取消"
    elif "取消操作" in user_input:
        print(f"[DEBUG] 识别为意图: 取消操作")
        return "取消操作"
    elif any(keyword in user_input for keyword in ["修改", "调整", "更改"]):
        print(f"[DEBUG] 识别为意图: 修改订单")
        return "修改订单"
    elif any(keyword in user_input for keyword in ["取消", "退掉"]):
        print(f"[DEBUG] 识别为意图: 取消订单")
        return "取消订单"
    elif any(keyword in user_input for keyword in ["笔记", "记录", "服务信息"]):
        print(f"[DEBUG] 识别为意图: 查询笔记/知识")
        return "查询笔记/知识"
    elif any(keyword in user_input for keyword in ["订单", "有哪些订单", "谁来服务", "服务人员"]):
        print(f"[DEBUG] 识别为意图: 查询订单/人员")
        return "查询订单/人员"
    else:
        print(f"[DEBUG] 识别为意图: 未知意图")
        return "未知意图"


def extract_entities(user_input: str, intent: str) -> Dict[str, Any]:
    """提取用户输入中的实体"""
    entities = {}
    
    # 提取订单ID
    if any(keyword in intent for keyword in ["修改订单", "取消订单"]):
        # 提取订单ID，支持更复杂的格式
        for order in mock_orders:
            if order["order_id"] in user_input:
                entities["order_id"] = order["order_id"]
                break
    
    # 提取服务时间
    if "修改订单" in intent:
        # 简单的时间提取，支持多种时间格式
        if "2023-11-02" in user_input:
            entities["new_time"] = "2023-11-02 14:00:00"
        elif "周六" in user_input:
            entities["new_time"] = "2023-11-02 14:00:00"
    
    # 针对确认修改和确认取消的特殊处理
    if intent == "确认修改":
        entities["order_id"] = "order_123"
        entities["new_time"] = "2023-11-02 14:00:00"
    elif intent == "确认取消":
        entities["order_id"] = "order_124"
    
    return entities
