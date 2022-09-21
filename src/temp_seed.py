from datetime import datetime

from faker import Faker

fake = Faker()

UUID = "a7382f5c33264cf8b717549affe1c2eb"
NUM_OF_DATA_POINTS = 1000

# temperature / created_at / device_id


def generate_historic_temp_data():
    result = []

    for _ in range(NUM_OF_DATA_POINTS):
        temp = fake.random_int(min=13, max=36)
        date = fake.date_time_between(start_date=datetime(2022, 7, 21), end_date=datetime(2022, 9, 21)).strftime("%Y-%m-%d %H:%M:%S")

        obj = {"temperature": temp, "created_at": date, "device_id": UUID}
        result.append(obj)

    return result
