"""商品查询工具"""
from app.tools.registry import register_tool
from app.services.product_service import ProductService


@register_tool(
    name="search_products",
    description="按关键词搜索在售商品（分页），返回商品名称、价格、库存等信息",
    display="正在搜索商品",
    parameters={
        "type": "object",
        "properties": {
            "keyword": {"type": "string", "description": "搜索关键词，匹配商品名称"},
            "page": {"type": "integer", "description": "页码，默认 1"},
            "page_size": {"type": "integer", "description": "每页数量，默认 10，最大 20"},
        },
        "required": ["keyword"],
    },
)
def search_products(db, user_id: int, args: dict) -> dict:
    service = ProductService(db)
    page = min(max(int(args.get("page", 1)), 1), 100)
    page_size = min(max(int(args.get("page_size", 10)), 1), 20)
    products, total = service.search_products(
        keyword=args["keyword"],
        page=page,
        page_size=page_size,
        only_active=True,
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
                "image_url": p.image_url,
                "description": (p.description or "")[:100],
            }
            for p in products
        ],
    }


@register_tool(
    name="query_product_detail",
    description="查询指定商品的详情（名称、价格、库存、描述），仅限在售商品",
    display="正在查询商品详情",
    parameters={
        "type": "object",
        "properties": {
            "product_id": {"type": "integer", "description": "商品 ID"},
        },
        "required": ["product_id"],
    },
)
def query_product_detail(db, user_id: int, args: dict) -> dict:
    product = ProductService(db).get_product(int(args["product_id"]), check_active=True)
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "description": product.description,
    }
