from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.api import api_router
from app.core.execptions import CustomException
from app.db import init_db

app = FastAPI(debug=True)

app.include_router(api_router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=200,  # 返回200状态码
        content={"code": exc.code, "message": exc.message},
    )


@app.on_event("startup")
def startup_event():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
