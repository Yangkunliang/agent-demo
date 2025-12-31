#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好慷智能体本地实现
基于FastAPI的聊天智能体，实现三个核心场景
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import yaml
import time

# 加载配置文件
def load_config():
    with open('intent_model.yml', 'r', encoding='utf-8') as f:
        intent_model = yaml.safe_load(f)
    with open('api_config.yml', 'r', encoding='utf-8') as f:
        api_config = yaml.safe_load(f)
    return intent_model, api_config

intent_model, api_config = load_config()

# 初始化FastAPI应用
app = FastAPI(title="好慷智能体", description="好慷全能管家AI智能助理")

# 添加CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域访问，生产环境应限制为特定域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 数据模型
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    user: str
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.1

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

# 模拟数据库
mock_orders = [
    {
        "order_id": "order_123",
        "service_time": "2023-11-01 14:00:00",
        "service_type": "深度清洁",
        "service_person": "张阿姨",
        "status": "已确认"
    },
    {
        "order_id": "order_124",
        "service_time": "2023-11-08 14:00:00",
        "service_type": "日常保洁",
        "service_person": "李阿姨",
        "status": "已确认"
    }
]

mock_service_notes = [
    {
        "note_id": "note_123",
        "content": "本次服务完成了客厅、卧室的清洁，客户对服务质量满意，提出下次可以增加厨房清洁",
        "service_date": "2023-10-15",
        "service_person": "张阿姨",
        "user_id": "user_123"
    },
    {
        "note_id": "note_124",
        "content": "本次服务完成了厨房、卫生间的深度清洁，客户提出了一些建议，希望下次服务时注意",
        "service_date": "2023-10-01",
        "service_person": "李阿姨",
        "user_id": "user_123"
    }
]

# 意图识别模块
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

# 提取实体
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

# 模拟业务API调用
def call_business_api(api_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """模拟调用业务API"""
    if api_name == "get_orders":
        return mock_orders
    elif api_name == "check_order_modify":
        return {
            "can_modify": True,
            "message": "该订单可以修改，周六有空位",
            "available_slots": ["2023-11-02 14:00:00", "2023-11-02 15:00:00"]
        }
    elif api_name == "update_order":
        for order in mock_orders:
            if order["order_id"] == params["order_id"]:
                order["service_time"] = params["service_time"]
                return {
                    "success": True,
                    "message": "订单修改成功",
                    "order": order
                }
        return {
            "success": False,
            "message": "订单不存在"
        }
    elif api_name == "cancel_order":
        for i, order in enumerate(mock_orders):
            if order["order_id"] == params["order_id"]:
                mock_orders.pop(i)
                return {
                    "success": True,
                    "message": "订单取消成功"
                }
        return {
            "success": False,
            "message": "订单不存在"
        }
    else:
        return {"error": "API不存在"}

# 模拟知识库查询
def query_knowledge_base(user_query: str, user_id: str) -> List[Dict[str, Any]]:
    """模拟查询知识库"""
    # 简单的关键词匹配，实际项目中应使用向量搜索
    results = []
    keywords = user_query.split()
    
    # 如果用户没有输入具体关键词，返回所有匹配用户ID的笔记
    if len(keywords) == 0:
        for note in mock_service_notes:
            if note["user_id"] == user_id:
                results.append(note)
    else:
        for note in mock_service_notes:
            if note["user_id"] == user_id and any(keyword in note["content"] for keyword in keywords):
                results.append(note)
    
    # 如果没有匹配到结果，返回所有匹配用户ID的笔记
    if len(results) == 0:
        for note in mock_service_notes:
            if note["user_id"] == user_id:
                results.append(note)
    
    return results

# 生成响应
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
    elif intent == "确认取消" or (intent == "取消订单" and "确认" in user_input):
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

# 聊天完成接口
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    """聊天完成接口"""
    # 获取最新的用户消息
    user_message = request.messages[-1]
    if user_message.role != "user":
        raise HTTPException(status_code=400, detail="Last message must be from user")
    
    user_input = user_message.content
    user_id = request.user
    
    # 简化处理：直接根据关键词生成响应
    lower_input = user_input.lower()
    
    # 处理问候语
    if any(keyword in lower_input for keyword in ["你好", "您好", "hi", "hello"]):
        response_content = "您好！我是好慷全能管家AI智能助理，很高兴为您服务。请问有什么可以帮助您的？"
    # 处理确认修改
    elif "确认修改" in lower_input:
        # 执行修改订单操作
        order_id = "order_123"
        new_time = "2023-11-02 14:00:00"
        result = call_business_api("update_order", {
            "order_id": order_id,
            "service_time": new_time
        })
        response_content = f"订单修改成功！新的服务时间为：{result['order']['service_time']}"
    # 处理确认取消
    elif "确认取消" in lower_input:
        # 执行取消订单操作
        order_id = "order_124"
        result = call_business_api("cancel_order", {
            "order_id": order_id
        })
        response_content = "订单取消成功！"
    # 处理修改订单相关
    elif any(keyword in lower_input for keyword in ["修改", "调整", "更改", "改", "变更"]) or any(keyword in lower_input for keyword in ["服务时间", "时间"]):
        # 检查订单ID
        order_id = None
        for order in mock_orders:
            if order["order_id"] in user_input:
                order_id = order["order_id"]
                break
        
        # 默认使用第一个订单
        if not order_id:
            order_id = mock_orders[0]["order_id"]
        
        # 检查新时间
        new_time = "2023-11-02 14:00:00"
        # 检查可修改性
        check_result = call_business_api("check_order_modify", {
            "order_id": order_id,
            "new_time": new_time
        })
        if check_result["can_modify"]:
            response_content = f"我已为您查询到订单状态：\n{check_result['message']}\n\n您是否确认将订单{order_id}修改为{new_time}？\n[确认修改] [取消操作]"
        else:
            response_content = f"抱歉，该订单无法修改：{check_result['message']}"
    # 处理取消订单
    elif any(keyword in lower_input for keyword in ["取消", "退掉", "撤销"]) and "订单" in lower_input:
        # 检查订单ID
        order_id = None
        for order in mock_orders:
            if order["order_id"] in user_input:
                order_id = order["order_id"]
                break
        
        if order_id:
            # 已指定订单，询问确认
            response_content = f"您确定要取消订单{order_id}吗？\n取消后可能会产生相应的费用，请您确认。\n<button onclick='sendMessage(\"确认取消订单{order_id}\")' class='message-button'>确认取消</button>"
        else:
            # 未指定订单，让用户选择
            if len(mock_orders) == 0:
                response_content = "您当前没有订单。"
            elif len(mock_orders) == 1:
                # 只有一笔订单，直接询问确认
                order_id = mock_orders[0]["order_id"]
                response_content = f"您确定要取消订单{order_id}吗？\n取消后可能会产生相应的费用，请您确认。\n<button onclick='sendMessage(\"确认取消订单{order_id}\")' class='message-button'>确认取消</button>"
            else:
                # 多笔订单，让用户选择
                response_content = "您有以下订单，请问您要取消哪一笔？\n"
                for order in mock_orders:
                    response_content += f"- 订单ID：{order['order_id']}，服务时间：{order['service_time']}，服务类型：{order['service_type']}\n"
                response_content += "\n请回复'取消订单+订单ID'，例如：取消订单order_123"
    # 处理查询服务笔记
    elif any(keyword in lower_input for keyword in ["笔记", "记录", "服务信息", "上次服务"]):
        notes = query_knowledge_base(user_input, user_id)
        if not notes:
            response_content = "没有找到相关的服务笔记。"
        else:
            response_content = "找到以下相关服务笔记：\n"
            for note in notes:
                response_content += f"- 服务日期: {note['service_date']}\n"
                response_content += f"  服务人员: {note['service_person']}\n"
                response_content += f"  笔记内容: {note['content'][:100]}...\n"
                response_content += f"  详情: [查看详情]({note['note_id']})\n"
            response_content += "\n[查看详情] [返回]"
    # 处理查询订单
    elif any(keyword in lower_input for keyword in ["订单", "有哪些订单", "谁来服务", "服务人员"]):
        orders = call_business_api("get_orders", {"user_id": user_id})
        if not orders:
            response_content = "您当前没有订单。"
        else:
            response_content = "为您找到以下订单：\n"
            for order in orders:
                response_content += f"- 订单ID：{order['order_id']}\n"
                response_content += f"  服务时间：{order['service_time']}\n"
                response_content += f"  服务类型：{order['service_type']}\n"
                response_content += f"  服务人员：{order['service_person']}\n"
                response_content += f"  状态：{order['status']}\n"
            response_content += "\n您可以说\"修改订单\"或\"取消订单\"来管理您的订单。"
    # 处理修改服务时间
    elif "修改服务时间" in lower_input or "更改服务时间" in lower_input:
        order_id = mock_orders[0]["order_id"]
        new_time = "2023-11-02 14:00:00"
        check_result = call_business_api("check_order_modify", {
            "order_id": order_id,
            "new_time": new_time
        })
        response_content = f"我已为您查询到订单状态：\n{check_result['message']}\n\n您是否确认将订单{order_id}修改为{new_time}？\n[确认修改] [取消操作]"
    # 默认响应
    else:
        # 尝试匹配一些常见问题
        if any(keyword in lower_input for keyword in ["帮助", "功能", "能做什么"]):
            response_content = "我是好慷全能管家AI智能助理，我可以为您提供以下服务：\n1. 查询服务笔记\n2. 查询订单信息\n3. 修改订单时间\n4. 取消订单\n\n您可以尝试说：\"我想查询订单\"或\"我想修改服务时间\""
        else:
            response_content = f"您说的是：'{user_input}'，我正在努力理解您的需求...\n\n您可以尝试以下问题：\n- 查询服务笔记\n- 查询订单\n- 修改订单时间\n- 取消订单"
    
    # 构建响应
    response = ChatResponse(
        id=f"chatcmpl-{int(time.time())}",
        created=int(time.time()),
        model=request.model,
        choices=[
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }
        ],
        usage={
            "prompt_tokens": len(user_input),
            "completion_tokens": len(response_content),
            "total_tokens": len(user_input) + len(response_content)
        }
    )
    
    return response

# 健康检查接口
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}

# 主函数
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
