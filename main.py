import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
# from starlette_exporter import handle_metrics
# from starlette_exporter import PrometheusMiddleware
# from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import set
from backend.src.account.user.api import user_router
from backend.src.account.user.login_handler import login_router
from backend.src.account.user.router import service_router
from backend.src.license.router import router as license_router

#########################
# BLOCK WITH API ROUTES #
#########################

app = FastAPI(
    title=set.PROJECT_NAME,
    version=set.PROJECT_VERSION
)
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
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(
    service_router,
    tags=["service"]
)

main_api_router.include_router(
    user_router,
    prefix="/user",
    tags=["USER"]
)
main_api_router.include_router(
    login_router,
    prefix="/login",
    tags=["LOGIN"]
)

main_api_router.include_router(
    license_router,
    prefix="/license",
    tags=["LICENSE"]
)


app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="127.0.0.1", port=8009)
