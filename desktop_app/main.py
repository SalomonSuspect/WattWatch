import sys
import pathlib

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QFileDialog, QLineEdit, QHBoxLayout

class MainApp(QMainWindow):
    RIDE_FILES_DIR = pathlib.Path(__file__).parent / "ride_files"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WATTWatch Desktop Application")
        self.setGeometry(200, 100, 500, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

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

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
