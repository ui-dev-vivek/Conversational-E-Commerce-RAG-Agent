from fastapi import APIRouter

router = APIRouter()

_SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Red T-Shirt", "price": 399, "color": "red"},
    {"id": 2, "name": "Blue Jeans", "price": 1299, "color": "blue"},
]


@router.get("/")
async def list_products(q: str | None = None):
    if not q:
        return _SAMPLE_PRODUCTS
    q_lower = q.lower()
    return [p for p in _SAMPLE_PRODUCTS if q_lower in p["name"].lower()]
