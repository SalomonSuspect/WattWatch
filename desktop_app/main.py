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
from PySide6.QtGui import QIntValidator
from helper_threads import FileIngestionWorker, PostDataToTC


class MainApp(QMainWindow):
    RIDE_FILES_DIR = pathlib.Path(__file__).parent / "ride_files"

    def __init__(self):
        super().__init__()

        # Setup file ingestion worker
        self.file_ingestion_worker = FileIngestionWorker()
        self.file_ingestion_worker.result_signal.connect(self.on_parse_data)
        self.file_ingestion_worker.exception_signal.connect(self.error_popup)

        # Setup PostDataToTC runner
        self.post_data_to_thundercloud = PostDataToTC()
        self.post_data_to_thundercloud.result_signal.connect(self.on_post_data_success)
        self.post_data_to_thundercloud.exception_signal.connect(self.error_popup)

        self.setWindowTitle("WATTWatch Desktop Application")
        self.setGeometry(200, 100, 500, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add button to ingest
        self.process_data_button = QPushButton("Process Data")
        self.process_data_button.clicked.connect(self.on_process_data_click)
        self.layout.addWidget(self.process_data_button)
        self.process_data_button.setEnabled(False)

        # Ride ID Input widget
        self.ride_id_layout = QHBoxLayout(self.central_widget)
        self.ride_id_label = QLabel("Ride ID:")
        int_validator = QIntValidator()
        self.ride_id_box = QLineEdit(self)
        self.ride_id_box.setValidator(int_validator)
        self.ride_id_box.textChanged.connect(self.enable_process_data_button)

        self.layout.addLayout(self.ride_id_layout)
        self.ride_id_layout.addWidget(self.ride_id_label)
        self.ride_id_layout.addWidget(self.ride_id_box)

        # File selection widget
        self.file_selection_layout = QHBoxLayout(self.central_widget)
        self.layout.addLayout(self.file_selection_layout)
        # Add a label to display the selected file path
        self.file_path = QLineEdit(self)
        self.file_path.textChanged.connect(self.enable_process_data_button)

        self.file_path.setText("No file selected yet")
        self.file_selection_layout.addWidget(self.file_path)

        # Add file selection button
        self.open_file_button = QPushButton("Select ride CSV")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.file_selection_layout.addWidget(self.open_file_button)

    def open_file_dialog(self):
        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Ride File CSV", str(self.RIDE_FILES_DIR), "*.csv"
        )
        if file_path:
            self.file_path.setText(file_path)
            self.process_data_button.setEnabled(True)

    def enable_process_data_button(self):
        self.process_data_button.setEnabled(
            len(self.file_path.text()) > 0 and len(self.ride_id_box.text()) > 0
        )

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
        error_message.exec_()

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
        success_message.exec_()
        self.ride_id_box.clear()
        self.file_path.clear()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
