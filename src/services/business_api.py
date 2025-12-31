from typing import Dict, Any
from src.utils.mock_data import mock_orders


def call_business_api(api_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """模拟调用业务API"""
    if api_name == "get_orders":
        return mock_orders
    elif api_name == "check_order_modify":
        return {
            "can_modify": True,
            "message": "该订单可以修改，周六有空位",
            "available_slots": ["2023-11-02 14:00:00", "2023-11-02 15:00:00"]
        }
    elif api_name == "update_order":
        for order in mock_orders:
            if order["order_id"] == params["order_id"]:
                order["service_time"] = params["service_time"]
                return {
                    "success": True,
                    "message": "订单修改成功",
                    "order": order
                }
        return {
            "success": False,
            "message": "订单不存在"
        }
    elif api_name == "cancel_order":
        for i, order in enumerate(mock_orders):
            if order["order_id"] == params["order_id"]:
                mock_orders.pop(i)
                return {
                    "success": True,
                    "message": "订单取消成功"
                }
        return {
            "success": False,
            "message": "订单不存在"
        }
    else:
        return {"error": "API不存在"}
