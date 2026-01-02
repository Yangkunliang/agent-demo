from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Message(BaseModel):
    """消息模型"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """聊天请求模型"""
    model: str
    messages: List[Message]
    user: str
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.1
    stream: Optional[bool] = False


class ChatResponse(BaseModel):
    """聊天响应模型"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]
