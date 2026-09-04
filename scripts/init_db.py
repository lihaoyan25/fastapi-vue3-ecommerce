import sys
from pathlib import Path
from decimal import Decimal
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        # 幂等校验：已存在则不重复创建
        admin = db.query(User).filter(User.role == "admin").first()
        if admin:
            print(f"管理员账号已存在：{admin.username}")
            return
        
        admin = User(
            username="admin",
            hashed_password=hash_password("admin123"),
            email="admin@example.com",
            phone=None,
            balance=Decimal("0"),
            status=1,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("管理员账号创建成功")
        print("   用户名: admin")
        print("   密码: admin123")
        print("请登录后尽快修改密码")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
