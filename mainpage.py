# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
import sys
import os
import ctypes
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout,QLabel, QDialog, QToolTip,QListWidgetItem
from PyQt5.QtGui import QIcon,QPixmap, QFont
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import subprocess
import resourcesCascade
import tkinter as tk
from aboutus import Ui_aboutus
from todo_manager import TodoManager
from timer import Ui_Timer
from Notepad import Ui_notepad
from statspage import Ui_Statistics
import settings
from PyQt5.QtCore import Qt
from musicplayer import MusicPlayer
from study_plan import Ui_study_plan
from aichatbot import get_gemini_response
from roadmap import Ui_MainWindow
from skills import Ui_skills
import google.generativeai as genai
import sqlite3
import json
from daily_schedule import Ui_daily_schedule
from quiz import Ui_quiz

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(script):
    if not is_admin():
        try:
            params = ' '.join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1)
        except:
            print("Failed to elevate privileges.")
        sys.exit(1)
    return True


genai.configure(api_key="AIzaSyCE2UcROTOZT9YujfGizIrNfGf8zDJ4zmY")

class Ui_mainpage(object):
    def openIntro(self, event):
        if event.button() == Qt.LeftButton:  # Handling left mouse button click
            # Run the Tkinter app in a separate process
            subprocess.Popen(['python', 'introduction.py'])

    def openContact(self, event):
        if event.button() == Qt.LeftButton:  # Handling left mouse button click
            # Run the Tkinter app in a separate process
            subprocess.Popen(['python', 'contact_us.py'])

    def openNotesViewer(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_notepad()
        self.ui.setupUi(self.window)
        self.window.show()

    def openDailySchedule(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_daily_schedule()
        self.ui.setupUi(self.window)
        self.window.show()

    def openQuiz(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_quiz()
        self.ui.setupUi(self.window)
        self.window.show()

    def openSettings(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = settings.Ui_settings(self.window)
        self.ui.setupUi(self.window)
        self.window.show() 

    def openSkills(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_skills()
        self.ui.setupUi(self.window)
        self.window.show()

    def openStatisticsPage(self,event):
        if event.button() == Qt.LeftButton:  # Handling left mouse button click
            self.window = Ui_Statistics()
            self.window.show()

    def openStatsTest(self, event):
        if event.button() == Qt.LeftButton:  # Handling left mouse button click
            # Run the Tkinter app in a separate process
            subprocess.Popen(['python', 'statspage_test.py'])

    def openStudyPlan(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_study_plan()
        self.ui.setupUi(self.window)
        self.window.show()

    def openAboutus(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_aboutus()
        self.ui.setupUi(self.window)
        self.window.show()

    def openFlashcards(self, event):
        if event.button() == Qt.LeftButton:  # Handling left mouse button click
            # Run the Tkinter app in a separate process
            subprocess.Popen(['python', 'flashcard.py'])


    def start_music_player(self):
        self.music_player = MusicPlayer()
        self.music_player.show()

    def openRoadmap(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, mainpage):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        # Creating table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                name TEXT,
                syllabus TEXT,
                skills_gained TEXT,
                initial_user_said_score INTEGER,
                initial_user_assessment_score INTEGER,
                final_user_assessment_score INTEGER
            )
        """)
                       
        cursor.execute("""CREATE TABLE IF NOT EXISTS study_plan
                        (name TEXT, plan TEXT DEFAULT NULL, study_period TEXT, avail TEXT)"""
                       )
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_choice (id INTEGER, domain TEXT)''')
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS domains (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT,
        skills TEXT
        )
        """)

        cursor.execute("SELECT COUNT(*) FROM domains")
        count_domain = cursor.fetchone()[0]

        cursor.execute('''
CREATE TABLE IF NOT EXISTS skills_points (
    skill TEXT PRIMARY KEY,
    points INTEGER DEFAULT 0
)
''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Achievements (
    achievement_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Ensures unique IDs
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    icon_path TEXT,
    is_unlocked INTEGER DEFAULT 0,
    description TEXT,  
    popup TEXT,              
    current_progress TEXT          
)''')
        cursor.execute("SELECT COUNT(*) FROM Achievements")
        count_achieve = cursor.fetchone()[0]

        if count_achieve == 0:
                achievements_data = []

                # Daily Streaks
                for i, streak in enumerate([5, 10, 15, 20, 30, 60, 90, 150, 300, 365]):
                        achievements_data.append({
                                "name": f"{streak} Day Streak",
                                "type": "daily_streak",
                                "icon_path": os.path.join("data", "assets", "daily_streaks", "unlocked", f"image_{i}.png"),  # Adjust file extensions
                                "description": f"Maintain a daily streak of {streak} days!",
                                "popup": f"Congratulations on maintaining a {streak} day streak!"
                        })


                # Quiz Streaks
                for i, streak in enumerate([5, 10, 15, 30, 50, 75, 100, 200]):
                        achievements_data.append({
                                "name": f"{streak} Quizzes Attempted",
                                "type": "quiz_streak",
                                "icon_path": os.path.join("data", "assets", "quiz_streaks", "unlocked", f"image_{i}.png"),  # Add icon paths if available
                                "description": f"Test your knowledge by attempting {streak} quizzes!",
                                "popup": f"You have attempted {streak} quizzes!"
                        })


                proficiencies = ["Beginner", "Basic", "Intermediate", "Advanced", "Master"]
                i = 0  # Initialize i
                for proficiency in proficiencies: #outer proficiency loop now
                        for count in [5, 10, 15]: # inner count loop now
                                achievements_data.append({
                                "name": f"{count} {proficiency} Skills",
                                "type": "skills_developed",
                                "icon_path": os.path.join("data", "assets", "skills_developed", "unlocked", f"image_{i}.png"),
                                "description": f"Develop {count} skills to {proficiency} level",
                                "popup": f"You have developed {count} {proficiency} level skills!" 
                                })
                                i += 1



                # Courses Completed
                i=0
                for count in [1, 5, 10, 15, 30, 50, 75, 100]:
                        achievements_data.append({
                                "name": f"{count} Courses Completed",
                                "type": "courses_completed",
                                "icon_path": os.path.join("data", "assets", "courses_completed", "unlocked", f"image_{i}.png"),
                                "description": f"Broaden your horizons by completing {count} courses!",
                                "popup": f"You have completed {count} courses!"
                        })
                        i=i+1

                # Misc Achievements
                misc_achievements = [
                {"name": "Study Marathoner", "type": "misc", "icon_path": os.path.join("data", "assets", "misc", "unlocked", f"image_1.png"), "description": "Study for 10 hours in a single week", "popup": "You've studied for 10 hours in a single week!"},
                {"name": "To-do Crusher", "type": "misc", "icon_path": os.path.join("data", "assets", "misc", "unlocked", f"image_2.png"), "description": "Achieve 10 study goals within a day", "popup": "You've crushed 10 study goals in a day!"},
                {"name": "Music Maestro", "type": "misc", "icon_path": os.path.join("data", "assets", "misc", "unlocked", f"image_3.png"), "description": "Play 25 different songs", "popup": "You are a true Music Maestro!"}
                ]
                achievements_data.extend(misc_achievements)


                # Master at Domains
                i=0
                domains = ["Computer Science", "Mathematics", "Physics", "Commerce", "Biology"]
                for domain in domains:
                        achievements_data.append({
                                "name": f"Master of {domain}",
                                "type": "domain_master",
                                "icon_path": os.path.join("data", "assets", "domain_master", "unlocked", f"image_{i}.png"),  # Add icon path
                                "description": f"Master all skills in {domain}",
                                "popup": f"You are a master of {domain}!"
                        })
                        i=i+1

                # Insert data using executemany for efficiency
                cursor.executemany("INSERT INTO Achievements (name, type, icon_path, description, popup) VALUES (:name, :type, :icon_path, :description, :popup)", achievements_data)
                conn.commit()

        cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_limit INTEGER NOT NULL,
    quiz TEXT NOT NULL,
    marks INTEGER NOT NULL,
    date_taken TEXT NOT NULL
)''')

        if count_domain == 0: 
                # Inserting data
                domains = {
                "Computer Science": [
                        "Mathematics", "Machine Learning", "Cybersecurity", "Graphic & Engineering Design", "Web Development",
                        "Full Stack Development", "Backend Development", "Frontend Development", "Python", "C", "C++", "Java",
                        "Data Science", "Problem Solving", "Data Structures and Algorithms", "Database Management", "Electronics",
                        "Operating Systems"
                ],
                "Mathematics": [
                        "Calculus", "Linear Algebra", "Probability and Statistics", "Differential Equations", "Number Theory",
                        "Abstract Algebra", "Mathematical Modeling", "Numerical Analysis", "Topology", "Graph Theory",
                        "Mathematical Logic", "Complex Analysis", "Optimization", "Proof Writing", "Mathematical Software",
                        "Discrete Mathematics", "Mathematical History", "Mathematical Communication"
                ],
                "Physics": [
                        "Advanced Calculus", "Linear Algebra", "Quantum Mechanics", "Classical Mechanics", "Electromagnetism",
                        "Thermodynamics", "Statistical Mechanics", "Nuclear Physics", "Solid State Physics", "Optics",
                        "Particle Physics", "Astrophysics", "Computational Physics", "Experimental Techniques",
                        "Mathematical Methods in Physics", "Scientific Programming", "Data Analysis", "Physical Modeling",
                        "Quantitative Reasoning", "Research Methodology"
                ],
                "Architecture": [
                        "Architectural Design", "Building Construction", "Architectural History", "Urban Planning",
                        "Sustainable Architecture", "Interior Design", "Structural Engineering", "Environmental Science",
                        "Site Planning", "Materials and Technology", "Building Codes and Regulations", "3D Modeling and Visualization",
                        "Architectural Communication", "Project Management", "Cultural Context in Architecture", "Professional Ethics",
                        "Spatial Analysis", "Landscape Architecture", "Lighting Design", "Acoustics"
                ],
                "Humanities and Art": [
                        "Critical Thinking", "Research and Writing", "Cultural Studies", "Literary Analysis", "Art History",
                        "Philosophy", "Ethics", "Visual Arts", "Music and Performing Arts", "Gender Studies", "History of Ideas",
                        "Aesthetics", "Creative Expression", "Interdisciplinary Approaches", "Media Studies", "Comparative Literature",
                        "Film Studies", "Theater and Drama", "Digital Humanities", "Social Sciences"
                ],
                "Chemistry": [
                        "Inorganic Chemistry", "Organic Chemistry", "Physical Chemistry", "Analytical Chemistry", "Biochemistry",
                        "Quantum Chemistry", "Spectroscopy", "Chemical Kinetics", "Thermodynamics", "Laboratory Techniques",
                        "Materials Science", "Environmental Chemistry", "Medicinal Chemistry", "Computational Chemistry",
                        "Chemical Safety", "Chemical Engineering", "Polymer Chemistry", "Surface Chemistry", "Nuclear Chemistry",
                        "Chemical Education"
                ],
                "Biology": [
                        "Cell Biology", "Genetics", "Ecology", "Evolutionary Biology", "Physiology", "Microbiology", "Molecular Biology",
                        "Bioinformatics", "Biostatistics", "Immunology", "Plant Biology", "Animal Behavior", "Neuroscience",
                        "Environmental Science", "Research Methods in Biology", "Biotechnology", "Conservation Biology",
                        "Marine Biology", "Health Sciences", "Fieldwork and Data Collection"
                ],
                "Commerce": [
                        "Accounting", "Financial Management", "Taxation", "Auditing", "Business Law", "Economics", "Marketing",
                        "Business Communication", "Financial Analysis", "Cost Accounting"
                ],
                "Business Administration": [
                        "Management Principles", "Organizational Behavior", "Marketing Management", "Human Resource Management",
                        "Financial Management", "Business Ethics", "Strategic Planning", "Entrepreneurship", "Leadership Skills",
                        "Project Management"
                ],
                "Design": [
                        "Design Thinking", "Visual Communication", "User Experience (UX) Design", "Typography", "Color Theory", "Product Design",
                        "Digital Illustration", "Prototyping", "Design Research", "Creative Problem-Solving"
                ],
                "Civil Engineering": [
                        "Structural Engineering", "Geotechnical Engineering", "Construction Management", "Surveying and Geomatics",
                        "Transportation Engineering", "Hydraulics and Water Resources", "Environmental Engineering",
                        "Concrete Technology", "Project Planning and Estimation", "AutoCAD and Civil Design Software"
                ],
                "Mechanical Engineering": [
                        "Thermodynamics", "Fluid Mechanics", "Strength of Materials", "Machine Design", "Heat Transfer",
                        "Manufacturing Processes", "CAD/CAM (Computer-Aided Design/Computer-Aided Manufacturing)", "Robotics and Automation",
                        "Materials Science", "Engineering Mechanics"
                ],
                "Electrical Engineering": [
                        "Circuit Analysis", "Electromagnetic Theory", "Power Systems", "Control Systems", "Digital Electronics",
                        "Microprocessors and Microcontrollers", "Electrical Machines", "Renewable Energy Systems", "Power Electronics",
                        "Instrumentation and Measurement"
                ],
                "Biotechnology": [
                        "Molecular Biology", "Genetic Engineering", "Bioinformatics", "Bioprocess Engineering", "Cell Culture Techniques",
                        "Immunology", "Biomedical Instrumentation", "Biochemistry", "Biostatistics", "Bioremediation"
                ],
                "Aerospace Engineering": [
                        "Aerodynamics", "Flight Mechanics", "Spacecraft Design", "Propulsion Systems", "Structural Analysis",
                        "Avionics and Navigation", "Materials for Aerospace", "Rocket Propulsion", "Space Exploration Technologies",
                        "Finite Element Analysis"
                ]
                }

                for domain, skills in domains.items():
                        cursor.execute("INSERT INTO domains (domain, skills) VALUES (?, ?)", (domain, json.dumps(skills)))
                conn.commit()


        conn.commit()
        cursor.close()
        conn.close()
        

        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        mainpage.setObjectName("mainpage")
        mainpage.resize(1211, 814)
        mainpage.setStyleSheet("background-color: rgb(27, 32, 81);")
        self.centralwidget = QtWidgets.QWidget(mainpage)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(-7, -10, 1221, 801))
        self.bg.setText("")
        self.bg.setPixmap(QPixmap(":/images/images for cascade/bg_image.png"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")
        self.logo_bg_shadow = QtWidgets.QLabel(self.centralwidget)
        self.logo_bg_shadow.setGeometry(QtCore.QRect(25, 25, 61, 61))
        self.logo_bg_shadow.setStyleSheet("background-color: rgb(23, 35, 67);\n"
"border-radius: 10px;\n"
"")
        self.logo_bg_shadow.setText("")
        self.logo_bg_shadow.setObjectName("logo_bg_shadow")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(20, 20, 61, 61))
        self.logo.setStyleSheet("background-color: rgb(99, 106, 154);\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"box-shadow: 10px 10px 5px rgba(0, 0, 0, 1);")
        self.logo.setText("")
        self.logo.setPixmap(QPixmap(":/images/images for cascade/Cascade-removebg-preview.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.nav_line = QtWidgets.QLabel(self.centralwidget)
        self.nav_line.setGeometry(QtCore.QRect(550, 60, 551, 1))
        self.nav_line.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.nav_line.setText("")
        self.nav_line.setObjectName("nav_line")
        self.intro_nav = QtWidgets.QLabel(self.centralwidget)
        self.intro_nav.setGeometry(QtCore.QRect(570, 20, 101, 41))
        self.intro_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.intro_nav.setObjectName("intro_nav")
        self.intro_nav.mousePressEvent = self.openIntro
        self.studyplan_nav = QtWidgets.QLabel(self.centralwidget)
        self.studyplan_nav.setGeometry(QtCore.QRect(680, 20, 81, 41))
        self.studyplan_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.studyplan_nav.setObjectName("studyplan_nav")
        self.studyplan_nav.mousePressEvent = lambda event: self.openStudyPlan()
        self.calender_nav = QtWidgets.QLabel(self.centralwidget)
        self.calender_nav.setGeometry(QtCore.QRect(770, 20, 71, 41))
        self.calender_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.calender_nav.setObjectName("calender_nav")
        self.stats_nav = QtWidgets.QLabel(self.centralwidget)
        self.stats_nav.setGeometry(QtCore.QRect(850, 20, 61, 41))
        self.stats_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.stats_nav.setObjectName("stats_nav")
        self.stats_nav.mousePressEvent = self.openStatsTest
        self.faq_nav = QtWidgets.QLabel(self.centralwidget)
        self.faq_nav.setGeometry(QtCore.QRect(930, 20, 41, 41))
        self.faq_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.faq_nav.setObjectName("faq_nav")
        self.about_nav = QtWidgets.QLabel(self.centralwidget)
        self.about_nav.setGeometry(QtCore.QRect(990, 20, 41, 41))
        self.about_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.about_nav.setObjectName("about_nav")
        self.about_nav.mousePressEvent = lambda event: self.openAboutus()
        self.contact_nav = QtWidgets.QLabel(self.centralwidget)
        self.contact_nav.setGeometry(QtCore.QRect(1050, 20, 51, 41))
        self.contact_nav.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"color: rgb(255, 255, 255);\n"
"font: 8pt \"Montserrat\";")
        self.contact_nav.setObjectName("contact_nav")
        self.contact_nav.mousePressEvent = self.openContact

        self.settings = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: [mainpage.hide(), self.openSettings()])        
        self.settings.setGeometry(QtCore.QRect(1120, 30, 31, 28))
        self.settings.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 14px;")
        
        self.settings.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(":/images/images for cascade/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings.setIcon(icon)
        self.settings.setObjectName("settings")
        self.help = QtWidgets.QPushButton(self.centralwidget)
        self.help.setGeometry(QtCore.QRect(1160, 30, 31, 28))
        self.help.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 14px;")
        self.help.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QPixmap(":/images/images for cascade/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon1)
        self.help.setObjectName("help")
        self.help.clicked.connect(self.start_music_player)
        self.music = QtWidgets.QPushButton(self.centralwidget)
        self.music.setGeometry(QtCore.QRect(1160, 70, 31, 28))
        self.music.setStyleSheet("background-color: rgb(0,0,0);\n"
"border-radius: 14px;")
        self.music.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QPixmap(":/images/images for cascade/icon-musical-notes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.music.setIcon(icon5)
        self.music.setIconSize(QtCore.QSize(40, 40))  
        self.music.setObjectName("music")
        self.music.clicked.connect(self.start_music_player)
        self.sidebar = QtWidgets.QLabel(self.centralwidget)
        self.sidebar.setGeometry(QtCore.QRect(-10, 170, 71, 451))
        self.sidebar.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(167, 145, 203,0.3);")
        self.sidebar.setText("")
        self.sidebar.setObjectName("sidebar")

        self.timer = QtWidgets.QLabel(self.centralwidget)
        self.timer.setGeometry(QtCore.QRect(10, 180, 41, 51))
        self.timer.setStyleSheet("QLabel { background-color: transparent; }\n"
                         "QToolTip { color: black; background-color: white; border: 1px solid black; }")

        self.timer.setText("")
        self.timer.setPixmap(QPixmap(":/images/images for cascade/timer_icon.png"))
        self.timer.setObjectName("timer")
        self.timer.setToolTip("Timer")
        QToolTip.setFont(QFont('Montserrat', 10))
        self.timer.mousePressEvent = lambda event: self.timer_clicked(event)


        self.daily_schedule = QtWidgets.QLabel(self.centralwidget)
        self.daily_schedule.setGeometry(QtCore.QRect(13, 309, 41, 51))
        self.daily_schedule.setStyleSheet("QLabel{ background-color: rgb(255, 255, 255,0);}\n"
                                          "QToolTip { color: black; background-color: white; border: 1px solid black; }")
        self.daily_schedule.setText("")
        self.daily_schedule.setPixmap(QPixmap(":/images/images for cascade/dailyScedule_icon.png"))
        self.daily_schedule.setObjectName("daily_schedule")
        self.daily_schedule.mousePressEvent = lambda event: self.openDailySchedule()
        self.daily_schedule.setToolTip("Daily Schedule")
        QToolTip.setFont(QFont('Montserrat', 10))

        self.flashcard = QtWidgets.QLabel(self.centralwidget)
        self.flashcard.setGeometry(QtCore.QRect(10, 245, 41, 51))
        self.flashcard.setStyleSheet("QLabel{ background-color: rgb(255, 255, 255,0);}\n"
                                          "QToolTip { color: black; background-color: white; border: 1px solid black; }")
        self.flashcard.setText("")
        self.flashcard.setPixmap(QPixmap(":/images/images for cascade/flashcard_icon.png"))
        self.flashcard.setObjectName("flashcard")
        self.flashcard.mousePressEvent = self.openFlashcards
        self.flashcard.setToolTip("Flashcards")
        QToolTip.setFont(QFont('Montserrat', 10))
        

        self.quiz = QtWidgets.QLabel(self.centralwidget)
        self.quiz.setGeometry(QtCore.QRect(17, 440, 41, 41))
        self.quiz.setStyleSheet("QLabel{ background-color: rgb(255, 255, 255,0);}\n"
                                          "QToolTip { color: black; background-color: white; border: 1px solid black; }")
        self.quiz.setText("")
        self.quiz.setPixmap(QPixmap(":/images/images for cascade/Quiz_icon.png"))
        self.quiz.setScaledContents(False)
        self.quiz.setObjectName("quiz")
        self.quiz.mousePressEvent = lambda event: self.openQuiz()
        self.quiz.setToolTip("Quiz")
        QToolTip.setFont(QFont('Montserrat', 10))
        self.sylabus_tracker = QtWidgets.QLabel(self.centralwidget)
        self.sylabus_tracker.setGeometry(QtCore.QRect(12, 374, 41, 51))
        self.sylabus_tracker.setStyleSheet("QLabel{ background-color: rgb(255, 255, 255,0);}\n"
                                          "QToolTip { color: black; background-color: white; border: 1px solid black; }")
        self.sylabus_tracker.setText("")
        self.sylabus_tracker.setPixmap(QPixmap(":/images/images for cascade/SyllabusTracker_icon.png"))
        self.sylabus_tracker.setObjectName("sylabus_tracker")
        self.sylabus_tracker.mousePressEvent = lambda event: self.openSkills()
        self.sylabus_tracker.setToolTip("Skills")
        QToolTip.setFont(QFont('Montserrat', 10))
        self.feedback = QtWidgets.QLabel(self.centralwidget)
        self.feedback.setGeometry(QtCore.QRect(10, 563, 41, 51))
        self.feedback.setStyleSheet("QLabel{ background-color: rgb(255, 255, 255,0);}\n"
                                          "QToolTip { color: black; background-color: white; border: 1px solid black; }")
        self.feedback.setText("")
        pixmap = QPixmap(":/images/images for cascade/roadmap_icon.png")
        scaled_pixmap = pixmap.scaled(self.feedback.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.feedback.setPixmap(scaled_pixmap)
        self.feedback.setObjectName("feedback")
        self.feedback.mousePressEvent = lambda event: self.openRoadmap()
        self.feedback.setToolTip("Roadmap")
        QToolTip.setFont(QFont('Montserrat', 10))
        self.sidebar_line_2 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_2.setGeometry(QtCore.QRect(10, 235, 41, 1))
        self.sidebar_line_2.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_2.setText("")
        self.sidebar_line_2.setObjectName("sidebar_line_2")
        self.sidebar_line_3 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_3.setGeometry(QtCore.QRect(10, 298, 41, 1))
        self.sidebar_line_3.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_3.setText("")
        self.sidebar_line_3.setObjectName("sidebar_line_3")
        self.sidebar_line_4 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_4.setGeometry(QtCore.QRect(10, 360, 41, 1))
        self.sidebar_line_4.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_4.setText("")
        self.sidebar_line_4.setObjectName("sidebar_line_4")
        self.sidebar_line_5 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_5.setGeometry(QtCore.QRect(10, 427, 41, 1))
        self.sidebar_line_5.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_5.setText("")
        self.sidebar_line_5.setObjectName("sidebar_line_5")
        self.sidebar_line_6 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_6.setGeometry(QtCore.QRect(10, 490, 41, 1))
        self.sidebar_line_6.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_6.setText("")
        self.sidebar_line_6.setObjectName("sidebar_line_6")
        self.stars = QtWidgets.QLabel(self.centralwidget)
        self.stars.setGeometry(QtCore.QRect(280, 120, 111, 111))
        self.stars.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.stars.setText("")
        self.stars.setPixmap(QPixmap(":/images/images for cascade/starsss.png"))
        self.stars.setObjectName("stars")
        self.main_box = QtWidgets.QLabel(self.centralwidget)
        self.main_box.setGeometry(QtCore.QRect(630, 150, 521, 591))
        self.main_box.setStyleSheet("border-top-right-radius: 13px;\n"
"border-bottom-right-radius: 13px;\n"
"background-color: rgb(167, 145, 203,0.2);")
        self.main_box.setText("")
        self.main_box.setObjectName("main_box")
        self.main_box_2 = QtWidgets.QLabel(self.centralwidget)
        self.main_box_2.setGeometry(QtCore.QRect(660, 180, 461, 531))
        self.main_box_2.setStyleSheet("border-top-right-radius: 13px;\n"
"border-bottom-right-radius: 13px;\n"
"background-color: rgb(0, 0, 0,0.6);")
        self.main_box_2.setText("")
        self.main_box_2.setObjectName("main_box_2")
        self.quick_notes_title = QtWidgets.QLabel(self.centralwidget)
        self.quick_notes_title.setGeometry(QtCore.QRect(970, 188, 201, 71))
        self.quick_notes_title.setStyleSheet("color: rgb(167, 145, 203);\n"
"background-color: rgb(255, 255, 255,0);\n"
"font: 25pt \"Montserrat\";\n"
"")
        self.quick_notes_title.setObjectName("quick_notes_title")
        self.todo_title = QtWidgets.QLabel(self.centralwidget)
        self.todo_title.setGeometry(QtCore.QRect(980, 440, 201, 71))
        self.todo_title.setStyleSheet("color: rgb(167, 145, 203);\n"
"background-color: rgb(255, 255, 255,0);\n"
"font: 25pt \"Montserrat\";\n"
"")
        self.todo_title.setObjectName("todo_title")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(690, 530, 381, 31))
        self.checkBox.setStyleSheet("QCheckBox {\n"
"    background-color: rgb(255, 255, 255, 0);\n"
"    font: 12pt \"Montserrat\";\n"
"    color: rgb(195, 195, 195);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 1px solid #c3c3c3;\n"
"    background: none;\n"
"    border-radius:3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #c3c3c3;\n"
"    background-color: rgb(0,0,0,0);\n"
"    border-radius: 5px;\n"
"    image: url(:/images/images for cascade/checkmark.png);\n"
"}\n"
"\n"
"")
    
        self.checkBox.setText("")
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(690, 560, 391, 42))
        self.checkBox_2.setStyleSheet("QCheckBox {\n"
"    background-color: rgb(255, 255, 255, 0);\n"
"    font: 12pt \"Montserrat\";\n"
"    color: rgb(195, 195, 195);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 1px solid #c3c3c3;\n"
"    background: none;\n"
"    border-radius:3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #c3c3c3;\n"
"    background-color: rgb(0,0,0,0);\n"
"    border-radius: 5px;\n"
"    image: url(:/images/images for cascade/checkmark.png);\n"
"}\n"
"\n"
"")
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(690, 601, 391, 31))
        self.checkBox_3.setStyleSheet("QCheckBox {\n"
"    background-color: rgb(255, 255, 255, 0);\n"
"    font: 12pt \"Montserrat\";\n"
"    color: rgb(195, 195, 195);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 1px solid #c3c3c3;\n"
"    background: none;\n"
"    border-radius:3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #c3c3c3;\n"
"    background-color: rgb(0,0,0,0);\n"
"    border-radius: 5px;\n"
"    image: url(:/images/images for cascade/checkmark.png);\n"
"}\n"
"\n"
"")
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(690, 640, 391, 31))
        self.checkBox_4.setStyleSheet("QCheckBox {\n"
"    background-color: rgb(255, 255, 255, 0);\n"
"    font: 12pt \"Montserrat\";\n"
"    color: rgb(195, 195, 195);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 1px solid #c3c3c3;\n"
"    background: none;\n"
"    border-radius:3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #c3c3c3;\n"
"    background-color: rgb(0,0,0,0);\n"
"    border-radius: 5px;\n"
"    image: url(:/images/images for cascade/checkmark.png);\n"
"}\n"
"\n"
"")
            
        self.todo_line = QtWidgets.QLabel(self.centralwidget)
        self.todo_line.setGeometry(QtCore.QRect(720, 554, 371, 1))
        self.todo_line.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.todo_line.setText("")
        self.todo_line.setObjectName("todo_line")
        self.todo_line_2 = QtWidgets.QLabel(self.centralwidget)
        self.todo_line_2.setGeometry(QtCore.QRect(720, 593, 370, 1))
        self.todo_line_2.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.todo_line_2.setText("")
        self.todo_line_2.setObjectName("todo_line_2")
        self.todo_line_3 = QtWidgets.QLabel(self.centralwidget)
        self.todo_line_3.setGeometry(QtCore.QRect(720, 627, 370, 1))
        self.todo_line_3.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.todo_line_3.setText("")
        self.todo_line_3.setObjectName("todo_line_3")
        self.todo_line_4 = QtWidgets.QLabel(self.centralwidget)
        self.todo_line_4.setGeometry(QtCore.QRect(720, 665, 370, 1))
        self.todo_line_4.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.todo_line_4.setText("")
        self.todo_line_4.setObjectName("todo_line_4")
        self.todo = QtWidgets.QTextEdit(self.centralwidget)
        self.todo.setGeometry(QtCore.QRect(730, 530, 361, 21))
        self.todo.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"font: 10pt \"Monteserrat\";\n"
"color: rgb(195, 195, 195);")
        self.todo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.todo.setPlaceholderText("")
        self.todo.setObjectName("todo")
        self.todo_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.todo_2.setGeometry(QtCore.QRect(730, 570, 361, 21))
        self.todo_2.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"font: 10pt \"Monteserrat\";\n"
"color: rgb(195, 195, 195);")
        self.todo_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.todo_2.setObjectName("todo_2")
        self.todo_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.todo_3.setGeometry(QtCore.QRect(730, 604, 361, 21))
        self.todo_3.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"font: 10pt \"Monteserrat\";\n"
"color: rgb(195, 195, 195);")
        self.todo_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.todo_3.setObjectName("todo_3")
        self.todo_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.todo_4.setGeometry(QtCore.QRect(730, 640, 361, 21))
        self.todo_4.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
"font: 10pt \"Monteserrat\";\n"
"color: rgb(195, 195, 195);")
        self.todo_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.todo_4.setObjectName("todo_4")

        checkboxes = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        todos = [self.todo, self.todo_2, self.todo_3, self.todo_4]

        todo_manager = TodoManager(checkboxes, todos)    
        
        self.notes_line = QtWidgets.QLabel(self.centralwidget)
        self.notes_line.setGeometry(QtCore.QRect(690, 295, 401, 1))
        self.notes_line.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.notes_line.setText("")
        self.notes_line.setObjectName("notes_line")
        self.sidebar_line_7 = QtWidgets.QLabel(self.centralwidget)
        self.sidebar_line_7.setGeometry(QtCore.QRect(10, 552, 41, 1))
        self.sidebar_line_7.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.sidebar_line_7.setText("")
        self.sidebar_line_7.setObjectName("sidebar_line_7")
        self.notes = QtWidgets.QLabel(self.centralwidget)
        self.notes.setGeometry(QtCore.QRect(9, 500, 41, 51))
        self.notes.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.notes.setText("")
        self.notes.setPixmap(QPixmap(":/images/images for cascade/notes_icon.png"))
        self.notes.setObjectName("notes")
        self.notes_line_2 = QtWidgets.QLabel(self.centralwidget)
        self.notes_line_2.setGeometry(QtCore.QRect(690, 330, 401, 1))
        self.notes_line_2.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.notes_line_2.setText("")
        self.notes_line_2.setObjectName("notes_line_2")
        self.notes_line_3 = QtWidgets.QLabel(self.centralwidget)
        self.notes_line_3.setGeometry(QtCore.QRect(690, 365, 401, 1))
        self.notes_line_3.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.notes_line_3.setText("")
        self.notes_line_3.setObjectName("notes_line_3")
        self.notes_line_4 = QtWidgets.QLabel(self.centralwidget)
        self.notes_line_4.setGeometry(QtCore.QRect(690, 400, 401, 1))
        self.notes_line_4.setStyleSheet("background-color: rgb(255, 255, 255,0.5);")
        self.notes_line_4.setText("")
        self.notes_line_4.setObjectName("notes_line_4")
        self.welcome_title = QtWidgets.QLabel(self.centralwidget)
        self.welcome_title.setGeometry(QtCore.QRect(230, 210, 211, 81))
        self.welcome_title.setStyleSheet("color: rgb(167, 145, 203);\n"
"background-color: rgb(255, 255, 255,0);\n"
"font: 25pt \"Montserrat\";\n"
"font-weight: bold;")
        
        # Replace QTextEdit and QLabel with QListWidget
        self.notes_list = QtWidgets.QListWidget(self.centralwidget)
        self.notes_list.setGeometry(QtCore.QRect(690, 260, 401, 161)) 
        self.notes_list.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
                                     "font: 10pt \"Monteserrat\";\n"
                                     "color: rgb(195, 195, 195);")
        self.notes_list.setObjectName("notes_list")
        self.notes_list.setSpacing(8)
        self.notes_list.itemClicked.connect(self.open_notepad)
        
        
        # Load initial notes and last updated times
        self.load_notes()
        self.view_more_notes = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openNotesViewer())
        self.view_more_notes.setGeometry(QtCore.QRect(1010, 410, 93, 28))
        self.view_more_notes.setStyleSheet("QPushButton {\n"
"    background-color: rgba(185, 185, 185, 0);\n"
"    font: 8pt \"Montserrat\";\n"
"    color: rgb(154, 154, 154);\n"
"    border-radius: 5px;\n"
"   \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(195, 195, 195);\n"
"}\n"
"")
        self.view_more_notes.setObjectName("view_more_notes")
        self.ai_chat = QtWidgets.QTextEdit(self.centralwidget)
        self.ai_chat.setGeometry(QtCore.QRect(110, 290, 461, 380))
        self.ai_chat.setStyleSheet("border-radius: 13px;\n"
"background-color: rgb(0, 0, 0,0.5);")
        self.ai_chat.setText("")
        self.ai_chat.setObjectName("ai_chat")
        self.ai_chat_input = QtWidgets.QLineEdit(self.centralwidget)
        self.ai_chat_input.setGeometry(QtCore.QRect(110, 690, 463, 35))
        self.ai_chat_input.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
        "font: 10pt 'Montserrat';\n"
        "color: rgb(195, 195, 195);\n"
        "border: 1px solid #d4b9e9;\n"
        "border-radius: 6px;")
        self.ai_chat_input.setFrame(False)
        self.ai_chat_input.setObjectName("ai_chat_input")

        self.ai_chat_enter = QtWidgets.QPushButton(self.centralwidget)
        self.ai_chat_enter.setGeometry(QtCore.QRect(539, 692, 41, 31))
        self.ai_chat_enter.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.ai_chat_enter.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QPixmap(":/images/images for cascade/arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ai_chat_enter.setIcon(icon2)
        self.ai_chat_enter.setObjectName("ai_chat_enter")
        self.ai_chat_enter.clicked.connect(self.handle_ai_chat_input)
        mainpage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainpage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1211, 26))
        self.menubar.setObjectName("menubar")
        mainpage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainpage)
        self.statusbar.setObjectName("statusbar")
        mainpage.setStatusBar(self.statusbar)

        self.retranslateUi(mainpage)
        QtCore.QMetaObject.connectSlotsByName(mainpage)

    def retranslateUi(self, mainpage):
        icon = QtGui.QIcon(":/images/images for cascade/Cascade-removebg-preview.png")
        mainpage.setWindowIcon(icon)
        _translate = QtCore.QCoreApplication.translate
        mainpage.setWindowTitle(_translate("mainpage", "Cascade"))
        self.intro_nav.setText(_translate("mainpage", "Introduction"))
        self.studyplan_nav.setText(_translate("mainpage", "Study Plan"))
        self.calender_nav.setText(_translate("mainpage", "Calendar"))
        self.stats_nav.setText(_translate("mainpage", "Statistics"))
        self.faq_nav.setText(_translate("mainpage", "FAQ\'s"))
        self.about_nav.setText(_translate("mainpage", "About "))
        self.contact_nav.setText(_translate("mainpage", "Contact"))
        self.quick_notes_title.setText(_translate("mainpage", "Notes"))
        self.todo_title.setText(_translate("mainpage", "To-do"))
        self.welcome_title.setText(_translate("mainpage", "Welcome"))
        self.view_more_notes.setText(_translate("mainpage", "View More"))
        self.ai_chat_input.setPlaceholderText(_translate("mainpage", "Enter something ..."))

    def handle_ai_chat_input(self):
        question = self.ai_chat_input.text()
        title, response = get_gemini_response(question)
        self.ai_chat.clear()
        self.ai_chat.append(f"<h2 style='color: white;'>{title}</h2>")
        for chunk in response:
            self.ai_chat.append(f"<p style='color: white;'>{chunk.text}</p>")
        self.ai_chat.append('_' * 80)
        self.ai_chat.append("<h2 style='color: white;'>Chat History</h2>")
        for entry in self.chat.history:
            if hasattr(entry, 'question_text') and hasattr(entry, 'response_text'):
                self.ai_chat.append(f"<div style='background-color:#D3D3D3; color: white;'>Q: {entry.question_text}</div>")
                self.ai_chat.append(f"<div style='background-color:#F5F5F5; color: white;'>A: {entry.response_text}</div>")
        self.ai_chat.append('_' * 80)
        self.ai_chat_input.clear()

    def timer_clicked(self, event):
        timer_dialog = QDialog()
        ui = Ui_Timer(timer_dialog)  
        ui.setupUi(timer_dialog)
        ui.set_opacity(0.8)  
        timer_dialog.exec_()
        timer_dialog.show()

    def open_notepad(self, item):
        Predefined_folder = r"data\notepad_data"
        note_name = item.text().split()[0]  # Extract the note name (before the time ago)
        note_path = os.path.join(Predefined_folder, f"{note_name}.txt")

        # Open the note editor for the specified note
        subprocess.Popen(["python", "note_editor.py", note_path])

    def load_notes(self):

        now = datetime.datetime.now()
        self.notes_list.clear()
        Predefined_folder = r"data\notepad_data"

        # Iterate through files in the folder
        for filename in os.listdir(Predefined_folder):
                if filename.endswith(".txt"):
                        note_path = os.path.join(Predefined_folder, filename)

                        # Display note name and last updated time if the note exists
                        if os.path.exists(note_path):
                                last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(note_path))
                                time_diff = now - last_modified

                                # Calculate time ago
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

                                # Add item to the QListWidget with note name and last updated time
                                # Remove the ".txt" extension from the filename
                                note_name = filename[:-4]  # Remove the last 4 characters (".txt")
                                self.notes_list.addItem(f"{note_name}                              {time_ago}")

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Windows")
    mainpage = QtWidgets.QMainWindow()
    ui = Ui_mainpage()
    ui.setupUi(mainpage)
    mainpage.show()
    sys.exit(app.exec_())
