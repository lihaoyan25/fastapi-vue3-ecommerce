"""API v1路由汇总"""
from fastapi import APIRouter
from .routes import auth, products, cart, users

api_router = APIRouter()

# 注册认证路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
# 注册商品路由
api_router.include_router(products.router, prefix="/products", tags=["商品"])
# 注册购物车路由
api_router.include_router(cart.router, prefix="/cart", tags=["购物车"])
# 注册用户路由
api_router.include_router(users.router, prefix="/users", tags=["用户"])
