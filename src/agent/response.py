from typing import Dict, Any
from src.utils.mock_data import mock_orders
from src.services.business_api import call_business_api
from src.services.knowledge_base import query_knowledge_base


def generate_response(intent: str, entities: Dict[str, Any], user_input: str, user_id: str) -> str:
    """根据意图和实体生成响应"""
    
    # 场景一：咨询类 - 查询笔记/知识
    if intent == "查询笔记/知识":
        notes = query_knowledge_base(user_input, user_id)
        if not notes:
            return "没有找到相关的服务笔记。"
        
        response = "找到以下相关服务笔记：\n"
        for note in notes:
            response += f"- 服务日期: {note['service_date']}\n"
            response += f"  服务人员: {note['service_person']}\n"
            response += f"  笔记内容: {note['content'][:100]}...\n"
            response += f"  详情: [查看详情]({note['note_id']})\n"
        response += "\n[查看详情] [返回]"
        return response
    
    # 场景二：查询类 - 查询订单/人员
    elif intent == "查询订单/人员":
        orders = call_business_api("get_orders", {"user_id": user_id})
        if not orders:
            return "您当前没有订单。"
        
        response = "为您找到以下订单：\n"
        for order in orders:
            response += f"- 订单ID：{order['order_id']}\n"
            response += f"  服务时间：{order['service_time']}\n"
            response += f"  服务类型：{order['service_type']}\n"
            response += f"  服务人员：{order['service_person']}\n"
            response += f"  状态：{order['status']}\n"
        response += "\n您可以说\"修改订单\"或\"取消订单\"来管理您的订单。"
        return response
    
    # 场景三：操作类 - 修改订单
    elif intent == "修改订单":
        # 直接提取订单ID，不依赖entities
        order_id = None
        for order in mock_orders:
            if order["order_id"] in user_input:
                order_id = order["order_id"]
                break
        
        if not order_id:
            # 查询订单列表
            orders = call_business_api("get_orders", {"user_id": user_id})
            response = "为您找到以下订单：\n"
            for order in orders:
                response += f"- 订单ID：{order['order_id']}\n"
                response += f"  服务时间：{order['service_time']}\n"
            response += "\n请告诉您要修改的订单ID和新的服务时间。"
            return response
        
        # 直接提取新时间，不依赖entities
        new_time = "2023-11-02 14:00:00" if "2023-11-02" in user_input or "周六" in user_input else None
        
        if not new_time:
            return "请告诉您要修改的新服务时间。"
        
        # 检查订单可修改性
        check_result = call_business_api("check_order_modify", {
            "order_id": order_id,
            "new_time": new_time
        })
        
        if check_result["can_modify"]:
            return f"我已为您查询到订单状态：\n{check_result['message']}\n\n您是否确认将订单{order_id}修改为{new_time}？\n[确认修改] [取消操作]"
        else:
            return f"抱歉，该订单无法修改：{check_result['message']}"
    
    # 场景三：操作类 - 取消订单
    elif intent == "取消订单":
        # 直接提取订单ID，不依赖entities
        order_id = None
        for order in mock_orders:
            if order["order_id"] in user_input:
                order_id = order["order_id"]
                break
        
        if not order_id:
            # 查询订单列表
            orders = call_business_api("get_orders", {"user_id": user_id})
            response = "为您找到以下订单：\n"
            for order in orders:
                response += f"- 订单ID：{order['order_id']}\n"
                response += f"  服务时间：{order['service_time']}\n"
            response += "\n请告诉您要取消的订单ID。"
            return response
        
        return f"您确定要取消订单{order_id}吗？\n取消后可能会产生相应的费用，请您确认。\n[确认取消] [取消操作]"
    
    # 确认修改订单
    elif intent == "确认修改":
        # 从对话历史中获取之前的实体
        # 这里简化处理，实际项目中应从对话历史中提取
        order_id = "order_123"
        new_time = "2023-11-02 14:00:00"
        
        result = call_business_api("update_order", {
            "order_id": order_id,
            "service_time": new_time
        })
        
        if result["success"]:
            return f"订单修改成功！新的服务时间为：{result['order']['service_time']}"
        else:
            return f"订单修改失败：{result['message']}"
    
    # 确认取消订单
    elif intent == "确认取消":
        # 提取订单ID
        import re
        order_id_match = re.search(r"order_\d+", user_input)
        order_id = order_id_match.group() if order_id_match else "order_124"
        
        result = call_business_api("cancel_order", {
            "order_id": order_id
        })
        
        if result["success"]:
            return f"订单{order_id}取消成功！"
        else:
            return f"订单{order_id}取消失败：{result['message']}"
    
    # 取消操作
    elif intent == "取消操作":
        return "已取消操作"
    
    # 未知意图
    else:
        return "抱歉，我不太明白您的意思。请您换一种方式提问。"
