from fastapi import FastAPI
from src.routers import device
from src.routers import weather

app = FastAPI()
app.include_router(device.router)
app.include_router(weather.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
