import requests

THUNDERCLOUD_URL = "http://localhost:8000/"

def post_ride_data_to_api(bike_record):
    requests.post(THUNDERCLOUD_URL + "bike_record", json=bike_record.to_json())