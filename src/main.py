from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.errors.errors import APIError
from src.routers import auth, device, notification, settings, weather

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIError)
async def api_error_handler(request, err: APIError):
    return JSONResponse(status_code=err.status_code, content={"detail": err.detail}, headers=err.headers)


app.include_router(device.router)
app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(notification.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
