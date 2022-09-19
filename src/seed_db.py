import os
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

seed_time = datetime.now()

uuid = "a7382f5c33264cf8b717549affe1c2eb"

registered1 = Register(id=uuid, registered=True, created_at=seed_time, updated_at=seed_time)
user1 = User(first_name="Akemi", last_name="Kimura", email="test@test.com", phone_number="111-2222-3333", created_at=seed_time, updated_at=seed_time)
device1 = Device(id=uuid, latitude=35.6560, longitude=139.7247, device_name="Roppongi_Device", created_at=seed_time, updated_at=seed_time, user_id=1)
temp1 = Temperature(temperature=28.7, created_at=seed_time, device_id=uuid)
humidity1 = Humidity(humidity=54, created_at=seed_time, device_id=uuid)
motion1 = Motion(motion=True, created_at=seed_time, device_id=uuid)
notification1 = Notification(content="Please call", is_read=False, created_at=seed_time, device_id=uuid)
button1 = Button(device_listening=True, created_at=seed_time, device_id=uuid)
alarm1 = Alarm(is_alarm=False, created_at=seed_time, device_id=uuid)

session.add_all([registered1, user1, device1, temp1, humidity1, motion1, notification1, button1, alarm1])
session.commit()
