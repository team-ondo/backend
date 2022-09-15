from fastapi import FastAPI

from src.routers import device, weather

app = FastAPI()
app.include_router(device.router)
app.include_router(weather.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
