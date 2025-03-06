from data_structure import RideData, RideSummary
import requests

THUNDERCLOUD_URL = "http://localhost:8000/"


def post_ride_data_to_api(bike_record: RideData, bike_ride_id: int):
    res = requests.post(
        THUNDERCLOUD_URL + "bike_record" + f"/{bike_ride_id}",
        json=bike_record.to_json(),
    )
    res.raise_for_status()


def get_ride_summary(ride_id: int):
    response = requests.get(THUNDERCLOUD_URL + f"bike_record/summary/{ride_id}")
    response.raise_for_status()
    return RideSummary.from_json(response.json())
