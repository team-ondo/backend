from fastapi import FastAPI

from src.routers import auth, device, weather

app = FastAPI()
app.include_router(device.router)
app.include_router(weather.router)
app.include_router(auth.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
