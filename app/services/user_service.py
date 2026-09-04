"""用户业务服务"""
from typing import Tuple
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.dao.user_dao import UserDAO
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_dao = UserDAO()

    def register(
        self,
        username: str,
        password: str,
        email: str,
        phone: str | None = None,
    ) -> User:
        """用户注册"""
        # 业务校验: 用户名是否存在
        if self.user_dao.get_by_username(self.db, username):
            raise HTTPException(status_code=400, detail="用户名已存在")
        # 业务校验: 邮箱是否已注册
        if self.user_dao.get_by_email(self.db, email):
            raise HTTPException(status_code=400, detail="邮箱已注册")
        # 业务校验: 手机号是否已注册
        if phone and self.user_dao.get_by_phone(self.db, phone):
            raise HTTPException(status_code=400, detail="手机号已注册")

        # 创建用户 (默认赠送1000元体验金)
        user = User(
            username=username,
            hashed_password=hash_password(password),
            email=email,
            phone=phone,
            balance=Decimal("1000.00"),
            status=1,
            role="user"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, username: str, password: str) -> Tuple[str, str]:
        """用户登录，返回(access_token, refresh_token)"""
        user = self.user_dao.get_by_username(self.db, username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if user.status != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账号已被封禁或注销"
            )

        access_token = create_access_token(
            subject=user.user_id,
            extra_claims={"username": user.username},
        )
        refresh_token = create_refresh_token(subject=user.user_id)
        return access_token, refresh_token

    def get_user_by_id(self, user_id: int) -> User:
        """根据ID获取用户"""
        user = self.user_dao.get_by_id(self.db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user

    def recharge(self, user_id: int, amount: Decimal) -> User:
        """账户充值"""
        if amount <= 0:
            raise HTTPException(status_code=400, detail="充值金额必须大于0")
        user = self.get_user_by_id(user_id)
        user.balance += amount
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_my_info(
        self,
        user_id: int,
        email: str | None = None,
        phone: str | None = None,
    ) -> User:
        """更新当前用户信息"""
        user = self.get_user_by_id(user_id)
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        self.db.commit()
        self.db.refresh(user)
        return user

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> User:
        """修改密码"""
        user = self.get_user_by_id(user_id)
        if not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="原密码错误")
        user.hashed_password = hash_password(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user
