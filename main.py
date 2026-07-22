from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
QLineEdit, QComboBox, QDateEdit, QPushButton, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QColor
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(600, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.open_add_dialog)
        file_menu_item.addAction(add_student_action)
        
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        
        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.open_search_dialog)
        edit_menu_item.addAction(search_student_action)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Date of Birth", "Course", "Email"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)    

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("border: none;")
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        conn = sqlite3.connect("database.db")
        result = conn.execute("SELECT * FROM student")
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table.insertRow(row_index)
            for column_index, cell_data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))
                
        conn.close()
        
    def cell_clicked(self):
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.open_edit_dialog)
        self.status_bar.addWidget(edit_button)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.open_delete_dialog)
        self.status_bar.addWidget(delete_button)
        
    def open_add_dialog(self):
        dialog = AddDialog()
        dialog.exec()

    def open_search_dialog(self):
        dialog = SearchDialog()
        dialog.exec()

    def open_edit_dialog(self):
        dialog = EditDialog()
        dialog.exec()

    def open_delete_dialog(self):
        dialog = DeleteDialog()
        dialog.exec()

class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        self.date_of_birth = QDateEdit()
        self.date_of_birth.setCalendarPopup(True)
        self.date_of_birth.setDate(QDate.currentDate())
        layout.addWidget(self.date_of_birth)
        
        self.course_name = QComboBox()
        courses = ["Computer Science BSc", "Cyber Security BSc", "History BA", "Biology BSc", "Biomedical Science BSc", "Zoology BSc"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)
        
        button = QPushButton("Add")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.student_name.text()
        date_of_birth = self.date_of_birth.date().toString("dd/MM/yyyy")
        course = self.course_name.itemText(self.course_name.currentIndex())
        email = self.email.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student (name, date_of_birth, course, email) VALUES (?, ?, ?, ?)", 
                       (name, date_of_birth, course, email))
        conn.commit()
        cursor.close()
        conn.close()
        main_window.load_data()
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def search_student(self):
        name = self.student_name.text()
       
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            for col in range(main_window.table.columnCount()):
                main_window.table.item(item.row(), col).setBackground(QColor("yellow"))

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

app = QApplication(sys.argv)   
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())