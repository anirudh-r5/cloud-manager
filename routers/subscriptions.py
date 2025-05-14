from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from database import get_db
from bson import ObjectId
from datetime import datetime

router = APIRouter()

class SubscriptionInput(BaseModel):
    user_id: str = Field(..., description="User identifier")
    plan_id: str = Field(..., description="Plan ID user is subscribing to")

@router.post("/")
async def subscribe_user(subscription: SubscriptionInput, db=Depends(get_db)):
    # Ensure plan exists
    plan = await db.plans.find_one({"_id": ObjectId(subscription.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    sub_doc = {
        "user_id": subscription.user_id,
        "plan_id": ObjectId(subscription.plan_id)
    }

    # Upsert the subscription (one per user)
    await db.subscriptions.replace_one(
        {"user_id": subscription.user_id},
        sub_doc,
        upsert=True
    )
    return {"message": f"User {subscription.user_id} subscribed to plan '{plan['name']}'"}

@router.get("/{user_id}")
async def get_user_subscription(user_id: str, db=Depends(get_db)):
    subscription = await db.subscriptions.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    plan = await db.plans.find_one({"_id": subscription["plan_id"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    usage_summary = []
    limits = plan.get("limits", {})

    for service, limit in limits.items():
        usage_doc = await db.usages.find_one({"user_id": user_id, "service": service})
        count = usage_doc["count"] if usage_doc else 0
        usage_summary.append({
            "service": service,
            "used": count,
            "limit": limit,
            "remaining": max(0, limit - count)
        })

    return {
        "user_id": user_id,
        "plan_name": plan["name"],
        "plan_id": str(subscription["plan_id"]),
        "usage": usage_summary
    }


@router.put("/{user_id}")
async def change_user_plan(user_id: str, new_plan: SubscriptionInput, db=Depends(get_db)):
    # Validate new plan
    plan = await db.plans.find_one({"_id": ObjectId(new_plan.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    result = await db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": {
            "plan_id": ObjectId(new_plan.plan_id),
            "subscribed_at": datetime.now()
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"message": f"User {user_id} switched to plan '{plan['name']}'"}
