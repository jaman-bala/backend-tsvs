from fastapi import APIRouter

service_router = login_router = APIRouter()


@service_router.get("/ping")
async def ping():
    return {"Success": "Салам алейкум на backend🚀"}
