import yaml
import os


def load_config():
    """加载配置文件"""
    # 获取配置文件路径
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    
    with open(os.path.join(config_dir, 'intent_model.yml'), 'r', encoding='utf-8') as f:
        intent_model = yaml.safe_load(f)
    
    with open(os.path.join(config_dir, 'api_config.yml'), 'r', encoding='utf-8') as f:
        api_config = yaml.safe_load(f)
    
    return intent_model, api_config
