"""QThread workers"""

import pathlib

from PySide6.QtCore import QThread, Signal

from file_parser import parse_csv
from data_structure import RideData
from thundercloud import post_ride_data_to_api  # type: ignore


class FileIngestionWorker(QThread):
    result_signal = Signal(list)
    exception_signal = Signal(str)

    def __init__(self, file_path: str | None = None):
        super().__init__()
        self.file_path = file_path

    def run(self):
        if self.file_path is None:
            self.exception_signal.emit(
                "file path must be set before starting the worker"
            )
            return
        self.file_path = pathlib.Path(self.file_path)
        if not self.file_path.exists():
            self.exception_signal.emit(f"File {self.file_path} does not exist")
            return
        data_from_file = list(parse_csv(self.file_path))
        # print(f"{data_from_file=}/{self.file_path}")
        self.result_signal.emit(data_from_file)


class PostDataToTC(QThread):
    result_signal = Signal(int, int)
    exception_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.ride_data = []
        self.ride_id: int | None = None

    def run(self):
        if self.ride_id is None:
            self.exception_signal.emit("No ride ID set before starting the worker")
            return
        try:
            for data in self.ride_data:
                post_ride_data_to_api(data, self.ride_id)
        except Exception as e:
            self.exception_signal.emit(f"Error sending data to Thundercloud: {e}")
        else:
            self.result_signal.emit(self.ride_id, len(self.ride_data))
