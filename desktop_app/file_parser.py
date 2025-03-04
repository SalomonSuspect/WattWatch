import csv
import pathlib
from typing import Generator
from datetime import datetime

from data_structure import RideData


class FileParseException(Exception):
    pass


def convert_garmin_epoch_to_unix(g_epoch_time_stamp: int) -> int:
    """A FIT FILE timestamp is the seconds since Garmin Epoch of  December 31, 1989, 00:00:00 UTC.
    This method converts the garmin epoch time from a fit file timestamp to a Unix timestamp for normalization
    """
    garmin_epoch = datetime(1989, 12, 31, 0, 0)
    unix_epoch = datetime(1970, 1, 1, 0, 0)
    epoch_delta = garmin_epoch - unix_epoch
    return int(g_epoch_time_stamp + epoch_delta.total_seconds())


def csv_row_to_ride_data(csv_row: list[str]) -> RideData:
    normal_timestamp = convert_garmin_epoch_to_unix(int(csv_row[0]))
    try:
        return RideData(
            timestamp=normal_timestamp,
            long=int(csv_row[1]),
            lat=int(csv_row[2]),
            speed=float(csv_row[3]),
            soc=int(csv_row[4]),
        )
    except Exception as ec:
        raise FileParseException(f"Invalid data in CSV row: {csv_row}") from ec


def parse_csv(csv_file_path: pathlib.Path) -> Generator[RideData, None, None]:
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            yield csv_row_to_ride_data(row)
