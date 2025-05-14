from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from bson import ObjectId

router = APIRouter()

@router.get("/{user_id}/{service}")
async def check_access(user_id: str, service: str, db=Depends(get_db)):
    # 1. Get subscription
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="User has no subscription")

    # 2. Get plan
    plan = await db.plans.find_one({"_id": sub["plan_id"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # 3. Check if service is allowed
    if service not in plan.get("permissions", []):
        return False
    else:
        return True
