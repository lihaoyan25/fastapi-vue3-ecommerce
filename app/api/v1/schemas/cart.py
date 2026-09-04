"""购物车Schema"""
from pydantic import BaseModel, Field

class CartItemCreate(BaseModel):
    """添加购物车请求"""
    product_id: int = Field(..., gt=0, description="商品ID")
    quantity: int = Field(..., ge=1, le=9999, description="购买数量")

class CartItemUpdate(BaseModel):
    """更新购物车数量请求"""
    quantity: int = Field(..., ge=1, le=9999, description="购买数量")
