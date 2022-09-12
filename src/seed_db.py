from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import User, Device, Temperature, Humidity, Notification, Motion, Button, Alarm

USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'postgres'
DATABASE_URL = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

seed_time = datetime.now()

user1 = User(id=1, first_name="Akemi", last_name="Kimura", email="test@test.com", phone_number="111-2222-3333", created_at=seed_time, updated_at=seed_time)

device1 = Device(id=1, latitude=35.6560, longitude=139.7247, device_name="Roppongi_Device", created_at=seed_time, updated_at=seed_time, user_id=1)

temp1 = Temperature(id=1, temperature=28.7, created_at=seed_time, device_id=1)

humidity1 = Humidity(id=1, humidity=54, created_at=seed_time, device_id=1)

motion1 = Motion(id=1, motion=True, created_at=seed_time, device_id=1)

notification1 = Notification(id=1, content="Please call", is_read=False, created_at=seed_time, device_id=1)

button1 = Button(id=1, device_listening=True, created_at=seed_time, device_id=1)

alarm1 = Alarm(id=1, is_alarm=False, created_at=seed_time, device_id=1)

session.add_all([user1, device1, temp1, humidity1, motion1, notification1, button1, alarm1])

session.commit()
