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
            "soc": self.soc,
        }

@dataclass
class RideSummary:
    ride_id: int
    duration_m: float
    avg_speed_mph: float
    ending_soc: int

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> "RideSummary":
        return cls(
            ride_id=json_data["ride_id"],
            duration_m=json_data["duration_m"],
            avg_speed_mph=json_data["avg_speed_mph"],
            ending_soc=json_data["ending_soc"],
        )