from dataclasses import dataclass
from typing import Any

@dataclass
class RideData:
    timestamp: int
    long: int
    lat: int
    speed: float
    soc: int

    def to_json(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "long": self.long,
            "lat": self.lat,
            "speed": self.speed,
            "soc": self.soc
        }