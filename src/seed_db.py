import datetime as date
import random
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.utils import create_hash_password
from src.constants.common import SYNC_DATABASE_URL
from src.models.models import Alarm, Button, Device, Humidity, Motion, Notification, Register, Temperature, User
from src.seed.generate_seed_data import generate_historic_alarm_data, generate_historic_temp_data

engine = create_engine(SYNC_DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

uuid = "a7382f5c33264cf8b717549affe1c2eb"

seed_time = datetime.now()


def get_date():
    return datetime.now() - date.timedelta(random.randint(1, 7))


# content_type
"Alarm"
"Snooze"
"Out"

content_types = ["Alarm", "Snooze", "Out"]


def get_content_type():
    index = random.randint(0, 3) - 1
    return content_types[index]


data_set = []

data_set.append(Register(id=uuid, registered=True, created_at=seed_time, updated_at=seed_time))
data_set.append(
    User(
        first_name="Akemi",
        last_name="Kimura",
        email="test@test.com",
        phone_number="111-2222-3333",
        password=create_hash_password("secretPassword"),
        created_at=seed_time,
        updated_at=seed_time,
    )
)
data_set.append(
    Device(
        id=uuid,
        latitude=35.6560,
        longitude=139.7247,
        device_name="Roppongi_Device",
        zip_code="1001701",
        temp_upper_limit=32.9,
        temp_lower_limit=29.2,
        created_at=seed_time,
        updated_at=seed_time,
        user_id=1,
    )
)


generated_data_set = generate_historic_temp_data()

for row in generated_data_set.get("temp"):
    data_set.append(Temperature(**row))

for row in generated_data_set.get("humid"):
    data_set.append(Humidity(**row))

data_set.append(Motion(motion=True, created_at=seed_time, device_id=uuid))

data_set.append(Button(device_listening=True, created_at=seed_time, device_id=uuid))

generated_data_set_alarm = generate_historic_alarm_data()

for i in range(1, 21):
    notification_time = get_date()
    dynamic_content = get_content_type()
    message = ""

    if dynamic_content == "Alarm":
        message = "Alarm has been triggered, call to check in!"
    elif dynamic_content == "Snooze":
        message = "Alarm has been snoozed."
    else:
        message = "Out of house."

    id = i

    data_set.append(
        Notification(
            id=id,
            content_type=dynamic_content,
            content=message,
            is_read=False,
            created_at=notification_time,
            device_id=uuid,
        )
    )

for row in generated_data_set_alarm.get("alarm"):
    data_set.append(Alarm(**row))

session.add_all(data_set)

session.commit()
