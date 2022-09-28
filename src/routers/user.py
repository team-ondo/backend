from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.user as user_crud
import src.schemas.auth as auth_schema
import src.schemas.user as user_schema
from src.db.db import get_db
from src.errors.errors import TokenExpiredException, TokenValidationFailException, UserNotFoundException, error_response
from src.routers.auth import get_current_user

router = APIRouter()


@router.get(
    "/user/devices",
    response_model=List[user_schema.UserDevice],
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
)
async def read_user_devices(current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await user_crud.find_device_id_by_user_id(db, current_user.user_id)
