from datetime import datetime

import pytest

from file_parser import csv_row_to_ride_data, FileParseException


def unix_epoch_to_garmin(u_epoch):
    garmin_epoch = datetime(1989, 12, 31, 0, 0)
    unix_epoch = datetime(1970, 1, 1, 0, 0)
    epoch_delta = garmin_epoch - unix_epoch
    return int((u_epoch + epoch_delta.total_seconds()))


@pytest.fixture
def good_csv_row():
    return ["12345", "123456", "789012", "10.5", "95"]


@pytest.fixture
def bad_csv_row():
    return ["12345", "123456"]


def test_valid_ingestion(good_csv_row: list[str]):
    # Make sure a valid csv row gets ingested successfully
    ride_data = csv_row_to_ride_data(good_csv_row)
    assert ride_data.timestamp == unix_epoch_to_garmin(int(good_csv_row[0]))
    assert ride_data.long == int(good_csv_row[1])
    assert ride_data.lat == int(good_csv_row[2])
    assert ride_data.speed == float(good_csv_row[3])
    assert ride_data.soc == int(good_csv_row[4])


def test_bad_ingestion(bad_csv_row):
    # Make sure a valid csv row gets ingested successfully
    with pytest.raises(FileParseException):
        _ = csv_row_to_ride_data(bad_csv_row)
