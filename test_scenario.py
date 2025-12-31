#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
好慷智能体场景测试脚本
模拟三个核心场景的交互流程
"""

import yaml
import json

# 加载配置文件
def load_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 模拟智能体响应
def simulate_agent_response(scenario, user_input):
    """模拟智能体对用户输入的响应"""
    print(f"\n=== {scenario} ===")
    print(f"用户: {user_input}")
    
    # 加载配置
    intent_model = load_config('intent_model.yml')
    agent_config = load_config('agent_config.yml')
    
    # 模拟意图识别
    print(f"智能体: 正在识别意图...")
    
    # 模拟不同场景的响应
    if scenario == "场景一：查询服务笔记":
        print(f"智能体: 正在查询您的服务笔记...")
        print(f"智能体: 找到以下相关服务笔记：")
        print(f"- 服务日期: 2023-10-15")
        print(f"  服务人员: 张阿姨")
        print(f"  笔记内容: 本次服务完成了客厅、卧室的清洁，客户对服务质量满意...")
        print(f"  详情: [查看详情](note_123)")
        print(f"- 服务日期: 2023-10-01")
        print(f"  服务人员: 李阿姨")
        print(f"  笔记内容: 本次服务完成了厨房、卫生间的深度清洁，客户提出了一些建议...")
        print(f"  详情: [查看详情](note_124)")
        print(f"\n[查看详情] [返回]")
    
    elif scenario == "场景二：查询订单":
        print(f"智能体: 正在查询您的订单...")
        print(f"智能体: 为您找到以下订单：")
        print(f"- 订单ID：order_123")
        print(f"  服务时间：2023-11-01 14:00:00")
        print(f"  服务类型：深度清洁")
        print(f"  服务人员：张阿姨")
        print(f"  状态：已确认")
        print(f"- 订单ID：order_124")
        print(f"  服务时间：2023-11-08 14:00:00")
        print(f"  服务类型：日常保洁")
        print(f"  服务人员：李阿姨")
        print(f"  状态：已确认")
        print(f"\n您可以说\"修改订单\"或\"取消订单\"来管理您的订单。")
    
    elif scenario == "场景三：修改订单" and "修改订单" in user_input:
        print(f"智能体: 正在检查订单可修改性...")
        print(f"智能体: 我已为您查询到订单状态：")
        print(f"该订单可以修改，周六有空位。")
        print(f"\n您是否确认将订单order_123修改为2023-11-02 14:00？")
        print(f"[确认修改] [取消操作]")
    
    elif scenario == "场景三：修改订单" and "确认修改" in user_input:
        print(f"智能体: 正在修改订单...")
        print(f"智能体: 订单修改成功！新的服务时间为：2023-11-02 14:00:00")
    
    elif scenario == "场景三：取消订单" and "取消订单" in user_input:
        print(f"智能体: 您确定要取消订单order_124吗？")
        print(f"取消后可能会产生相应的费用，请您确认。")
        print(f"[确认取消] [取消操作]")
    
    elif scenario == "场景三：取消订单" and "确认取消" in user_input:
        print(f"智能体: 正在取消订单...")
        print(f"智能体: 订单取消成功！")
    
    else:
        print(f"智能体: 抱歉，我不太明白您的意思。请您换一种方式提问。")
    
    print("=" * 50)

# 测试三个场景
def test_scenarios():
    """测试三个核心场景"""
    print("好慷智能体场景测试")
    print("=" * 50)
    
    # 场景一：查询服务笔记
    simulate_agent_response("场景一：查询服务笔记", "上次服务的笔记是什么？")
    
    # 场景二：查询订单
    simulate_agent_response("场景二：查询订单", "我有哪些订单？")
    
    # 场景三：修改订单
    simulate_agent_response("场景三：修改订单", "我想修改订单order_123的时间为2023-11-02 14:00")
    simulate_agent_response("场景三：修改订单", "确认修改")
    
    # 场景三：取消订单
    simulate_agent_response("场景三：取消订单", "我想取消订单order_124")
    simulate_agent_response("场景三：取消订单", "确认取消")
    
    print("\n所有场景测试完成！")

# 验证配置文件完整性
def validate_configs():
    """验证配置文件的完整性"""
    print("\n验证配置文件完整性...")
    
    try:
        # 加载所有配置文件
        configs = [
            ('intent_model.yml', '意图识别模型'),
            ('api_config.yml', 'API和知识库配置'),
            ('confirmation_config.yml', '二次确认配置'),
            ('agent_config.yml', 'Agent完整配置')
        ]
        
        for config_file, description in configs:
            config = load_config(config_file)
            print(f"✓ {description} 加载成功")
        
        print("\n所有配置文件验证通过！")
        return True
    except Exception as e:
        print(f"✗ 配置文件验证失败: {e}")
        return False

if __name__ == "__main__":
    # 验证配置文件
    if validate_configs():
        # 运行场景测试
        test_scenarios()
    else:
        print("配置文件验证失败，无法运行测试")
