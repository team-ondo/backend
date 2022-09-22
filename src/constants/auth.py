import os

from dotenv import load_dotenv
from jose.constants import ALGORITHMS

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10080  # 60 * 24 * 7 (7 days)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_KEY = os.getenv("JWT_REFRESH_KEY")
ALGORITHM = ALGORITHMS.HS256
