from .controllers.auth.auth import router as router_auth
from .controllers.clients.client import router as router_client
from .controllers.products.product import router as router_products
from .controllers.orders.order import router as router_orders
from fastapi import FastAPI

app = FastAPI()
app.include_router(router_auth, prefix="/auth", tags=["Auth"])
app.include_router(router_client, tags=["Clientes"])
app.include_router(router_products, tags=["Products"])
app.include_router(router_orders, tags=["Orders"])
