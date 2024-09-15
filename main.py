import uvicorn

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import set, BASE_DIR, STATIC_FILES_DIR
from backend.src.account.user.api import user_router
from backend.src.account.user.admin_privilege import admin_router
from backend.src.account.user.login_handler import login_router
from backend.src.account.face.router import router as face_router

from backend.src.regions.router import router as region_router
from backend.src.departments.router import router as departments_router
from backend.src.ekzamens.router import router as ezamens_router
from backend.src.chat.router import router as chat_router


#########################
# BLOCK WITH API ROUTES #
#########################

app = FastAPI(
    title=set.PROJECT_NAME,
    version=set.PROJECT_VERSION
)

static_dir = STATIC_FILES_DIR
if not static_dir.exists():
    static_dir.mkdir(parents=True)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)
app.mount(
    "/static",
    StaticFiles(directory=static_dir),
    name="static",
)

origins = [
    "http://localhost:3000",  # React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

main_api_router = APIRouter()


@main_api_router.get("/")
async def ping():
    return FileResponse("static/404/404.jpg")

main_api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["CHAT"]
)

main_api_router.include_router(
    region_router,
    prefix="/regions",
    tags=["REGIONS"]
)

main_api_router.include_router(
    departments_router,
    prefix="/departments",
    tags=["DEPARTMENTS"]
)

main_api_router.include_router(
    ezamens_router,
    prefix="/exam",
    tags=["EKZAMEN"]
)


main_api_router.include_router(
    user_router,
    prefix="/users",
    tags=["USER"]
)

main_api_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["ADMIN-PRIVILEGES"]
)

main_api_router.include_router(
    login_router,
    prefix="/api",
    tags=["LOGIN"]
)

main_api_router.include_router(
    face_router,
    prefix="/api",
    tags=["FACE LOGIN"]
)


app.include_router(main_api_router)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="127.0.0.1", port=8001)
