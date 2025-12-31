from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.chat import ChatRequest, ChatResponse
from src.utils.mock_data import mock_orders
from src.services.business_api import call_business_api
from src.services.knowledge_base import query_knowledge_base
import time


# 初始化FastAPI应用
app = FastAPI(title="智能服务助手", description="智能服务助手")

# 添加CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域访问，生产环境应限制为特定域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)


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
        response_content = "您好！我是智能服务助手，很高兴为您服务。请问有什么可以帮助您的？"
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
        import re
        order_id_match = re.search(r"order_\d+", user_input)
        order_id = order_id_match.group() if order_id_match else "order_124"
        result = call_business_api("cancel_order", {
            "order_id": order_id
        })
        response_content = f"订单{order_id}取消成功！"
    # 处理修改订单相关
    elif any(keyword in lower_input for keyword in ["修改", "调整", "更改", "改", "变更"]) or any(keyword in lower_input for keyword in ["服务时间", "时间"]):
        # 检查订单ID
        order_id = None
        for order in mock_orders:
            if order["order_id"] in user_input:
                order_id = order["order_id"]
                break
        
        # 默认使用第一个订单
        if not order_id and mock_orders:
            order_id = mock_orders[0]["order_id"]
        elif not mock_orders:
            response_content = "您当前没有订单。"
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
        order_id = mock_orders[0]["order_id"] if mock_orders else "order_123"
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
            response_content = "我是智能服务助手，我可以为您提供以下服务：\n1. 查询服务笔记\n2. 查询订单信息\n3. 修改订单时间\n4. 取消订单\n\n您可以尝试说：\"我想查询订单\"或\"我想修改服务时间\""
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
