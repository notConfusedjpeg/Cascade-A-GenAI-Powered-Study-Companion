from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import os
import resourcesCascade
import note_editor
import datetime

Predefined_folder = r"data\notepad_data"
class Ui_notepad(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 580)
        MainWindow.setStyleSheet("background-color: rgb(36, 13, 77);\n"
                                 "color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bgl = QtWidgets.QLabel(self.centralwidget)
        self.bgl.setGeometry(QtCore.QRect(0, -90, 771, 761))
        self.bgl.setText("")
        self.bgl.setPixmap(QtGui.QPixmap(":/images/images for cascade/notesbg.png"))
        self.bgl.setObjectName("bgl")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 771, 731))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.notes_title = QtWidgets.QLabel(self.frame)
        self.notes_title.setGeometry(QtCore.QRect(270, 10, 211, 71))
        self.notes_title.setStyleSheet("color: rgb(167, 145, 203);\n"
                                       "background-color: rgb(255, 255, 255,0);\n"
                                       "font: 40pt \"Montserrat\";\n"
                                       "font-weight: bold;\n"
                                       "")
        self.notes_title.setObjectName("notes_title")
        self.notes_title.setText("Notes")

        self.add_note_button = QtWidgets.QPushButton(self.frame)
        self.add_note_button.setGeometry(QtCore.QRect(320, 77, 41, 51))
        self.add_note_button.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.add_note_button.setText("")
        icon2 = QtGui.QIcon(":/images/images for cascade/create_note_icon.png")
        self.add_note_button.setIcon(icon2)
        self.add_note_button.setIconSize(QtCore.QSize(34, 34))
        self.add_note_button.setObjectName("add_note_button")
        self.add_note_button.clicked.connect(self.add_note)

        self.delete_note_button = QtWidgets.QPushButton(self.frame)
        self.delete_note_button.setGeometry(QtCore.QRect(378, 77, 41, 51))
        self.delete_note_button.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.delete_note_button.setText("")
        icon1 = QtGui.QIcon(":/images/images for cascade/delete_note_icon.png")
        self.delete_note_button.setIcon(icon1)
        self.delete_note_button.setIconSize(QtCore.QSize(34, 34))
        self.delete_note_button.setObjectName("delete_note_button")
        self.delete_note_button.clicked.connect(self.prepare_delete_notes)

        self.edit_note_button = QtWidgets.QPushButton(self.frame)
        self.edit_note_button.setGeometry(QtCore.QRect(430, 77, 41, 51))
        self.edit_note_button.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.edit_note_button.setText("")
        icon = QtGui.QIcon(":/images/images for cascade/edit_note_icon.png")
        self.edit_note_button.setIcon(icon)
        self.edit_note_button.setIconSize(QtCore.QSize(37, 37))
        self.edit_note_button.setObjectName("edit_note_button")
        self.edit_note_button.clicked.connect(self.open_notepad)

        self.listWidget = QtWidgets.QListWidget(self.frame)
        self.listWidget.setGeometry(QtCore.QRect(20, 150, 471, 461))
        self.listWidget.setStyleSheet("QScrollArea {\n"
                                      "    background-color: rgb(0, 0, 0,0.3);\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar:vertical {\n"
                                      "    border: none;\n"
                                      "    background: transparent;\n"
                                      "    width: 10px; \n"
                                      "    margin: 0px 0px 0px 0px;\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::handle:vertical {\n"
                                      "    background-color: rgb(167, 145, 203);\n"
                                      "    min-height: 10px;\n"
                                      "    border-radius: 4px;\n"
                                      "}\n"
                                      "QScrollBar::handle:vertical:hover{\n"
                                      "    background-color: rgb(129, 113, 158);\n"
                                      "}\n"
                                      "QScrollBar::handle:vertical:pressed {    \n"
                                      "    background-color: rgb(158, 121, 203);\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::sub-line:vertical {\n"
                                      "    border: none;\n"
                                      "    background-color: rgb(167, 145, 203);\n"
                                      "    height: 0px;\n"
                                      "    border-top-left-radius: 7px;\n"
                                      "    border-top-right-radius: 7px;\n"
                                      "    subcontrol-position: top;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::sub-line:vertical:hover {    \n"
                                      "    background-color: rgb(129, 113, 158);\n"
                                      "}\n"
                                      "QScrollBar::sub-line:vertical:pressed {    \n"
                                      "    background-color: rgb(158, 121, 203);\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::add-line:vertical {\n"
                                      "    border: none;\n"
                                      "    background-color: rgb(167, 145, 203);\n"
                                      "    height: 0px;\n"
                                      "    border-bottom-left-radius: 7px;\n"
                                      "    border-bottom-right-radius: 7px;\n"
                                      "    subcontrol-position: bottom;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::add-line:vertical:hover {    \n"
                                      "    background-color: rgb(129, 113, 158);\n"
                                      "}\n"
                                      "QScrollBar::add-line:vertical:pressed {    \n"
                                      "    background-color: rgb(158, 121, 203);\n"
                                      "}\n"
                                      "\n"
                                      "QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                      "    background: none;\n"
                                      "}\n"
                                      "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                      "    background: none;\n"
                                      "}\n"
                                      "")
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setSpacing(8)
        self.listWidget.setObjectName("listWidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 507, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

       
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connecting itemClicked signal to open_notepad slot
        self.load_notes()

    def add_note(self):
        text, ok = QtWidgets.QInputDialog.getText(None, "Add Note", "Note:")
        if ok and text:
            self.listWidget.addItem(text)
            self.save_content(text)

    def prepare_delete_notes(self):
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
        self.delete_note_button.setText("Confirm Delete")
        self.delete_note_button.clicked.disconnect()
        self.delete_note_button.clicked.connect(self.delete_notes)

    def delete_notes(self):
        for index in reversed(range(self.listWidget.count())):
            item = self.listWidget.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                self.listWidget.takeItem(index)
        self.delete_note_button.setText("Delete")
        self.delete_note_button.clicked.disconnect()
        self.delete_note_button.clicked.connect(self.prepare_delete_notes)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon(":/images/images for cascade/notes_icon.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle(_translate("MainWindow", "Notepad"))

    
    def open_notepad(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            # Extract only the note name (before the spaces)
            note_name = current_item.text().split(" ")[0] 
            note_path = os.path.join(Predefined_folder, f"{note_name}.txt")
            subprocess.Popen(["python", "note_editor.py", note_path])


    def save_content(self, note_name):
        notes_dir = os.path.join(os.getcwd(), Predefined_folder)
        os.makedirs(notes_dir, exist_ok=True)
        note_path = os.path.join(notes_dir, f"{note_name}.txt")
        with open(note_path, "w") as f:
            f.write("")

    def load_notes(self):
        self.listWidget.clear()
        now = datetime.datetime.now()

        for filename in os.listdir(Predefined_folder):
            if filename.endswith(".txt"):
                note_name = os.path.splitext(filename)[0]
                note_path = os.path.join(Predefined_folder, filename)
                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(note_path))
                time_diff = now - last_modified

                seconds = time_diff.total_seconds()
                if seconds < 60:
                    time_ago = "Few seconds ago"
                elif seconds < 3600:  # Less than an hour
                    minutes = int(seconds // 60)
                    time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
                elif seconds < 86400:  # Less than a day
                    hours = int(seconds // 3600)
                    time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
                else: 
                    days = int(seconds // 86400)
                    time_ago = f"{days} day{'s' if days > 1 else ''} ago"

                # Create a custom list item for better formatting
                item = QtWidgets.QListWidgetItem()
                # Assuming your QListWidget has enough width to display the text
                item.setText(f"{note_name:<65}{time_ago:>5}")  # Adjust spacing as needed

                self.listWidget.addItem(item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Windows")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_notepad()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
