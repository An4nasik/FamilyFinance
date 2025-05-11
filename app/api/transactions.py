from fastapi import APIRouter, HTTPException
from typing import List
from app.services.transaction_service import TransactionService
from app.schemas.transaction import PurchaseCreate, TopUpCreate, OperationRead

router = APIRouter(prefix="/families/{family_id}", tags=["Transactions"])
service = TransactionService()

@router.get("/transactions", response_model=List[OperationRead])
async def list_ops(family_id: str):
    return await service.list(family_id)

@router.post("/purchases", status_code=201)
async def add_purchase(family_id: str, data: PurchaseCreate):
    return await service.purchase(family_id, data)  # Передаем family_id и data

@router.post("/topups", status_code=201)
async def add_topup(family_id: str, data: TopUpCreate):
    return await service.topup(data)

@router.delete("/transactions/{op_id}")
async def delete_op(family_id: str, op_id: str):
    ok = await service.remove(op_id)
    if not ok:
        raise HTTPException(404, "Operation not found")
    return {"status": "success"}