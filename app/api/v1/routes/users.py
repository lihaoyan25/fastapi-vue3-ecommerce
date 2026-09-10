"""用户路由"""
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.services.user_service import UserService
from app.api.v1.schemas.user import (
    UserResponse, UserUpdate, UserPasswordUpdate, RechargeRequest
)
from app.api.v1.schemas.common import success_response
from app.models.user import User

router = APIRouter()


@router.put("/me")
async def update_my_info(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新当前用户信息"""
    user_service = UserService(db)
    user = await run_in_threadpool(
        user_service.update_my_info,
        current_user.user_id,
        user_in.username,
        user_in.email,
        user_in.phone,
        user_in.current_password,
    )
    return success_response(data=UserResponse.model_validate(user).model_dump())


@router.put("/me/password")
async def change_password(
    password_in: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """修改密码"""
    user_service = UserService(db)
    await run_in_threadpool(
        user_service.change_password,
        current_user.user_id,
        password_in.old_password,
        password_in.new_password,
    )
    return success_response(message="密码修改成功")


@router.get("/me/balance")
async def get_balance(
    current_user: User = Depends(get_current_user),
):
    """查询账户余额"""
    return success_response(data={"balance": current_user.balance, "currency": "CNY"})


@router.post("/me/recharge")
async def recharge(
    recharge_in: RechargeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """账户充值"""
    user_service = UserService(db)
    user = await run_in_threadpool(
        user_service.recharge,
        current_user.user_id,
        recharge_in.amount,
    )
    return success_response(data={"balance": user.balance, "currency": "CNY"})
