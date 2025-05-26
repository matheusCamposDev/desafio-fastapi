from .controllers.auth.auth import router as router_auth
from .controllers.clients.client import router as router_client
from .controllers.products.product import router as router_products
from fastapi import FastAPI

app = FastAPI()
app.include_router(router_auth, prefix="/auth", tags=["Auth"])
app.include_router(router_client, tags=["Clientes"])
app.include_router(router_products, tags=["Products"])
