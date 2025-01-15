from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import resourcesCascade


class TooltipLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.ToolTip)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("background-color: #1C0A39; border: 1px solid black; padding: 0px;")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def showTooltip(self, pixmap, pos):
        self.setPixmap(pixmap)
        self.resize(pixmap.size())  # Resize the label to match the pixmap size
        self.move(pos)
        self.show()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1039, 765)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 1041, 731))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(":images/images for cascade/Roadmapv2.png"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")

        # Create custom tooltip label
        self.tooltip_label = TooltipLabel(MainWindow)

        self.labels = {
            "BM": (200, 340, ":/images/images for cascade/Frame 50.png"),
            "stats": (430, 350, ":/images/images for cascade/Frame 51.png"),
            "calculus": (680, 340, ":/images/images for cascade/Frame 52.png"),
            "eco": (800, 470, ":/images/images for cascade/Frame 53.png"),
            "regression": (610, 470, ":/images/images for cascade/Frame 54.png"),
            "ATA": (470, 470, ":/images/images for cascade/Frame 55.png"),
            "precoding": (90, 470, ":/images/images for cascade/Frame 56.png"),
            "python": (180, 560, ":/images/images for cascade/Frame 57.png"),
            "Rprog": (300, 560, ":/images/images for cascade/Frame 58.png"),
            "EDA": (460, 560, ":/images/images for cascade/Frame 59.png"),
            "DL": (680, 560, ":/images/images for cascade/Frame 60.png"),
            "MLOps": (840, 560, ":/images/images for cascade/Frame 61.png"),
        }

        for name, (x, y, image_path) in self.labels.items():
            label = QtWidgets.QLabel(self.centralwidget)
            label.setGeometry(QtCore.QRect(x, y, 55, 41))
            label.setText("")
            label.setObjectName(name)
            label.enterEvent = lambda event, img=image_path, lbl=label: self.show_tooltip(event, img, lbl)
            label.leaveEvent = lambda event: self.hide_tooltip()
            setattr(self, name, label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1039, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon(":/images/images for cascade/Cascade-removebg-preview.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def show_tooltip(self, event, image_path, widget):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(200, 250, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.tooltip_label.showTooltip(scaled_pixmap, event.globalPos())

    def hide_tooltip(self):
        self.tooltip_label.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
