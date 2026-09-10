"""购物车路由"""
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.services.cart_service import CartService
from app.api.v1.schemas.cart import CartItemCreate, CartItemUpdate
from app.api.v1.schemas.common import success_response
from app.models.user import User

router = APIRouter()


@router.get("")
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """查看购物车"""
    cart_service = CartService(db)
    data = await run_in_threadpool(cart_service.get_cart, current_user.user_id)
    return success_response(data=data)


@router.post("/items")
async def add_to_cart(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """添加商品到购物车"""
    cart_service = CartService(db)
    data = await run_in_threadpool(
        cart_service.add_item,
        current_user.user_id,
        item_in.product_id,
        item_in.quantity,
    )
    return success_response(data=data)


@router.put("/items/{product_id}")
async def update_cart_item(
    product_id: int,
    item_in: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新购物车商品数量"""
    cart_service = CartService(db)
    data = await run_in_threadpool(
        cart_service.update_item_quantity,
        current_user.user_id,
        product_id,
        item_in.quantity,
    )
    return success_response(data=data)


@router.delete("/items/{product_id}")
async def remove_from_cart(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除购物车商品"""
    cart_service = CartService(db)
    data = await run_in_threadpool(
        cart_service.remove_item,
        current_user.user_id,
        product_id,
    )
    return success_response(data=data)


@router.delete("/clear")
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """清空购物车"""
    cart_service = CartService(db)
    data = await run_in_threadpool(cart_service.clear_cart, current_user.user_id)
    return success_response(data=data)
