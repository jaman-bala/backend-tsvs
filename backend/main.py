from fastapi import FastAPI

from backend.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
    )


@app.get("/")
def hello_api():
    return {"massage": "Салам алейкум на backend🚀"}
