from fastapi import FastAPI, HTTPException

from data_structures import BikeRecord, RideSummary
from helper_functions import find_average_speed

bike_records: dict[int, list[BikeRecord]] = {}
app = FastAPI()

@app.post("/bike_record/{ride_id}")
def ingest_bike_record(ride_id: int, bike_record: BikeRecord):
    print(f"Received bike record: {bike_record} for {ride_id}")
    if ride_id not in bike_records:
        bike_records[ride_id] = [bike_record]
    else:
        bike_records[ride_id].append(bike_record)
    print(f"Total bike records for id {ride_id}: {len(bike_records[ride_id])}")
    return {"message": f"Bike record received for {ride_id}"}

@app.get("/bike_record/{ride_id}")
def get_bike_records(ride_id: int):
    print(f"Responding with bike records for id {ride_id} - {bike_records.keys()}")
    if ride_id not in bike_records:
        raise HTTPException(status_code=404, detail=f"bike record {ride_id} not found")
    return bike_records.get(ride_id)

@app.get("/")
def main():
    return {"message": "Welcome to Thundercloud - ebike tracking API"}

