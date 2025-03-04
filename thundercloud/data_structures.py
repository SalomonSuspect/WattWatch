from pydantic import BaseModel

class BikeRecord(BaseModel):
    timestamp: int
    long: int
    lat: int
    speed: float
    soc: int

class RideSummary(BaseModel):
    start_time: int
    end_time: int
    avg_speed: float
    ending_soc: int