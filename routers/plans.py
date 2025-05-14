from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from database import get_db
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

router = APIRouter()

class PlanInput(BaseModel):
    name: str = Field(..., description="Unique name of the plan")
    description: str = Field(..., description="Description of the plan")
    limits: Dict[str, int] = Field(default_factory=dict, description="Service usage limits")
    permissions: list[str] = Field(default_factory=list, description="List of allowed services")

@router.post("/")
async def create_plan(plan: PlanInput, db=Depends(get_db)):
    existing = await db.plans.find_one({"name": plan.name})
    if existing:
        raise HTTPException(status_code=400, detail="Plan already exists")
    plan_doc = plan.model_dump()
    result = await db.plans.insert_one(plan_doc)
    if result:
        return 'Created new plan!'
    raise HTTPException(status_code=500, detail="Insertion error")

@router.get("/")
async def list_plans(db=Depends(get_db)):
    plans = await db.plans.find().to_list(100)
    for plan in plans: 
        plan["_id"] = str(plan["_id"])
    return plans

@router.get("/{plan_id}")
async def get_plan(plan_id: str, db=Depends(get_db)):
    plan = await db.plans.find_one({"_id": ObjectId(plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan["_id"] = str(plan["_id"])
    return plan

@router.put("/{plan_id}")
async def update_plan(plan_id: str, plan: PlanInput, db=Depends(get_db)):
    update_data = jsonable_encoder(plan)
    result = await db.plans.update_one(
        {"_id": ObjectId(plan_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    updated_plan = await db.plans.find_one({"_id": ObjectId(plan_id)})
    updated_plan["_id"] = str(updated_plan["_id"])
    return updated_plan

@router.delete("/{plan_id}")
async def delete_plan(plan_id: str, db=Depends(get_db)):
    result = await db.plans.delete_one({"_id": ObjectId(plan_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan deleted"}