""" 数据库购物车项模型 """
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class CartItem(Base):
    """购物车项模型"""
    __tablename__ = "cart_items"

    # 主键
    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="购物车项ID")

    # 外键 - 关联用户
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True, comment="用户 ID")

    # 外键 - 关联商品
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False, index=True, comment="商品 ID")

    # 购买数量
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="购买数量")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")

    # 关联关系 - 用户 & 商品
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self) -> str:
        return f"CartItem(cart_item_id={self.cart_item_id}, user_id={self.user_id}, quantity={self.quantity})"