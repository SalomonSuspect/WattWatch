import csv
import pathlib
from typing import Generator
from datetime import datetime

from data_structure import RideData


def convert_garmin_epoch_to_unix(g_epoch_time_stamp: int) -> int:
    """A FIT FILE timestamp is the seconds since Garmin Epoch of  December 31, 1989, 00:00:00 UTC.
       This method converts the garmin epoch time from a fit file timestamp to a Unix timestamp for normalization
    """
    garmin_epoch = datetime(1989, 12, 31, 0, 0)
    unix_epoch = datetime(1970, 1, 1, 0, 0)
    epoch_delta = garmin_epoch - unix_epoch
    return int(g_epoch_time_stamp + epoch_delta.total_seconds())

def parse_csv(csv_file_path: pathlib.Path) -> Generator[RideData, None, None]:
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            normal_timestamp = convert_garmin_epoch_to_unix(int(row[0]))
            yield RideData(timestamp=normal_timestamp, long=int(row[1]), lat=int(row[2]), speed=float(row[3]), soc=int(row[4]))       
