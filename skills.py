from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QToolTip, QLabel
from PyQt5.QtGui import QPixmap, QFont
import sqlite3
import resourcesCascade

class TooltipLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.ToolTip)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("background-color: #1C0A39; border: 1px solid black; padding: 0px;")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def showTooltip(self, image_path, pos):
        pixmap = QPixmap(image_path)
        
        # Define the maximum size for the tooltip
        max_width = 200
        max_height = 250
        
        # Scale the pixmap to fit within the defined dimensions while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(max_width, max_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        
        self.setPixmap(scaled_pixmap)
        self.resize(scaled_pixmap.size())  # Resize the label to match the scaled pixmap size
        self.move(pos)
        self.show()

class Ui_skills(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1211, 814)
        MainWindow.setStyleSheet("background-color: rgb(27, 32, 81);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background Label
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 1211, 801))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(":/images/images for cascade/bg_image.png"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")

        # Main Box 1
        self.main_box_1 = QtWidgets.QLabel(self.centralwidget)
        self.main_box_1.setGeometry(QtCore.QRect(70, 50, 1061, 671))
        self.main_box_1.setStyleSheet("border-radius: 13px;\n"
                                      "background-color: rgba(0, 0, 0, 0.6);")
        self.main_box_1.setText("")
        self.main_box_1.setObjectName("main_box_1")

        # Main Box 2
        self.main_box_2 = QtWidgets.QLabel(self.centralwidget)
        self.main_box_2.setGeometry(QtCore.QRect(110, 140, 981, 531))
        self.main_box_2.setStyleSheet("border-radius: 13px;\n"
                                      "background-color: rgba(81, 58, 147, 0.5);")
        self.main_box_2.setText("")
        self.main_box_2.setObjectName("main_box_2")

        # Skills Title
        self.skills_title = QtWidgets.QLabel(self.centralwidget)
        self.skills_title.setGeometry(QtCore.QRect(960, 60, 201, 71))
        self.skills_title.setStyleSheet("color: rgb(167, 145, 203);\n"
                                        "background-color: rgba(255, 255, 255, 0);\n"
                                        "font: 27pt 'Montserrat';\n"
                                        "font-weight: bold;\n")
        self.skills_title.setObjectName("skills_title")

        # Current Skills Title
        self.currentskills_title = QtWidgets.QLabel(self.centralwidget)
        self.currentskills_title.setGeometry(QtCore.QRect(250, 140, 341, 71))
        self.currentskills_title.setStyleSheet("color: rgb(167, 145, 203);\n"
                                               "background-color: rgba(255, 255, 255, 0);\n"
                                               "font: 20pt 'Montserrat';\n")
        self.currentskills_title.setObjectName("currentskills_title")

        # Proficiency Title
        self.proficiency_title = QtWidgets.QLabel(self.centralwidget)
        self.proficiency_title.setGeometry(QtCore.QRect(740, 140, 341, 71))
        self.proficiency_title.setStyleSheet("color: rgb(167, 145, 203);\n"
                                             "background-color: rgba(255, 255, 255, 0);\n"
                                             "font: 20pt 'Montserrat';\n")
        self.proficiency_title.setObjectName("proficiency_title")

        # Line Separator
        self.line = QtWidgets.QLabel(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(140, 210, 921, 1))
        self.line.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.line.setText("")
        self.line.setObjectName("line")

        # Scroll Area
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(140, 230, 921, 411))
        self.scrollArea.setStyleSheet("background-color: transparent;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # Scroll Area Widget Contents
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 919, 409))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        # Grid Layout for Skills and Proficiency
        self.gridLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 670, 369))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.tooltip_label = TooltipLabel(MainWindow)

        self.help = QtWidgets.QLabel(self.centralwidget)
        self.help.setGeometry(QtCore.QRect(950, 170, 29, 29))
        self.help.setStyleSheet("QLabel {"  # Target QLabel
            "    background-color: transparent; "  # Keep background transparent
            "    border-radius: 13px; "
            "    font: 10pt 'Monteserrat'; "
            "    color:rgb(149, 145, 203); "
            "}")
        self.help.setObjectName("help")
        self.help.enterEvent = lambda event: self.show_help_tooltip(event)
        self.help.leaveEvent = lambda event: QToolTip.hideText()

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1211, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Populate skills and proficiency levels
        self.populate_skills_and_proficiency()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon(":/images/images for cascade/dark_study_icon.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle(_translate("MainWindow", "Skills"))
        self.skills_title.setText(_translate("MainWindow", "Skills"))
        self.currentskills_title.setText(_translate("MainWindow", "Current Skills"))
        self.proficiency_title.setText(_translate("MainWindow", "Proficiency"))
        self.help.setText(_translate("MainWindow", "?"))

    def show_help_tooltip(self, event):
        image_path = ":/images/images for cascade/instructions.png"
        self.tooltip_label.showTooltip(image_path, event.globalPos())

    def populate_skills_and_proficiency(self):
        connection = sqlite3.connect("cascade_project.db")
        cursor = connection.cursor()

        cursor.execute("SELECT skill, points FROM skills_points")
        skills_points = cursor.fetchall()

        skill_labels = []
        proficiency_labels = []

        for i, (skill, points) in enumerate(skills_points):
            skill_label = QtWidgets.QLabel(self.gridLayoutWidget)
            skill_label.setText(skill)
            skill_label.setStyleSheet("font: 18pt 'Montserrat'; color: rgb(167, 145, 203);")
            skill_labels.append(skill_label)

            proficiency_label = QtWidgets.QLabel(self.gridLayoutWidget)
            proficiency_label.setFixedSize(30, 30)  # Set a fixed size for the image labels
            proficiency_label.setScaledContents(True)
            
            proficiency_image = self.get_proficiency_image(points)
            print(f"Skill: {skill}, Points: {points}, Image: {proficiency_image}")  # Debug output

            proficiency_label.setPixmap(QtGui.QPixmap(proficiency_image))

            proficiency_labels.append(proficiency_label)

            self.gridLayout.addWidget(skill_label, i, 0)
            self.gridLayout.addWidget(proficiency_label, i, 1)

        connection.close()

    def get_proficiency_image(self, points):
        if 0 <= points < 100:
            return ":/images/images for cascade/Beginner.png"
        elif 100 <= points < 200:
            return ":/images/images for cascade/Basic.png"
        elif 200 <= points < 300:
            return ":/images/images for cascade/Intermediate.png"
        elif 300 <= points < 400:
            return ":/images/images for cascade/Advance.png"
        elif points >= 400:
            return ":/images/images for cascade/Master.png"
        return ""  # Default case if no image path is matched

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_skills()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
