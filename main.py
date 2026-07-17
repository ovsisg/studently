from PyQt6.QtWidgets import QMainWindow, QApplication   
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")

app = QApplication(sys.argv)   
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())