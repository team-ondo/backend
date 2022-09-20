import datetime as date
import os
import random
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.models import Alarm, Button, Device, Humidity, Motion, Notification, Register, Temperature, User

load_dotenv()
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

engine = create_engine(SYNC_DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

uuid = "a7382f5c33264cf8b717549affe1c2eb"

seed_time = datetime.now()


def get_date():
    # slightly randomizes day
    return datetime.now() - date.timedelta(random.randint(1, 7))


date1 = get_date()
date2 = get_date()
date3 = get_date()

registered1 = Register(id=uuid, registered=True, created_at=seed_time, updated_at=seed_time)
user1 = User(first_name="Akemi", last_name="Kimura", email="test@test.com", phone_number="111-2222-3333", created_at=seed_time, updated_at=seed_time)
device1 = Device(id=uuid, latitude=35.6560, longitude=139.7247, device_name="Roppongi_Device", created_at=seed_time, updated_at=seed_time, user_id=1)

temp1 = Temperature(temperature=28.7, created_at=date1, device_id=uuid)
humidity1 = Humidity(humidity=54, created_at=date1, device_id=uuid)
temp2 = Temperature(temperature=28.7, created_at=date1, device_id=uuid)
humidity2 = Humidity(humidity=54, created_at=date1, device_id=uuid)
temp3 = Temperature(temperature=25.8, created_at=date1, device_id=uuid)
humidity3 = Humidity(humidity=66, created_at=date1, device_id=uuid)
temp4 = Temperature(temperature=29.7, created_at=date2, device_id=uuid)
humidity4 = Humidity(humidity=70, created_at=date2, device_id=uuid)
temp5 = Temperature(temperature=30.7, created_at=date2, device_id=uuid)
humidity5 = Humidity(humidity=71, created_at=date2, device_id=uuid)
temp6 = Temperature(temperature=28.7, created_at=date2, device_id=uuid)
humidity6 = Humidity(humidity=54, created_at=date2, device_id=uuid)
temp7 = Temperature(temperature=31.7, created_at=date3, device_id=uuid)
humidity7 = Humidity(humidity=72, created_at=date3, device_id=uuid)
temp8 = Temperature(temperature=25.6, created_at=date3, device_id=uuid)
humidity8 = Humidity(humidity=60, created_at=date3, device_id=uuid)

motion1 = Motion(motion=True, created_at=seed_time, device_id=uuid)
notification1 = Notification(content="Please call", is_read=False, created_at=seed_time, device_id=uuid)
button1 = Button(device_listening=True, created_at=seed_time, device_id=uuid)
alarm1 = Alarm(is_alarm=False, created_at=seed_time, device_id=uuid)

session.add_all(
    [
        registered1,
        user1,
        device1,
        temp1,
        humidity1,
        temp2,
        humidity2,
        temp3,
        humidity3,
        temp4,
        humidity4,
        temp6,
        humidity6,
        temp7,
        humidity7,
        temp8,
        humidity8,
        motion1,
        notification1,
        button1,
        alarm1,
    ]
)

# session.add_all(test_temp_humidity)

session.commit()
