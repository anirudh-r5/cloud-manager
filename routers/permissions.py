from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from database import get_db

router = APIRouter()

class PermissionInput(BaseModel):
    name: str = Field(..., description="Label for the permission (e.g., AI)")
    endpoint: str = Field(..., description="API endpoint this permission controls (e.g., /ai)")
    description: str = Field(..., description="Description of what this permission grants access to")

@router.post("/")
async def create_permission(permission: PermissionInput, db=Depends(get_db)):
    existing = await db.permissions.find_one({"name": permission.name})
    if existing:
        raise HTTPException(status_code=400, detail="Permission with this name already exists")
    result = await db.permissions.insert_one(permission.model_dump())
    if result:
        return "Created new permission"
    raise HTTPException(status_code=500)

@router.get("/")
async def list_permissions(db=Depends(get_db)):
    permissions = await db.permissions.find().to_list(100)
    for permission in permissions:
        permission["_id"] = str(permission["_id"])
    return permissions

@router.put("/{name}")
async def update_permission(name: str, updated: PermissionInput, db=Depends(get_db)):
    result = await db.permissions.update_one(
        {"name": name},
        {"$set": updated.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")

    updated_doc = await db.permissions.find_one({"name": updated.name})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc

@router.delete("/{name}")
async def delete_permission(name: str, db=Depends(get_db)):
    result = await db.permissions.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": f"Permission '{name}' deleted"}
