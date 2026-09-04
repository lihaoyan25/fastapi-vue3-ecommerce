"""用户数据访问层"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

class UserDAO:
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()

    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return db.query(User).filter(User.phone == phone).first()

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.user_id == user_id).first()