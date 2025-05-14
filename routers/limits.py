from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_db

router = APIRouter()

@router.post("/{user_id}")
async def track_usage(user_id: str, service: str = Query(...), db=Depends(get_db)):
    usage = await db.usages.find_one({"user_id": user_id, "service": service})
    if usage:
        await db.usages.update_one(
            {"user_id": user_id, "service": service},
            {"$inc": {"count": 1}}
        )
    else:
        await db.usages.insert_one({"user_id": user_id, "service": service, "count": 1})
    return {"message": f"Logged usage for {service}"}

@router.get("/{user_id}/limit")
async def check_limit(user_id: str, service: str = Query(...), db=Depends(get_db)):
    # Get user subscription
    sub = await db.subscriptions.find_one({"user_id": user_id})
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")

    # Get plan
    plan = await db.plans.find_one({"_id": sub["plan_id"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    limit = plan.get("limits", {}).get(service, 0)
    usage = await db.usages.find_one({"user_id": user_id, "service": service})
    count = usage["count"] if usage else 0

    return {"limit_reached": count >= limit}

@router.post("/{user_id}/reset")
async def reset_usage(user_id: str, service: str, db=Depends(get_db)):
    result = await db.usages.update_one(
        {"user_id": user_id, "service": service},
        {"$set": {"count": 0}}
    )
    if result.matched_count == 0:
        return {"message": f"No usage found for {service}"}
    return {"message": f"Usage reset for {service}"}