import yaml
import os
import re
from typing import Any, Dict
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


def replace_env_vars(value: Any) -> Any:
    """递归替换配置中的环境变量占位符"""
    if isinstance(value, str):
        # 替换 {{ENV_VAR}} 格式的环境变量占位符
        pattern = r'\{\{(\w+)\}\}'
        matches = re.findall(pattern, value)
        for match in matches:
            env_value = os.environ.get(match, f"{{{{{match}}}}}")
            value = value.replace(f"{{{{{match}}}}}", env_value)
        return value
    elif isinstance(value, dict):
        return {k: replace_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_env_vars(item) for item in value]
    else:
        return value


def load_config():
    """加载配置文件"""
    # 获取配置文件路径
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    
    with open(os.path.join(config_dir, 'intent_model.yml'), 'r', encoding='utf-8') as f:
        intent_model = yaml.safe_load(f)
    
    with open(os.path.join(config_dir, 'api_config.yml'), 'r', encoding='utf-8') as f:
        api_config = yaml.safe_load(f)
    
    with open(os.path.join(config_dir, 'agent_config.yml'), 'r', encoding='utf-8') as f:
        agent_config = yaml.safe_load(f)
    
    # 替换环境变量
    intent_model = replace_env_vars(intent_model)
    api_config = replace_env_vars(api_config)
    agent_config = replace_env_vars(agent_config)
    
    return intent_model, api_config, agent_config
