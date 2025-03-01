from dataclasses import dataclass

@dataclass
class RideData:
    timestamp: int
    long: int
    lat: int
    speed: float
    soc: int
