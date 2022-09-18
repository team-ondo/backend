from pydantic import BaseModel


class TokenData(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    user_id: int
    exp: int


class SystemUser(BaseModel):
    user_id: int
