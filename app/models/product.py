""" 数据库商品模型 """
from sqlalchemy import Integer, String, DateTime, DECIMAL, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List
from app.database import Base
from decimal import Decimal

# CartItem模型中引用了Product模型, Product模型中又引用了CartItem模型, 导致循环引用, 故需要使用TYPE_CHECKING来避免循环引用
if TYPE_CHECKING:
    from app.models.cart import CartItem


class Product(Base):
    """商品模型"""
    __tablename__ = "products"

    # 主键
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="商品 ID")

    # 基本信息
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="商品名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="商品描述")
    price: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), nullable=False, comment="商品价格")
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="库存数量")
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="商品图片 URL")

    # 状态
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True, comment="是否上架")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")

    # 关联关系 - 购物车项
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Product(product_id={self.product_id}, name={self.name}, price={self.price})"