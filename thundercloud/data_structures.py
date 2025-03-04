from pydantic import BaseModel

class BikeRecord(BaseModel):
    timestamp: int
    long: int
    lat: int
    speed: float
    soc: int

class RideSummary(BaseModel):
    ride_id: int
    duration_m: float
    avg_speed_mph: float
    ending_soc: int