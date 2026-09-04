"""购物车业务服务"""
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.cart import CartItem
from app.models.product import Product
from app.dao.cart_dao import CartDAO
from app.services.product_service import ProductService
from app.services.user_service import UserService


class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.cart_dao = CartDAO()
        self.product_service = ProductService(db)
        self.user_service = UserService(db)

    def _build_cart_response(self, items: List[CartItem]):
        """构建购物车响应数据"""
        cart_items = []
        total_amount = Decimal("0.00")
        total_quantity = 0
        for item in items:
            product = item.product
            subtotal = product.price * item.quantity
            cart_items.append({
                "cart_item_id": item.cart_item_id,
                "product_id": product.product_id,
                "product_name": product.name,
                "product_price": product.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
                "created_at": item.created_at,
                "image_url": product.image_url
            })
            total_amount += subtotal
            total_quantity += item.quantity
        return {
            "items": cart_items,
            "total_amount": round(total_amount, 2),
            "total_quantity": total_quantity
        }

    def get_cart(self, user_id: int):
        """获取用户购物车"""
        items = self.cart_dao.get_by_user(self.db, user_id)
        return self._build_cart_response(items)

    def add_item(self, user_id: int, product_id: int, quantity: int):
        """添加商品到购物车"""
        # 校验商品是否存在且上架
        product = self.product_service.get_product(product_id, check_active=True)

        # 校验库存
        if not self.product_service.check_stock(product, quantity):
            raise HTTPException(status_code=400, detail="库存不足")
        # 检查购物车是否已有该商品
        existing = self.cart_dao.get_by_user_and_product(self.db, user_id, product_id)
        if existing:
            # 累加数量
            new_quantity = existing.quantity + quantity
            if not self.product_service.check_stock(product, new_quantity):
                raise HTTPException(status_code=400, detail="库存不足")
            existing.quantity = new_quantity
            self.db.commit()
            self.db.refresh(existing)
        else:
            # 新增购物车项
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            self.db.add(cart_item)
            self.db.commit()
            self.db.refresh(cart_item)
        return self.get_cart(user_id)

    def update_item_quantity(self, user_id: int, product_id: int, quantity: int):
        """更新购物车商品数量"""
        item = self.cart_dao.get_by_user_and_product(self.db, user_id, product_id)
        if not item:
            raise HTTPException(status_code=404, detail="购物车中不存在该商品")
        product = self.product_service.get_product(product_id, check_active=True)
        if not self.product_service.check_stock(product, quantity):
            raise HTTPException(status_code=400, detail="库存不足")
        item.quantity = quantity
        self.db.commit()
        self.db.refresh(item)
        return self.get_cart(user_id)

    def remove_item(self, user_id: int, product_id: int):
        """删除购物车商品"""
        self.cart_dao.delete_by_product(self.db, user_id, product_id)
        self.db.commit()
        return self.get_cart(user_id)

    def clear_cart(self, user_id: int):
        """清空购物车"""
        self.cart_dao.clear_by_user(self.db, user_id)
        self.db.commit()
        return self.get_cart(user_id)

    def checkout(self, user_id: int):
        """购物车结算（添加行锁防超卖）"""
        try:
            # 1. 获取购物车
            cart_items = self.cart_dao.get_by_user(self.db, user_id)
            if not cart_items:
                raise HTTPException(status_code=400, detail="购物车为空")

            # 2. 校验所有商品库存并计算总金额（仅预检，不加锁）
            total_amount = Decimal("0.00")
            for item in cart_items:
                product = self.product_service.get_product(item.product_id, check_active=True)
                if not self.product_service.check_stock(product, item.quantity):
                    raise HTTPException(
                        status_code=400,
                        detail=f"商品【{product.name}】库存不足"
                    )
                total_amount += product.price * item.quantity
            total_amount = round(total_amount, 2)

            # 3. 校验用户余额
            user = self.user_service.get_user_by_id(user_id)
            if user.balance < total_amount:
                raise HTTPException(status_code=400, detail="账户余额不足")

            # 4. 扣减库存，with_for_update() 添加数据库行锁，防止并发超卖
            for item in cart_items:
                # 锁定商品行，其他事务必须等本次提交完成后才能修改
                stmt = select(Product).where(Product.product_id == item.product_id).with_for_update()
                # populate_existing 强制用数据库最新值刷新实例，避免沿用步骤2预检时的过期快照
                product = self.db.execute(
                    stmt.execution_options(populate_existing=True)
                ).scalar_one()
                # 加锁后二次校验库存（非常关键！预检后库存有可能被别人改掉）
                if product.stock < item.quantity:
                    raise HTTPException(status_code=400, detail=f"商品【{product.name}】库存不足")
                product.stock -= item.quantity

            # 5. 扣减用户余额
            user.balance -= total_amount

            # 6. 清空购物车
            self.cart_dao.clear_by_user(self.db, user_id)

            # 7. 一次性提交全部修改，事务生效
            self.db.commit()

            return {
                "success": True,
                "total_amount": total_amount,
                "message": "结算成功"
            }

        except Exception as e:
            # 任何异常都回滚事务
            self.db.rollback()
            raise e
