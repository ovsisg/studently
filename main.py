from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, \
QLineEdit, QComboBox, QDateEdit, QPushButton, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
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
        about_action.triggered.connect(self.open_about_dialog)
        
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

    def open_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec()

class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)
        
        self.date_of_birth = QDateEdit()
        self.date_of_birth.setCalendarPopup(True)
        self.date_of_birth.setDate(QDate.currentDate())
        layout.addWidget(self.date_of_birth)
        
        self.course = QComboBox()
        courses = ["Computer Science BSc", "Cyber Security BSc", "History BA", "Biology BSc", "Biomedical Science BSc", "Zoology BSc"]
        self.course.addItems(courses)
        layout.addWidget(self.course)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)
        
        button = QPushButton("Add")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.name.text()
        date_of_birth = self.date_of_birth.date().toString("dd/MM/yyyy")
        course = self.course.itemText(self.course.currentIndex())
        email = self.email.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student (name, date_of_birth, course, email) VALUES (?, ?, ?, ?)", 
                       (name, date_of_birth, course, email))
        conn.commit()
        cursor.close()
        conn.close()
        main_window.load_data()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        content = """Miles is an npc. Now npcs are rare to find. Well, actually, no. People are sheep nowadays.
        """
        self.setText(content)
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)
        
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def search_student(self):
        name = self.name.text()
       
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            for col in range(main_window.table.columnCount()):
                main_window.table.item(item.row(), col).setBackground(QColor("yellow"))

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()
        index = main_window.table.currentRow()

        self.id = main_window.table.item(index, 0).text()

        name = main_window.table.item(index, 1).text()
        self.name = QLineEdit(name)
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        date_of_birth = main_window.table.item(index, 2).text()
        self.date_of_birth = QDateEdit()
        self.date_of_birth.setCalendarPopup(True)
        self.date_of_birth.setDate(QDate.fromString(date_of_birth, "dd/MM/yyyy"))
        layout.addWidget(self.date_of_birth)

        course = main_window.table.item(index, 3).text()
        self.course = QComboBox()
        courses = ["Computer Science BSc", "Cyber Security BSc", "History BA", "Biology BSc", "Biomedical Science BSc", "Zoology BSc"]
        self.course.addItems(courses)
        self.course.setCurrentText(course)
        layout.addWidget(self.course)

        email = main_window.table.item(index, 4).text()
        self.email = QLineEdit(email)
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)
        
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
        
        self.setLayout(layout)

    def update_student(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE student SET name = ?, date_of_birth = ?, course = ?, email = ? WHERE id = ?",
                       (self.name.text(), self.date_of_birth.text(), self.course.itemText(self.course.currentIndex()), 
                        self.email.text(), self.id))
        conn.commit()
        cursor.close()
        conn.close()
        main_window.load_data()
        self.close()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studently")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete it?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_student)

    def delete_student(self):
        index = main_window.table.currentRow()
        id = main_window.table.item(index, 0).text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = ?", (id, ))
        conn.commit()
        cursor.close()
        conn.close()
        main_window.load_data()
        self.close()

app = QApplication(sys.argv)   
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())