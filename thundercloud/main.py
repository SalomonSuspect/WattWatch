from pydantic import BaseModel
from fastapi import FastAPI

class BikeRecord(BaseModel):
    timestamp: int
    long: int
    lat: int
    speed: float
    soc: int

bike_records = []
app = FastAPI()

@app.post("/bike_record")
async def ingest_bike_record(bike_record: BikeRecord):
    print(f"Received bike record: {bike_record}")
    bike_records.append(bike_record)
    print(f"Total bike records: {len(bike_records)}")
    return {"message": "Bike record received"}

@app.get("/")
def main():
    return {"message": "Welcome to Thundercloud - ebike tracking API"}

