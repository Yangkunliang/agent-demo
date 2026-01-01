# 测试Dify API集成
import os
import sys
from pathlib import Path

# 将项目根目录添加到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.services.dify_service import DifyService

# 加载.env文件
load_dotenv()

# 打印环境变量
print("环境变量：")
print(f"DIFY_API_KEY: {os.environ.get('DIFY_API_KEY')}")
print(f"DIFY_APP_ID: {os.environ.get('DIFY_APP_ID')}")
print(f"DIFY_API_URL: {os.environ.get('DIFY_API_URL')}")

# 测试DifyService初始化
try:
    dify_service = DifyService()
    print("\nDifyService初始化成功！")
    
    # 测试聊天完成
    try:
        messages = [{"role": "user", "content": "你好"}]
        response = dify_service.chat_completion(messages, "test_user")
        print("\nDify API调用成功！")
        print(f"响应内容：{response}")
        
        # 提取响应内容
        content = dify_service.get_chat_response_content(response)
        print(f"\n提取的响应内容：{content}")
    except Exception as e:
        print(f"\nDify API调用失败：{e}")
except Exception as e:
    print(f"\nDifyService初始化失败：{e}")