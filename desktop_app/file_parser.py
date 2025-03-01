import csv
import pathlib
from typing import Generator
from data_structure import RideData

def parse_csv(csv_file_path: pathlib.Path) -> Generator[RideData, None, None]:
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield RideData(timestamp=int(row[0]), long=int(row[1]), lat=int(row[2]), speed=float(row[3]), soc=int(row[4]))       
