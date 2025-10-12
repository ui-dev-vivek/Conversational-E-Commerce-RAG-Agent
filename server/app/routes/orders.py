from fastapi import APIRouter, HTTPException

router = APIRouter()

_SAMPLE_ORDERS = [
    {"order_id": "ord_001", "status": "shipped", "items": [1, 2]},
]


@router.get("/{order_id}")
async def get_order(order_id: str):
    for o in _SAMPLE_ORDERS:
        if o["order_id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="Order not found")


@router.post("/")
async def create_order(item_ids: list[int]):
    # naive creation
    new = {"order_id": f"ord_{len(_SAMPLE_ORDERS)+1:03d}", "status": "processing", "items": item_ids}
    _SAMPLE_ORDERS.append(new)
    return new
