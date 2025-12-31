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
