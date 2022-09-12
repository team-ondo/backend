from fastapi import FastAPI
from src.routers import device

app = FastAPI()
app.include_router(device.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
