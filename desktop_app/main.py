import sys
import pathlib

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QLineEdit, QHBoxLayout

from helper_threads import FileIngestionWorker
class MainApp(QMainWindow):
    RIDE_FILES_DIR = pathlib.Path(__file__).parent / "ride_files"
    def __init__(self):
        super().__init__()

        # Setup file ingestion worker
        self.file_ingestion_worker = FileIngestionWorker()
        self.file_ingestion_worker.result_signal.connect(self.label_done)
        self.setWindowTitle("WATTWatch Desktop Application")
        self.setGeometry(200, 100, 500, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Add button to ingest
        self.process_data_button = QPushButton("Process Data")
        self.process_data_button.clicked.connect(self.process_data)
        self.layout.addWidget(self.process_data_button)
        self.process_data_button.setEnabled(False)
        
        # File selection widget
        self.file_selection_layout = QHBoxLayout(self)
        self.layout.addLayout(self.file_selection_layout)
        # Add a label to display the selected file path
        self.file_path = QLineEdit(self)
        self.file_path.setText("No file selected yet")
        self.file_selection_layout.addWidget(self.file_path)

        # Add file selection button
        self.open_file_button = QPushButton("Select ride CSV")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.file_selection_layout.addWidget(self.open_file_button)


    def open_file_dialog(self):
        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Ride File CSV", str(self.RIDE_FILES_DIR), "*.csv")
        if file_path:
            self.file_path.setText(file_path)
            self.process_data_button.setEnabled(True)

    def process_data(self):
        # Start the file ingestion worker with the selected file path
        self.file_ingestion_worker.file_path = self.file_path.text()
        self.file_ingestion_worker.start()


    def label_done(self, data:list):
        print(data)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
