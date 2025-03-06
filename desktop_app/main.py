from os import error
import sys
import pathlib

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
    QLabel,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from helper_threads import FileIngestionWorker, PostDataToTC, RideSummaryWorker
from data_structure import RideSummary


class MainApp(QMainWindow):
    RIDE_FILES_DIR = pathlib.Path(__file__).parent / "ride_files"

    def __init__(self):
        super().__init__()

        # Setup file ingestion Runner
        self.file_ingestion_worker = FileIngestionWorker()
        self.file_ingestion_worker.result_signal.connect(self.on_parse_data)
        self.file_ingestion_worker.exception_signal.connect(self.error_popup)

        # Setup PostDataToTC Runner
        self.post_data_to_thundercloud = PostDataToTC()
        self.post_data_to_thundercloud.result_signal.connect(self.on_post_data_success)
        self.post_data_to_thundercloud.exception_signal.connect(self.error_popup)

        # Get Ride Summary Runner
        self.ride_summary_runner = RideSummaryWorker()
        self.ride_summary_runner.result_signal.connect(self.on_get_ride_summary_success)
        self.ride_summary_runner.exception_signal.connect(self.error_popup)

        # Setup UI
        self.setWindowTitle("WATTWatch Desktop Application")
        self.setGeometry(200, 100, 500, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add a label to display the application's banner
        banner = QLabel("WattWatch Desktop Application")
        banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner.setStyleSheet(
            """
            background-color: #FF0000;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """
        )
        self.layout.addWidget(banner)

        # Ride ID Input widget
        self.ride_id_layout = QHBoxLayout(self.central_widget)
        self.ride_id_label = QLabel("Ride ID:")
        int_validator = QIntValidator()
        self.ride_id_box = QLineEdit(self)
        self.ride_id_box.setValidator(int_validator)

        self.layout.addLayout(self.ride_id_layout)
        self.ride_id_layout.addWidget(self.ride_id_label)
        self.ride_id_layout.addWidget(self.ride_id_box)

        self.display_ride_info_box = QPushButton("Display Ride Info")
        self.display_ride_info_box.setEnabled(False)
        self.ride_id_layout.addWidget(self.display_ride_info_box)

        # File selection widget
        self.file_selection_layout = QHBoxLayout(self.central_widget)
        self.layout.addLayout(self.file_selection_layout)
        # Add a label to display the selected file path
        self.file_path = QLineEdit(self)

        self.file_path_default_text = "No file selected yet"
        self.file_path.setText(self.file_path_default_text)
        self.file_selection_layout.addWidget(self.file_path)

        # Add file selection button
        self.open_file_button = QPushButton("Select ride CSV")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.file_selection_layout.addWidget(self.open_file_button)

        # Add button to ingest
        self.process_data_button = QPushButton("Publish Data to Thundercloud")
        self.layout.addWidget(self.process_data_button)
        self.process_data_button.setEnabled(False)

        # Connect GUI signals/slots last
        self.process_data_button.clicked.connect(self.on_process_data_click)
        self.file_path.textChanged.connect(self.enable_buttons)
        self.ride_id_box.textChanged.connect(self.enable_buttons)
        self.display_ride_info_box.clicked.connect(self.on_get_ride_summary_click)

    def open_file_dialog(self):
        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Ride File CSV", str(self.RIDE_FILES_DIR), "*.csv"
        )
        if file_path:
            self.file_path.setText(file_path)
            self.process_data_button.setEnabled(True)

    def enable_buttons(self):
        self.process_data_button.setEnabled(
            self.file_path.text() != self.file_path_default_text
            and len(self.ride_id_box.text()) > 0
        )
        self.display_ride_info_box.setEnabled(len(self.ride_id_box.text()) > 0)

    def on_process_data_click(self):
        # Start the file ingestion worker with the selected file path
        self.file_ingestion_worker.file_path = self.file_path.text()
        self.file_ingestion_worker.start()

    def error_popup(self, message: str):
        error_message = QMessageBox(self)
        error_message.setWindowTitle("Error")
        error_message.setText(message)
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.setIcon(QMessageBox.Critical)
        error_message.exec()

    def on_parse_data(self, data: list):
        print("Parsed data now posting to thundercloud")
        self.post_data_to_thundercloud.ride_data = data
        self.post_data_to_thundercloud.ride_id = int(self.ride_id_box.text())
        self.post_data_to_thundercloud.start()

    def on_post_data_success(self, ride_id: int, ride_data_length: int):
        success_message = QMessageBox(self)
        success_message.setWindowTitle("Success")
        success_message.setText(
            f"Successfully sent {ride_data_length} records for ride {ride_id} to Thundercloud."
        )
        success_message.setStandardButtons(QMessageBox.Ok)
        success_message.exec()
        self.ride_id_box.clear()
        self.file_path.setText(self.file_path_default_text)

    def on_get_ride_summary_click(self):
        self.ride_summary_runner.ride_id = int(self.ride_id_box.text())
        self.ride_summary_runner.start()

    def on_get_ride_summary_success(self, summary: RideSummary):
        summary_message = QMessageBox(self)
        summary_message.setWindowTitle("Ride Summary")
        summary_message.setText(
            f"Ride Summary for Ride ID: {summary.ride_id}\n"
            f"Total Duration: {summary.duration_m: 0.2f} minutes\n"
            f"Average Speed: {summary.avg_speed_mph} mph"
        )
        summary_message.setStandardButtons(QMessageBox.Ok)
        summary_message.exec()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
