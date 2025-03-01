from data_structure import RideData
import requests

THUNDERCLOUD_URL = "http://localhost:8000/"

def post_ride_data_to_api(bike_record: RideData, bike_ride_id: int):
    requests.post(THUNDERCLOUD_URL + "bike_record" + f"/{bike_ride_id}", json=bike_record.to_json())