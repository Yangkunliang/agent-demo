from typing import Dict, Any, List
import os
import requests


class DifyService:
    """Dify API服务类"""
    
    def __init__(self):
        """初始化Dify服务"""
        # 从环境变量获取配置
        self.api_key = os.environ.get('DIFY_API_KEY', '')
        self.app_id = os.environ.get('DIFY_APP_ID', '')
        
        # 验证配置
        if not self.api_key:
            raise ValueError('DIFY_API_KEY environment variable is required')
        if not self.app_id:
            raise ValueError('DIFY_APP_ID environment variable is required')
    
    def chat_completion(self, messages: List[Dict[str, Any]], user_id: str, stream: bool = False) -> Any:
        """调用Dify API进行聊天完成
        
        Args:
            messages: 消息列表，格式如 [{"role": "user", "content": "你好"}]
            user_id: 用户ID
            stream: 是否使用流式响应
            
        Returns:
            Dify API响应结果，如果是流式响应则返回响应对象
        """
        # 添加调试日志
        print(f"[DEBUG] Dify API Key: {self.api_key[:10]}...")
        print(f"[DEBUG] Dify App ID: {self.app_id}")
        print(f"[DEBUG] User ID: {user_id}")
        print(f"[DEBUG] Messages: {messages}")
        print(f"[DEBUG] Stream mode: {stream}")
        
        # 使用requests直接调用Dify API，不依赖SDK，这样可以确保使用正确的URL和参数
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Dify 1.11.2版本的API端点是 /v1/chat-messages
        api_url = "http://localhost:5001/v1/chat-messages"
        
        # 构建请求数据
        data = {
            "inputs": {},
            "query": messages[-1]['content'],
            "response_mode": "streaming" if stream else "blocking",
            "conversation_id": None,
            "user": user_id
        }
        
        print(f"[DEBUG] API URL: {api_url}")
        print(f"[DEBUG] Request data: {data}")
        
        # 直接调用Dify API，不做任何错误处理，让错误自然抛出
        response = requests.post(api_url, headers=headers, json=data, stream=stream)
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response headers: {dict(response.headers)}")
        
        # 先检查响应状态码
        response.raise_for_status()
        
        # 无论是否请求了流式响应，都返回响应对象，让调用者处理
        return response
    
    def get_chat_response_content(self, response: Dict[str, Any]) -> str:
        """从Dify API响应中提取聊天内容
        
        Args:
            response: Dify API响应结果
            
        Returns:
            聊天回复内容
        """
        return response.get('answer', '')
