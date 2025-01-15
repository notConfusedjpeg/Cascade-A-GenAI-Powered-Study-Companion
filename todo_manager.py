import datetime
import sys
from PyQt5 import QtCore, QtWidgets

class TodoManager:
    def __init__(self, checkboxes, todos):
        self.checkboxes = checkboxes
        self.todos = todos

        # Connect checkboxes to the corresponding todo items
        for checkbox, todo in zip(self.checkboxes, self.todos):
            checkbox.stateChanged.connect(lambda state, todo=todo, checkbox=checkbox: self.toggle_todo_strike(todo, checkbox))

        # Schedule midnight cleanup
        self.cleanup_timer = QtCore.QTimer()
        self.cleanup_timer.timeout.connect(self.cleanup_todos)
        self.cleanup_timer.start(1000)  # Check every second for midnight

    def toggle_todo_strike(self, todo, checkbox):
        if checkbox.isChecked():
            todo.setStyleSheet("text-decoration: line-through;  background-color: rgb(255, 255, 255,0); color: rgb(195, 195, 195); font: 10pt")
        else:
            todo.setStyleSheet("text-decoration: none; background-color: rgb(255, 255, 255,0); color: rgb(195, 195, 195);")

    def cleanup_todos(self):
        now = datetime.datetime.now()
        midnight = datetime.datetime(now.year, now.month, now.day, 0, 0)
        if now.time() >= datetime.time(23, 59, 59) or now.time() < datetime.time(0, 0, 0):
            for checkbox, todo in zip(self.checkboxes, self.todos):
                if checkbox.isChecked():
                    todo.clear()
                    checkbox.setChecked(False)
                    todo.setStyleSheet("text-decoration: none; color: rgb(195, 195, 195);")