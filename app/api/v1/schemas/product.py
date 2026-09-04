"""商品Schema"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    description: Optional[str] = Field(None, max_length=1000, description="商品描述")
    price: Decimal = Field(..., gt=0, description="商品价格")
    stock: int = Field(..., ge=0, le=999999, description="库存数量")
    image_url: Optional[str] = Field(None, max_length=255, description="商品图片")

class ProductCreate(ProductBase):
    """创建商品请求"""
    pass

class ProductUpdate(BaseModel):
    """更新商品请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0, le=999999)
    image_url: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ProductListResponse(BaseModel):
    """商品列表响应"""
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
