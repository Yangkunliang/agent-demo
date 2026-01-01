from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models.chat import ChatRequest, ChatResponse
from src.services.dify_service import DifyService
from dotenv import load_dotenv
import time

# 加载.env文件中的环境变量
load_dotenv()

# 初始化Dify服务
try:
    dify_service = DifyService()
except ValueError as e:
    # 如果环境变量未配置，设置为None，后续使用默认逻辑
    dify_service = None
    print(f"Dify service initialization failed: {e}")


# 初始化FastAPI应用
app = FastAPI(title="智能服务助手", description="智能服务助手")

# 添加CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # 明确允许前端来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
    expose_headers=["*"],  # 暴露所有响应头
    max_age=600,  # 预检请求结果缓存时间
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
    response_content = ""
    
    # 直接使用Dify API，不做降级处理
    if dify_service:
        # 将Message对象转换为Python字典列表
        messages_dict = [msg.dict() for msg in request.messages]
        dify_response = dify_service.chat_completion(messages_dict, user_id)
        response_content = dify_service.get_chat_response_content(dify_response)
    else:
        # 如果Dify服务未初始化，抛出错误
        raise HTTPException(status_code=500, detail="Dify service not initialized")
    

    
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
