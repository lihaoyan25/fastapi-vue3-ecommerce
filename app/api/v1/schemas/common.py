"""通用响应模型与辅助函数"""
from typing import Any
from pydantic import BaseModel


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str


def success_response(data: Any = None, message: str = "success") -> dict:
    """构造统一成功响应 {code, message, data}"""
    return {"code": 200, "message": message, "data": data}
