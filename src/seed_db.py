import datetime as date
import os
import random
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.utils import create_hash_password
from src.models.models import Alarm, Button, Device, Humidity, Motion, Notification, Register, Temperature, User
from src.seed.generate_seed_data import generate_historic_temp_data

load_dotenv()
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

engine = create_engine(SYNC_DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

uuid = "a7382f5c33264cf8b717549affe1c2eb"

seed_time = datetime.now()


def get_date():
    return datetime.now() - date.timedelta(random.randint(1, 7))


data_set = []

data_set.append(Register(id=uuid, registered=True, created_at=seed_time, updated_at=seed_time))
data_set.append(
    User(
        first_name="Akemi",
        last_name="Kimura",
        email="test@test.com",
        phone_number="111-2222-3333",
        password=create_hash_password("secret"),
        created_at=seed_time,
        updated_at=seed_time,
    )
)
data_set.append(
    Device(id=uuid, latitude=35.6560, longitude=139.7247, device_name="Roppongi_Device", created_at=seed_time, updated_at=seed_time, user_id=1)
)


generated_data_set = generate_historic_temp_data()

for row in generated_data_set.get("temp"):
    data_set.append(Temperature(**row))

for row in generated_data_set.get("humid"):
    data_set.append(Humidity(**row))

data_set.append(Motion(motion=True, created_at=seed_time, device_id=uuid))
data_set.append(Notification(content="Please call", is_read=False, created_at=seed_time, device_id=uuid))
data_set.append(Button(device_listening=True, created_at=seed_time, device_id=uuid))
data_set.append(Alarm(is_alarm=False, created_at=seed_time, device_id=uuid))

session.add_all(data_set)

session.commit()
