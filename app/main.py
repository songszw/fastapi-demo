from fastapi import FastAPI

from app.api import api_router
from app.db import init_db

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
def startup_event():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
