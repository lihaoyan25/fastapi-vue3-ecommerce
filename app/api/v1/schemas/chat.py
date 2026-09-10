"""客服Schema"""
from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChatContext(BaseModel):
    """用户随消息发送的卡片上下文"""
    type: Literal["product", "order"] = Field(..., description="卡片类型: product=商品, order=订单")
    id: int = Field(..., ge=1, description="商品/订单 ID")


class ChatSendRequest(BaseModel):
    """发送消息请求"""
    content: str = Field(..., min_length=1, max_length=2000, description="消息内容")
    context: Optional[ChatContext] = Field(None, description="可选的卡片上下文")
