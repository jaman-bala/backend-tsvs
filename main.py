import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
# from starlette_exporter import handle_metrics
# from starlette_exporter import PrometheusMiddleware
# from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import set
from backend.src.account.user.api import user_router
from backend.src.account.user.login_handler import login_router
from backend.src.regions.router import router as region_router
from backend.src.departments.router import router as departments_router

#########################
# BLOCK WITH API ROUTES #
#########################

app = FastAPI(
    title=set.PROJECT_NAME,
    version=set.PROJECT_VERSION
)
app.mount("/static", StaticFiles(directory="static"), name="static")


# origins = [
#     "http://localhost:3000",  # React app
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# )
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance


@main_api_router.get("/")
async def ping():
    return {"Success": "Салам алейкум на backend🚀"}

main_api_router.include_router(
    region_router,
    prefix="/api",
    tags=["REGIONS"]
)

main_api_router.include_router(
    departments_router,
    prefix="/api",
    tags=["DEPARTMENTS"]
)


main_api_router.include_router(
    user_router,
    prefix="/api",
    tags=["USER"]
)

main_api_router.include_router(
    login_router,
    prefix="/api",
    tags=["LOGIN"]
)


app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="127.0.0.1", port=8000)
