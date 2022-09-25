from fastapi import APIRouter, Depends, Path

import src.schemas.auth as auth_schema
from src.constants.common import RE_UUID
from src.errors.errors import (
    DeviceIsNotConnectedToServerError,
    FailedToSendCommandToDeviceError,
    TokenExpiredException,
    TokenValidationFailException,
    UserNotFoundException,
    error_response,
)
from src.main import socket_manager as sm
from src.routers.auth import get_current_user
from src.utils.socket import find_socket_id_by_device_id

router = APIRouter()


@router.get(
    "/devices/{device_id}/alarm/off",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
            DeviceIsNotConnectedToServerError,
            # FailedToSendCommandToDeviceError,
        ]
    ),
)
async def set_device_alarm_off(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
):
    socket_id = find_socket_id_by_device_id(device_id)
    if socket_id is None:
        raise DeviceIsNotConnectedToServerError()

    await sm.emit("set_alarm_off", to=socket_id, namespace="/hardware")

    # TODO How to set ack result in callback
    # raise FailedToSendCommandToDeviceError
