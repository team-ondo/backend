from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, device, notification, settings, weather

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(device.router)
app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(notification.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
