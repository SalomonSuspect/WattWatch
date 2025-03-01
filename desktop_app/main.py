import pathlib

from file_parser import parse_csv
from thundercloud import post_ride_data_to_api

def main():
    ride_id = 1
    while True:
        print("\nWelcome to ThunderCloud Bike Ingestion Tool!")
        csv_path = pathlib.Path(input("path to csv file: "))
        print(f"Posting ride data from {csv_path} for ride {ride_id}")
        for item in parse_csv(csv_path):
            post_ride_data_to_api(item, bike_ride_id=ride_id) 
        ride_id += 1

if __name__ == "__main__":
    main()
