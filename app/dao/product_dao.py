"""商品数据访问层"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.product import Product

class ProductDAO:
    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        """根据ID获取商品"""
        return db.query(Product).filter(Product.product_id == product_id).first()

    def get_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Product]:
        """获取商品列表"""
        query = db.query(Product)
        if only_active:
            query = query.filter(Product.is_active == True)
        return query.offset(skip).limit(limit).all()

    def count(self, db: Session, only_active: bool = True) -> int:
        """统计商品数量"""
        query = db.query(Product)
        if only_active:
            query = query.filter(Product.is_active == True)
        return query.count()

    def search(
        self,
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Product]:
        """搜索商品"""
        query = db.query(Product).filter(Product.name.ilike(f"%{keyword}%"))
        if only_active:
            query = query.filter(Product.is_active == True)
        return query.offset(skip).limit(limit).all()

    def search_count(self, db: Session, keyword: str, only_active: bool = True) -> int:
        """搜索商品数量"""
        query = db.query(Product).filter(Product.name.ilike(f"%{keyword}%"))
        if only_active:
            query = query.filter(Product.is_active == True)
        return query.count()