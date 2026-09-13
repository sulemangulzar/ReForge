from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.profile import router as profile_router
from app.api.v1.routes.goal import router as goal_router

app = FastAPI(
    title="ReForge",
    description="A Health Tracking App.",
    version="0.1.0"
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(profile_router, tags=["profile"])
app.include_router(goal_router, tags=["goals"])

@app.get("/")
def health():
    return {"message" : "Running"}


@app.get("/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

