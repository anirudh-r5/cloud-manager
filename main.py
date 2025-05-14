from typing import Annotated
from fastapi import Cookie, Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import connect_to_mongo, get_db
from routers import plans, permissions, subscriptions, rbac, limits, auth
from routers.auth import require_role
from routers.rbac import check_access
from routers.limits import check_limit, track_usage

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ready the DB instance
    await connect_to_mongo()
    yield

async def enforce_service_access(service: str, username: str, db):
    if not username:
        raise HTTPException(status_code=401, detail="Login required")

    allowed = await check_access(user_id=username, service=service, db=db)
    if not allowed:
        raise HTTPException(status_code=403, detail=f"No access to {service}")

    limit = await check_limit(user_id=username, service=service, db=db)
    if limit["limit_reached"]:
        raise HTTPException(status_code=403, detail=f"Limit reached for {service}")

    await track_usage(user_id=username, service=service, db=db)

app = FastAPI(title="Cloud Manager", lifespan=lifespan)

app.include_router(plans.router, prefix="/plans", tags=["Plans"], dependencies=[Depends(require_role('admin'))])
app.include_router(permissions.router, prefix="/permissions", tags=["Permissions"], dependencies=[Depends(require_role('admin'))])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(rbac.router, prefix="/access", tags=["Access"])
app.include_router(limits.router, prefix="/usage", tags=["Usage"])
app.include_router(auth.router, prefix="/auth", tags=["Authorization"])

@app.get("/")
async def home(username: Annotated[str | None, Cookie()] = None):
    return {"user": username}

@app.get("/compute")
async def compute(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('compute',username,db)
    return {"message": "Accessed compute service"}

@app.get("/storage")
async def storage(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('storage',username, db)
    return {"message": "Accessed storage service"}

@app.get("/container")
async def container(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('container',username, db)
    return {"message": "Accessed container service"}

@app.get("/db")
async def db(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('db',username, db)
    return {"message": "Accessed database service"}

@app.get("/app")
async def caching(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('app',username, db)
    return {"message": "Accessed app service"}

@app.get("/ai")
async def ai(username: Annotated[str | None, Cookie()] = None, db=Depends(get_db)):
    await enforce_service_access('ai',username, db)
    return {"message": "Accessed AI model service"}