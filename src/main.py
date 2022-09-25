from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_socketio import SocketManager
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.errors.errors import APIError
from src.routers import auth, device, notification, settings, user, weather
from src.sockets.hardware_namespace import HardwareNameSpace

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)
app.include_router(device.router)
app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(notification.router)
app.include_router(user.router)


@app.exception_handler(APIError)
async def api_error_handler(request, err: APIError):
    return JSONResponse(status_code=err.status_code, content={"detail": err.detail}, headers=err.headers)


socket_manager = SocketManager(app)
socket_manager._sio.register_namespace(HardwareNameSpace("/hardware"))


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


from src.routers import alarm  # noqa: E402

app.include_router(alarm.router)
