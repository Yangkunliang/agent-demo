from typing import List, Dict, Any
from src.utils.mock_data import mock_service_notes


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
