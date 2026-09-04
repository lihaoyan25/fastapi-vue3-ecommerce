""" 数据库用户模型 """
from sqlalchemy import Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List
from app.database import Base
from decimal import Decimal

# CartItem模型中引用了User模型, User模型中又引用了CartItem模型, 导致循环引用, 故需要使用TYPE_CHECKING来避免循环引用
if TYPE_CHECKING:
    from app.models.cart import CartItem

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    # 主键
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户 ID")

    # 基本信息
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="哈希后的密码")
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True, comment="邮箱")
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, index=True, comment="手机号")

    # 账户信息
    balance: Mapped[Decimal] = mapped_column(DECIMAL(14, 2), default=0.0, nullable=False, comment="账户余额")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="用户状态: 1=正常, 2=封禁, 3=注销")
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False, comment="用户角色: user=普通用户, admin=管理员")

    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")

    # 关联关系 - 与购物车项中的用户关联
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

    # __repr__方法: 用于在调试时打印对象的字符串表示, 方便查看对象属性, 例如: User(user_id=1, username=admin)
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, username={self.username})"