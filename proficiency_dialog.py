# proficiency_dialog.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton, QVBoxLayout, QWidget, QDialog
from PyQt5.QtCore import Qt
import sqlite3
import resourcesCascade
import add_course_setting

class ProficiencyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Course Proficiency")
        self.proficiency_level = 0
        self.setStyleSheet("background-color: rgb(27, 32, 81); color: white;")  # Added a background color
        self.course_name = self.get_last_course_name()

        self.label = QLabel(f"How would you rate your proficiency in '{self.course_name}' (0-15)?", self)
        self.label.setStyleSheet("color: rgb(167, 145, 203); font: 10pt 'Montserrat';")

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(15)
        self.slider.setValue(0)  
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet("QSlider::groove:horizontal {border: 1px solid #999999; height: 8px;background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(167, 145, 203), stop:1 rgb(167, 145, 203));border-radius: 4px;}QSlider::handle:horizontal {background: rgb(167, 145, 203);border: 1px solid #777777;width: 13px;margin: -2px 0;border-radius: 4px;}")
        self.value_label = QLabel("0", self)
        self.value_label.setStyleSheet("color: rgb(195, 195, 195); font: 10pt 'Montserrat';")
        self.slider.valueChanged.connect(self.update_value_label)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("QPushButton {background-color: rgb(167, 145, 203); color: white; border-radius: 5px; font: 10pt 'Montserrat';}"
"QPushButton:hover {color: rgb(225, 225, 225);}")

        self.ok_button.clicked.connect(self.accept)
        

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
    
    def update_value_label(self, value):
        self.value_label.setText(str(value))
        self.proficiency_level = value

    def get_proficiency(self):
        return self.proficiency_level

    def accept(self):
        self.store_proficiency()
        if self.parent() and isinstance(self.parent(), add_course_setting.Ui_add_course_settings):
           self.parent().add_course_settings.close()
        super().accept()

    
    def store_proficiency(self):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        try:
            # Fetch the last course
            cursor.execute("SELECT name FROM courses ORDER BY ROWID DESC LIMIT 1")
            row = cursor.fetchone()

            if row:
                course_name = row[0]  # Get the name of the last added course

                cursor.execute("SELECT * FROM courses WHERE name = ?", (course_name,))
                row=cursor.fetchone()
                if row:
                    cursor.execute("UPDATE courses SET initial_user_said_score = ? WHERE name = ?", (self.proficiency_level, course_name))
                    print(f"updating the proficiency level for {course_name} to {self.proficiency_level} in the db")
                else:
                    cursor.execute("INSERT INTO courses(name, initial_user_said_score) VALUES (?,?)", (course_name, self.proficiency_level))
                    print(f"storing the proficiency level for {course_name} as {self.proficiency_level} in the db")
                    

                conn.commit()  # Commit changes to the database
            else:
              print("no course found")
        
        except sqlite3.Error as e:
          print(f"An error occurred: {e.args[0]}")
        
        finally:
          conn.close() #Close connection to database
    
    def get_last_course_name(self):
                conn = sqlite3.connect('cascade_project.db')
                cursor = conn.cursor()
                # Query the database to get the most recent course
                cursor.execute("SELECT name FROM courses ORDER BY ROWID DESC LIMIT 1")
                row = cursor.fetchone()
                conn.close()

                # Return the course if found, otherwise return None
                if row:
                   
                   return row[0]
                else:
                   return "Test Course"
    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = ProficiencyDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("Proficiency level:", dialog.get_proficiency())
    sys.exit(app.exec_())