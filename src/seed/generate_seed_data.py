from datetime import datetime, timedelta
from typing import Dict, List

from faker import Faker

fake = Faker()

UUID = "a7382f5c33264cf8b717549affe1c2eb"
NUM_OF_DATA_POINTS = 10000
NUM_OF_DATA_POINTS_FOR_DAY = 1000


def generate_historic_temp_data() -> Dict[str, List]:

    result: Dict[str, List] = {
        "temp": [],
        "humid": [],
    }

    for _ in range(NUM_OF_DATA_POINTS):
        temp = fake.random_int(min=13, max=36)
        humid = fake.random_int(min=50, max=80)
        date = fake.date_time_between(start_date=datetime(2022, 7, 21), end_date=datetime(2022, 9, 21)).strftime("%Y-%m-%d %H:%M:%S")

        temp_obj = {"temperature": temp, "created_at": date, "device_id": UUID}
        humid_obj = {"humidity": humid, "created_at": date, "device_id": UUID}

        result["temp"].append(temp_obj)
        result["humid"].append(humid_obj)

    for _ in range(NUM_OF_DATA_POINTS_FOR_DAY):
        temp = fake.random_int(min=13, max=36)
        humid = fake.random_int(min=50, max=80)
        date = fake.date_time_between(start_date=datetime.now() - timedelta(days=1), end_date=datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        temp_obj = {"temperature": temp, "created_at": date, "device_id": UUID}
        humid_obj = {"humidity": humid, "created_at": date, "device_id": UUID}

        result["temp"].append(temp_obj)
        result["humid"].append(humid_obj)

    return result
