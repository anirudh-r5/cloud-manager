from fastapi import APIRouter, Response, Request, HTTPException, Form, Depends
from database import get_db

router = APIRouter()

@router.post("/register")
async def register(username: str = Form(...), role: str = Form(...), db=Depends(get_db)):
    existing = await db.users.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if role not in ["admin", "customer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'admin' or 'customer'")
    
    await db.users.insert_one({"username": username, "role": role})
    return {"message": f"User '{username}' registered with role '{role}'"}

@router.post("/login")
async def login(response: Response, username: str = Form(...), role: str = Form(...), db=Depends(get_db)):
    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.get("role") != role:
        raise HTTPException(status_code=403, detail="Role mismatch")
    response.set_cookie("username", username, httponly=True)
    return {"message": "Logged in"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("username")
    return {"message": "Logged out"}

async def get_current_user(request: Request, db=Depends(get_db)):
    username = request.cookies.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="Not logged in")
    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

def require_role(role: str):
    async def verify_role(user=Depends(get_current_user)):
        user_role = user.get("role")
        if user_role != role:
            raise HTTPException(status_code=403, detail=f"Unauthorized Access. Current Role: '{role}'")
        return user
    return verify_role
