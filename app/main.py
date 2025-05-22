from .controllers.auth.auth import router as router_auth
from fastapi import FastAPI

app = FastAPI()
app.include_router(router_auth, prefix="/auth", tags=["Auth"])
