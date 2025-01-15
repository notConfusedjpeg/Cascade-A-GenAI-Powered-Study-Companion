import sys
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QDialog
import datetime
import sqlite3
import resourcesCascade

class Ui_Statistics(QMainWindow):
    def __init__(self):
        
        super().__init__()
        icon = QtGui.QIcon(":/images/images for cascade/Cascade-removebg-preview.png")
        self.setWindowIcon(icon)
        self.setWindowTitle("Statistics")

        # Create a QHBoxLayout instance for the main layout
        main_layout = QHBoxLayout()

        # Create a QVBoxLayout instance for the vertical graphs
        vertical_layout = QVBoxLayout()

        # Create bar graph widgets
        self.vertical_bar_graph1 = pg.PlotWidget()
        self.vertical_bar_graph2 = pg.PlotWidget()
        self.horizontal_bar_graph = pg.PlotWidget()

        # Add vertical bar graph widgets to the vertical layout
        vertical_layout.addWidget(self.vertical_bar_graph1)
        vertical_layout.addWidget(self.vertical_bar_graph2)

        # Add the vertical layout and the horizontal bar graph widget to the main layout
        main_layout.addLayout(vertical_layout)
        main_layout.addWidget(self.horizontal_bar_graph)

        # Create a QLabel widget for displaying most/least studied subjects
        self.subject_info_label = QLabel()
        self.subject_info_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.subject_info_label.setWordWrap(True)  # Allow text to wrap

        # Generate data for the bar graphs
        self.generate_data()

        # Set titles for the bar graphs
        self.vertical_bar_graph1.setTitle("Hours Spent ")
        self.vertical_bar_graph2.setTitle("Most focused daily")
        self.horizontal_bar_graph.setTitle("Day Streak")

        # Set up the layout for the subject info label
        info_layout = QVBoxLayout()
        info_layout.addWidget(self.subject_info_label)
        info_widget = QWidget()
        info_widget.setLayout(info_layout)
        main_layout.addWidget(info_widget)

        # Set the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def generate_data(self):
        conn = sqlite3.connect('cascade_project.db')
        conn.row_factory = sqlite3.Row

        # Data for the bar graphs
        subjects = self.display_courses()
        y1 = self.display_time()

        days= self.display_day()
        y2 = self.display_time2()
        # Create bar graph items for vertical bar graphs
        bar_graph_item1 = pg.BarGraphItem(x=list(range(len(subjects))), height=y1, width=0.6, brush='r')
        bar_graph_item2 = pg.BarGraphItem(x=list(range(len(days))), height=y2, width=0.6, brush='b')

        # Add bar graph items to the vertical plot widgets
        self.vertical_bar_graph1.addItem(bar_graph_item1)
        self.vertical_bar_graph2.addItem(bar_graph_item2)

        # Create a bar graph item for the horizontal bar graph
        bar_graph_item3 = pg.BarGraphItem(x0=[0]*len(subjects), y=list(range(len(subjects))), height=0.6, width=y1, brush='g')
        self.horizontal_bar_graph.addItem(bar_graph_item3)

        # Set the x-axis labels for the vertical bar graphs
        self.vertical_bar_graph1.getAxis('bottom').setTicks([list(zip(range(len(subjects)), subjects))])
        self.vertical_bar_graph2.getAxis('bottom').setTicks([list(zip(range(len(days)), days))])

        # Set the y-axis labels for the horizontal bar graph
        self.horizontal_bar_graph.getAxis('left').setTicks([list(zip(range(len(subjects)), subjects))])

        cursor = conn.cursor()        

        # Example: Set most/least studied subjects
        try:
            cursor.execute("SELECT subject FROM timer ORDER BY time DESC LIMIT 1;")
            most_subject = cursor.fetchone()
            most_studied_subject = most_subject[0] if most_subject else 'N/A'

            cursor.execute("SELECT subject FROM timer ORDER BY time LIMIT 1;")
            least_subject = cursor.fetchone()
            least_studied_subject = least_subject[0] if least_subject else 'N/A'

            cursor.execute("SELECT day FROM time_per_day ORDER BY time DESC LIMIT 1;")
            most_focused = cursor.fetchone()
            most_focused_day = most_focused[0] if most_focused else 'N/A'

            cursor.execute("SELECT day FROM time_per_day ORDER BY time LIMIT 1;")
            least_focused = cursor.fetchone()
            least_focused_day = least_focused[0] if least_focused else 'N/A'
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            most_studied_subject = least_studied_subject = 'N/A'
            most_focused_day = least_focused_day = 'N/A'
        finally:
            cursor.close()
            conn.close()

        self.subject_info_label.setText(f"<b>Most Studied Subject:</b> {most_studied_subject}<br><b>Least Studied Subject:</b> {least_studied_subject}<br><b>Most Focused Day:</b> {most_focused_day}<br><b>Least Focused Day:</b> {least_focused_day}")


    def display_courses(self):
        conn = sqlite3.connect('cascade_project.db')
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM courses")
        course_name = cursor.fetchall()
        course_list = [row['name'] for row in course_name]

        cursor.close()
        conn.close()

        return course_list

    def display_time(self):
        conn = sqlite3.connect('cascade_project.db')
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT time FROM timer")
        course_time = cursor.fetchall()
        time_list = [row['time'] for row in course_time]

        cursor.close()
        conn.close()

        return time_list
    
    def display_day(self):
        # Connect to the database
        conn = sqlite3.connect('cascade_project.db')
        
        # Fetch the days from the table
        cursor = conn.cursor()
        cursor.execute("SELECT day FROM time_per_day")
        days = cursor.fetchall()
        days_list = [day[0] for day in days]  # Directly use the string without strftime

        cursor.close()
        conn.close()

        return days_list

    
    def display_time2(self):
        # Connect to the database
        conn = sqlite3.connect('cascade_project.db')
        
        # Fetch the days from the table
        cursor = conn.cursor()
        cursor.execute("SELECT time FROM time_per_day")
        time2 = cursor.fetchall()
        time2_list=[]
                
        for i in range(len(time2)):
                time2_list.append(time2[i][0])

        cursor.close()
        conn.close()

        return(time2_list)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Ui_Statistics()
    main.show()
    sys.exit(app.exec_())
