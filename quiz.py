from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QFont
import resourcesCascade
import sqlite3
import os
import re
import functools
import google.generativeai as genai
import time
import json

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, SafetySetting
    vertex_ai_available = True
except ImportError:
    print("Warning: vertexai library not found. Subjective quiz assessment will be unavailable.")
    vertex_ai_available = False

try:
    import google.generativeai as genai
    genai_available = True
except ImportError:
    print("Warning: google-generativeai library not found. Subjective quiz generation will be unavailable.")
    genai_available = False


class Ui_quiz(object):
    def __init__(self):
        self.score1 = 0
        self.questions_frames = []
        self.feedback_data = {} 

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1209, 942)
        MainWindow.setStyleSheet("background-color: rgb(27, 32, 81);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 1221, 901))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(":/images/images for cascade/bg_image.png"))
        self.bg.setScaledContents(True)
        self.bg.setObjectName("bg")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1201, 751))
        self.widget.setStyleSheet("background: transparent;")
        self.widget.setObjectName("widget")
        self.main_title_quiz = QtWidgets.QLabel(self.widget)
        self.main_title_quiz.setGeometry(QtCore.QRect(450, 0, 381, 71))
        self.main_title_quiz.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.main_title_quiz.setStyleSheet("background: transparent;\n"
                                           "font: 24pt \"Montserrat\";\n"
                                           "font-weight: bold;\n"
                                           "color: rgb(167, 145, 203);\n"
                                           "qproperty-alignment: AlignCenter;\n"
                                           "")
        self.main_title_quiz.setObjectName("main_title_quiz")
        self.bg_box1 = QtWidgets.QLabel(self.widget)
        self.bg_box1.setGeometry(QtCore.QRect(50, 100, 501, 141))
        self.bg_box1.setStyleSheet("border-radius: 15px;\n"
                                   "background-color: rgba(126, 59, 115, 0.5);")
        self.bg_box1.setText("")
        self.bg_box1.setObjectName("bg_box1")
        self.select_course_title = QtWidgets.QLabel(self.widget)
        self.select_course_title.setGeometry(QtCore.QRect(-40, 100, 311, 51))
        self.select_course_title.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.select_course_title.setStyleSheet("background: transparent;\n"
                                                "font: 17pt \"Montserrat\";\n"
                                                "color: rgb(167, 145, 203);\n"
                                                "qproperty-alignment: AlignCenter;\n"
                                                "")
        self.select_course_title.setObjectName("select_course_title")
        self.dropdown_course = QtWidgets.QComboBox(MainWindow)
        self.dropdown_course.setGeometry(QtCore.QRect(90, 180, 150, 35))
        course_list = self.display_courses()
        self.dropdown_course.addItems(course_list)
        self.dropdown_course.setStyleSheet("""
        QComboBox {
            font: 10pt "Montserrat";
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            font-weight: 500;
        }
        QComboBox:on {
            background-color: rgb(58, 40, 93);
        }
        QComboBox QListView {
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(100, 100, 100);
        }
        QComboBox QListView::item {
            background-color: transparent;
            color: rgb(255, 255, 255);
        }
        QComboBox QListView::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QComboBox QListView::item:selected {
            background-color: rgb(100, 100, 150);
            color: rgb(255, 255, 255);
        }
        """)
        self.nav_line_2 = QtWidgets.QLabel(self.widget)
        self.nav_line_2.setGeometry(QtCore.QRect(60, 146, 471, 1))
        self.nav_line_2.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.nav_line_2.setText("")
        self.nav_line_2.setObjectName("nav_line_2")
        self.select_difficulty = QtWidgets.QLabel(self.widget)
        self.select_difficulty.setGeometry(QtCore.QRect(-30, 270, 311, 51))
        self.select_difficulty.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.select_difficulty.setStyleSheet("background: transparent;\n"
                                             "font: 17pt \"Montserrat\";\n"
                                             "color: rgb(167, 145, 203);\n"
                                             "qproperty-alignment: AlignCenter;\n"
                                             "")
        self.select_difficulty.setObjectName("select_difficulty")
        self.dropdown_diff = QtWidgets.QComboBox(MainWindow)
        self.dropdown_diff.setGeometry(QtCore.QRect(90, 350, 150, 35))
        self.dropdown_diff.addItems(['Easy', 'Medium', 'Hard'])
        self.dropdown_diff.setStyleSheet("""
        QComboBox {
            font: 10pt "Montserrat";
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            font-weight: 500;
        }
        QComboBox:on {
            background-color: rgb(58, 40, 93);
        }
        QComboBox QListView {
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(100, 100, 100);
        }
        QComboBox QListView::item {
            background-color: transparent;
            color: rgb(255, 255, 255);
        }
        QComboBox QListView::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QComboBox QListView::item:selected {
            background-color: rgb(100, 100, 150);
            color: rgb(255, 255, 255);
        }
        """)
        self.nav_line_3 = QtWidgets.QLabel(self.widget)
        self.nav_line_3.setGeometry(QtCore.QRect(60, 316, 471, 1))
        self.nav_line_3.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.nav_line_3.setText("")
        self.nav_line_3.setObjectName("nav_line_3")
        self.bg_box2 = QtWidgets.QLabel(self.widget)
        self.bg_box2.setGeometry(QtCore.QRect(50, 270, 501, 141))
        self.bg_box2.setStyleSheet("border-radius: 15px;\n"
                                   "background-color: rgba(112, 72, 163, 0.5);")
        self.bg_box2.setText("")
        self.bg_box2.setObjectName("bg_box2")
        self.bg_box3 = QtWidgets.QLabel(self.widget)
        self.bg_box3.setGeometry(QtCore.QRect(650, 100, 501, 141))
        self.bg_box3.setStyleSheet("border-radius: 15px;\n"
                                   "background-color: rgba(72, 147, 163, 0.3);")
        self.bg_box3.setText("")
        self.bg_box3.setObjectName("bg_box3")
        self.select_ques_limit = QtWidgets.QLabel(self.widget)
        self.select_ques_limit.setGeometry(QtCore.QRect(610, 100, 311, 51))
        self.select_ques_limit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.select_ques_limit.setStyleSheet("background: transparent;\n"
                                             "font: 17pt \"Montserrat\";\n"
                                             "color: rgb(167, 145, 203);\n"
                                             "qproperty-alignment: AlignCenter;\n"
                                             "")
        self.select_ques_limit.setObjectName("select_ques_limit")
        self.dropdown_ques = QtWidgets.QComboBox(MainWindow)
        self.dropdown_ques.setGeometry(QtCore.QRect(680, 180, 150, 35))
        self.dropdown_ques.addItems(['5', '10', '15'])
        self.dropdown_ques.setStyleSheet("""
        QComboBox {
            font: 10pt "Montserrat";
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            font-weight: 500;
        }
        QComboBox:on {
            background-color: rgb(58, 40, 93);
        }
        QComboBox QListView {
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(100, 100, 100);
        }
        QComboBox QListView::item {
            background-color: transparent;
            color: rgb(255, 255, 255);
        }
        QComboBox QListView::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QComboBox QListView::item:selected {
            background-color: rgb(100, 100, 150);
            color: rgb(255, 255, 255);
        }
        """)
        self.nav_line_4 = QtWidgets.QLabel(self.widget)
        self.nav_line_4.setGeometry(QtCore.QRect(660, 147, 477, 1))
        self.nav_line_4.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.nav_line_4.setText("")
        self.nav_line_4.setObjectName("nav_line_4")
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setGeometry(QtCore.QRect(860, 360, 93, 28))
        self.enter_button = QtWidgets.QPushButton(self.widget)
        self.enter_button.setGeometry(QtCore.QRect(790, 320, 221, 31))
        self.enter_button.setStyleSheet("font: 13pt \"Montserrat\";\n"
                                        "background-color: rgb(87, 60, 138);\n"
                                        "color: rgb(195, 195, 195);\n"
                                        "border:none;")
        self.enter_button.setObjectName("enter_button")
        self.left_button = QtWidgets.QPushButton(self.widget)
        self.left_button.setGeometry(QtCore.QRect(760, 320, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.left_button.setFont(font)
        self.left_button.setStyleSheet("font: 8pt \"Montserrat\";\n"
                                        "background-color: rgb(87, 60, 138);\n"
                                        "color: rgb(195, 195, 195);\n"
                                        "border:none;\n"
                                        "border-radius: 7px;")
        self.left_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images for cascade/starsss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.left_button.setIcon(icon)
        self.left_button.setIconSize(QtCore.QSize(30, 30))
        self.left_button.setObjectName("left_button")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(1000, 320, 41, 31))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("font: 8pt \"Montserrat\";\n"
                                        "background-color: rgb(87, 60, 138);\n"
                                        "color: rgb(195, 195, 195);\n"
                                        "border-radius:7px;")
        self.pushButton_2.setText("")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(60, 480, 1091, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1089, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Quiz Type Selector
        self.quiz_type_selector = QtWidgets.QComboBox(self.widget)
        self.quiz_type_selector.setGeometry(QtCore.QRect(90, 430, 150, 35))
        self.quiz_type_selector.addItems(["Objective", "Subjective"])
        self.quiz_type_selector.setStyleSheet("""
        QComboBox {
            font: 10pt "Montserrat";
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            font-weight: 500;
        }
        QComboBox:on {
            background-color: rgb(58, 40, 93);
        }
        QComboBox QListView {
            background-color: rgb(58, 40, 93);
            color: rgb(255, 255, 255);
            border: 1px solid rgb(100, 100, 100);
        }
        QComboBox QListView::item {
            background-color: transparent;
            color: rgb(255, 255, 255);
        }
        QComboBox QListView::item:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }
        QComboBox QListView::item:selected {
            background-color: rgb(100, 100, 150);
            color: rgb(255, 255, 255);
        }
        """)

        self.label_behind_button = QtWidgets.QLabel(self.widget)
        self.label_behind_button.setGeometry(QtCore.QRect(770, 330, 281, 31))
        self.label_behind_button.setStyleSheet("background-color: rgb(58, 40, 93);\n"
                                               "border-radius:7px;")
        self.label_behind_button.setText("")
        self.label_behind_button.setObjectName("label_behind_button")
        self.label_behind_button.raise_()
        self.bg_box1.raise_()
        self.select_course_title.raise_()
        self.nav_line_2.raise_()
        self.bg_box2.raise_()
        self.select_difficulty.raise_()
        self.nav_line_3.raise_()
        self.bg_box3.raise_()
        self.select_ques_limit.raise_()
        self.nav_line_4.raise_()
        self.enter_button.raise_()
        self.enter_button.clicked.connect(self.display_questions_from_content)
        self.left_button.clicked.connect(self.display_questions_from_content)
        self.pushButton_2.clicked.connect(self.display_questions_from_content)
        self.scrollArea.raise_()
        self.pushButton_2.raise_()
        self.left_button.raise_()
        self.submit_quiz_button = QtWidgets.QPushButton(self.centralwidget)
        self.submit_quiz_button.setGeometry(QtCore.QRect(1060, 760, 93, 28))
        self.submit_quiz_button.setStyleSheet("font: 8pt \"Montserrat\";\n"
                                              "background-color: rgb(87, 60, 138);\n"
                                              "color: rgb(195, 195, 195);")
        self.submit_quiz_button.setObjectName("submit_quiz_button")

        self.submit_quiz_button.clicked.connect(self.submit_quiz)
        self.line_2 = QtWidgets.QLabel(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(380, 820, 341, 51))
        self.line_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.line_2.setStyleSheet("background: transparent;\n"
                                   "font: 12pt \"Montserrat\";\n"
                                   "color: rgb(167, 145, 203);\n"
                                   "qproperty-alignment: AlignCenter;\n"
                                   "")
        self.line_2.setObjectName("line_2")
        self.score = QtWidgets.QTextEdit(self.centralwidget)
        self.score.setGeometry(QtCore.QRect(620, 830, 104, 41))
        self.score.setObjectName("score")
        self.score.setStyleSheet("font: 12pt 'Montserrat'; color: white;")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1209, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon(":/images/images for cascade/dark_quiz_icon.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle(_translate("MainWindow", "Quiz"))
        self.main_title_quiz.setText(_translate("MainWindow", "Quiz"))
        self.select_course_title.setText(_translate("MainWindow", "Course:"))
        self.select_difficulty.setText(_translate("MainWindow", "Difficulty:"))
        self.select_ques_limit.setText(_translate("MainWindow", "Question Limit:"))
        self.enter_button.setText(_translate("MainWindow", "Generate Quiz!"))
        self.submit_quiz_button.setText(_translate("MainWindow", "Submit"))
        self.line_2.setText(_translate("MainWindow", "You scored: "))

    def display_courses(self):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM courses")
        course_name = cursor.fetchall()
        course_list = [name[0] for name in course_name]
        cursor.close()
        conn.close()
        return course_list

    def inputs(self):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        course_name = self.dropdown_course.currentText()
        cursor.execute("SELECT syllabus FROM courses WHERE name = ?", (course_name,))
        syllabus_row = cursor.fetchone()
        syllabus = syllabus_row[0] if syllabus_row else "N/A"
        question_limit = self.dropdown_ques.currentText()
        difficulty = self.dropdown_diff.currentText()
        quiz_type = self.quiz_type_selector.currentText()
        conn.close()
        return course_name, syllabus, difficulty, question_limit, quiz_type


    def multiturn_generate_content(self):
        if not genai_available:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Gemini API library not found.")
            return None
        course_name, syllabus, difficulty, question_limit, quiz_type = self.inputs()
        if quiz_type == "Objective" and vertex_ai_available:
            return self._generate_objective_quiz()
        elif quiz_type == "Subjective" and genai_available:
            return self._generate_subjective_quiz(course_name, syllabus, difficulty, question_limit)
        else:
            msg = "Gemini or Vertex AI library not found, or quiz type not selected."
            QtWidgets.QMessageBox.warning(self.widget, "Error", msg)
            return None


    def _generate_objective_quiz(self):
        def parse_quiz(quiz_text):
            if "**Answer Key**:" not in quiz_text:
                raise ValueError("The quiz text does not contain an answer key.")
            parts = quiz_text.split("**Answer Key**:")
            if len(parts) < 2:
                raise ValueError("The quiz text is not correctly formatted.")
            questions_text, answer_key_text = parts
            question_pattern = re.compile(
                r"(\d+)\.\s*(.*?)\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*(?=\d+\.\s*|\Z)",
                re.DOTALL)
            questions = question_pattern.findall(questions_text)
            answer_pattern = re.compile(r"(\d+)\.\s*([A-D])")
            answers = answer_pattern.findall(answer_key_text)
            answer_dict = {int(num): ans for num, ans in answers}
            quiz_data = []
            for q in questions:
                question_number, question_text, option_a, option_b, option_c, option_d = q
                question_number = int(question_number)
                correct_answer = answer_dict.get(question_number, "N/A")
                quiz_data.append({
                    "question_number": question_number,
                    "question_text": question_text.strip(),
                    "options": {
                        "A": option_a.strip(),
                        "B": option_b.strip(),
                        "C": option_c.strip(),
                        "D": option_d.strip(),
                    },
                    "correct_answer": correct_answer
                })
            return quiz_data

        try:
            vertexai.init(project="673460396526", location="us-central1")
            model = GenerativeModel(
                "projects/673460396526/locations/us-central1/endpoints/3677037363143376896",
                system_instruction=["""Create a quiz using the following instructions:
The user will provide:Course title
Number of questions: {It will range from 5-15}.Difficulty level: {easy, medium, hard}.Syllabus: {content to be covered}.The quiz should include:A TitleFour options (A, B, C, D) for each question.An answer key provided at the end in the format: "**Answer Key**:\n1. B)\n2. A)\n3. B)\n4.".Ensure the questions cover the provided syllabus and match the specified difficulty level. The answer key must be accurate and in the correct format.

Example input from user:
Create a quiz:-
Course title: Digital Image Processing
Number of questions : 5Difficulty level: MediumSyllabus: Understanding of digital image processing concepts, covering topics such as image formation, transformation, depth estimation, feature extraction, image segmentation, pattern analysis, and motion analysis.


Example output:

## Digital Image Processing Quiz

1. What transformation is commonly used for perspective correction in digital images?
 A) Orthogonal transformation
 B) Affine transformation
 C) Fourier transform
 D) Wavelet transform

2. What technique is used for depth estimation in multi-camera views?
 A) Binocular stereopsis
 B) Image segmentation
 C) Region growing
 D) Optical flow

3. Which feature extraction method is used for detecting edges in images?
 A) Harris corner detection
 B) Canny edge detection
 C) SIFT feature extraction
 D) Hough transform

4. What is the purpose of image segmentation?
 A) To classify pixels into regions
 B) To enhance image contrast
 C) To remove noise from images
 D) To compress image data

5. How are patterns analyzed in digital image processing?
 A) Through clustering and classification
 B) By applying convolution and filtering
 C) Using Fourier transform and histogram processing
 D) Through region growing and edge detection

**Answer Key**:
1. B)
2. A)
3. B)
4. A)
5. A)"""]
            )
            course_name, syllabus, difficulty, question_limit, quiz_type = self.inputs()
            prompt = f"""Create a quiz:- 
Course Title: {course_name} 
Number of questions: {question_limit} 
Difficulty Level: {difficulty} 
Syllabus:{syllabus}"""
            chat = model.start_chat()
            response = chat.send_message([prompt])
            if hasattr(response, 'candidates') and len(response.candidates) > 0:
                content = response.candidates[0].content.parts[0].text
                return parse_quiz(content)
            else:
                print("No candidates found in the response.")
                return None
        except Exception as e:
            print(f"Error generating objective quiz: {e}")
            QtWidgets.QMessageBox.warning(self.widget, "Error", f"Objective quiz generation failed: {e}")
            return None



    def _generate_subjective_quiz(self, course_name, syllabus, difficulty, question_limit):
        try:
            genai.configure(api_key="AIzaSyBEWgDXRyFMHJpXG9bHZZFyDDKDYVEWY2k")
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 512,
                "top_p": 0.95,
            }
            chat_session = model.start_chat(history=[])

            prompt = f"""Generate {question_limit} subjective questions for a {difficulty} quiz on {course_name}.  The quiz should cover the following syllabus: {syllabus}. Format the output as follows:
Question 1: [Question Text]
Answer 1:
Question 2: [Question Text]
Answer 2:
...
"""
            response = chat_session.send_message([prompt])
            response_text = response.text  # Extract the text from the response object

            questions_data = []
            question_pattern = re.compile(r"Question (\d+):(.*?)\nAnswer \d+:", re.DOTALL)
            matches = question_pattern.findall(response_text)  # Use response_text here

            for match in matches:
                question_number, question_text = match
                questions_data.append({
                    "question_number": int(question_number),
                    "question_text": question_text.strip(),
                    "answer_space": ""
                })
            return questions_data
        except Exception as e:
            print(f"Error generating subjective quiz using Gemini: {e}")
            QtWidgets.QMessageBox.warning(self.widget, "Error", f"Subjective quiz generation failed: {e}")
            return None


    def display_questions(self, questions_data):
        # Clear existing widgets
        for i in reversed(range(self.scrollAreaWidgetContents.layout().count())):
            item = self.scrollAreaWidgetContents.layout().itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.scrollAreaWidgetContents.layout().removeItem(item)

        for question_data in questions_data:
            question_frame = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(question_frame)

            question_text_edit = QtWidgets.QTextEdit(question_frame)
            question_text_edit.setReadOnly(True)
            question_text_edit.setPlainText(question_data['question_text'])
            question_text_edit.setStyleSheet("font: 13pt 'Montserrat'; color: white;")
            layout.addWidget(question_text_edit)

            if 'options' in question_data:
                for option_text in question_data['options'].values():
                    option_button = QtWidgets.QRadioButton(question_frame)
                    option_button.setText(option_text)
                    option_button.setStyleSheet("font: 11pt 'Montserrat'; color: white;")
                    option_button.option_id = list(question_data['options'].keys())[
                        list(question_data['options'].values()).index(option_text)]
                    layout.addWidget(option_button)
                    option_button.toggled.connect(functools.partial(self.check_answer, question_frame, option_button))
                    question_frame.correct_answer = question_data['correct_answer']
            else:
                answer_edit = QtWidgets.QTextEdit(question_frame)
                answer_edit.setPlaceholderText("Enter your answer here")
                answer_edit.setStyleSheet("font: 11pt 'Montserrat'; color: white;")
                layout.addWidget(answer_edit)
                question_frame.answer_edit = answer_edit  # Store the answer_edit as an attribute 


            layout.addStretch(1)
            self.scrollAreaWidgetContents.layout().addWidget(question_frame)
            self.questions_frames.append(question_frame)



    def display_questions_from_content(self):
        questions_data = self.multiturn_generate_content()
        if questions_data:
            self.display_questions(questions_data)

    def check_answer(self, question_frame, option_button):
        if option_button.isChecked() and option_button.option_id == question_frame.correct_answer:
            self.score1 += 1
    
    def submit_quiz(self):
        if self.quiz_type_selector.currentText() == "Objective":
            self.calculate_score()
            self.insert_quiz()
        else:  # Subjective Quiz
            self.assess_subjective_answer()
            self.insert_quiz() 

    def assess_subjective_answer(self):
        RATE_LIMIT_SECONDS = 60
        if not vertex_ai_available:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Vertex AI library not found.")
            return

        try:
            vertexai.init(project="673460396526", location="us-central1")
            model = GenerativeModel(
                "projects/673460396526/locations/us-central1/endpoints/7082632793179553792",  # Replace with your endpoint ID
                system_instruction=["""
                    Instructions:
1. Evaluate the student\'s answer to the following question.
2. Provide a grade out of 10.
3. Give structured feedback with strengths, weaknesses, and suggestions for improvement within 50 words.
Question: {question_text}
Student Answer: {answer_text}
Your Response (in this exact format):



{
    \"$Grade$\": <grade_out_of_10>,
    \"$Feedback$\": {
        \"&Strengths&\": \"<strengths_of_answer>\",
        \"&Weaknesses&\": \"<weaknesses_of_answer>\",
        \"&Suggestions&\": \"<suggestions_for_improvement>\"
    }
}
Make sure to include \"$\" for Grade and Feedback, \"&\" for Strengths, Weaknesses and Suggestions. These are essential for parsing."""]  # System instruction for answer assessment
            )

            generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.9,
    "top_p": 0.83,
    "response_mime_type": "application/json"
}

            safety_settings = [
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                SafetySetting(
                    category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
            ]

            all_feedbacks = []
            total_grade = 0

            for question_frame in self.questions_frames:
                question_text = question_frame.findChild(QtWidgets.QTextEdit).toPlainText()
                answer_text = question_frame.answer_edit.toPlainText()

                prompt = f"""
                    **Question:**
                    {question_text}

                    **Student Answer:**
                    {answer_text}
                """  # Prompt for the model

                chat = model.start_chat()  # Start a new chat session for each question
                response = chat.send_message(prompt,generation_config=generation_config,
        safety_settings=safety_settings)

                if hasattr(response, 'candidates') and len(response.candidates) > 0:
                    content = response.candidates[0].content.parts[0].text
                     

                    try:
                        parsed_feedback = json.loads(content) 
                        grade_str = parsed_feedback.get("$Grade$") 
                        try:
                            grade = float(grade_str)  # Try converting to float
                            total_grade += grade
                        except (TypeError, ValueError):
                            if grade_str is not None: # Only print if there's a value but it's not a valid number
                                print(f"Invalid grade format: {grade_str}, using default grade of 0.")
                            grade = 0  # Default to 0 if not convertible

                        # Add the grade value directly into the dictionary for consistent access later
                        parsed_feedback['Grade'] = grade  # Add a "Grade" key for easier tooltip creation
                        
                        all_feedbacks.append(parsed_feedback)
                    except json.JSONDecodeError as json_error:
                        print(f"Error parsing JSON: {json_error}")
                        print(f"Raw model output after cleaning: {cleaned_content}")
                        default_feedback = {
                            "Grade": 0,
                            "Feedback": {
                                "Strengths": "",
                                "Weaknesses": "Could not assess answer due to invalid JSON response.",
                                "Suggestions for Improvement": ""
                            }
                        }
                        all_feedbacks.append(default_feedback)
                else:
                    print("No candidates found in the response.")
                    default_feedback = {
                        "Grade": 0,
                        "Feedback": {
                            "Strengths": "",
                            "Weaknesses": "Could not assess answer - no candidates in the model's response.",
                            "Suggestions for Improvement": ""
                        }
                    }
                    all_feedbacks.append(default_feedback)

                time.sleep(RATE_LIMIT_SECONDS)
                
            if len(self.questions_frames) > 0: # Guard against division by zero
                self.score1 = total_grade / len(self.questions_frames)
            else:
                self.score1 = 0

            for i, question_frame in enumerate(self.questions_frames):
                feedback_data = all_feedbacks[i]

                # Use the added 'Grade' key for simplicity (no more .get('$Grade$', 'N/A'))
                tooltip_text = f"<b>Grade:</b> {feedback_data.get('$Grade$', 'N/A')}/10<br><br>" 
                tooltip_text += f"<b>Strengths:</b> {feedback_data.get('$Feedback$', {}).get('&Strengths&', 'N/A')}<br>"
                tooltip_text += f"<b>Weaknesses:</b> {feedback_data.get('$Feedback$', {}).get('&Weaknesses&', 'N/A')}<br>"
                tooltip_text += f"<b>Suggestions for Improvement:</b> {feedback_data.get('$Feedback$', {}).get('&Suggestions&', 'N/A')}"

                # Set the tooltip for the question_frame
                question_frame.setToolTip(tooltip_text) 


            self.display_feedback(all_feedbacks)

        except Exception as e:
            print(f"Error assessing subjective answer using Vertex AI: {e}")
            QtWidgets.QMessageBox.warning(self.widget, "Error", f"Subjective answer assessment failed: {e}")
        finally:
            self.calculate_score()


    def display_feedback(self, all_feedbacks):
        feedback_text = ""
        for feedback in all_feedbacks:  # Iterate directly through dictionaries 
            # Access 'Grade' and 'Feedback' from each dictionary
            grade = feedback.get('Grade', 'N/A') 
            feedback_data = feedback.get('Feedback', {}) 

            feedback_text += f"**Grade:** {grade}/10\n"
            feedback_text += "**Feedback:**\n"
            feedback_text += f"- **Strengths:** {feedback_data.get('Strengths', 'N/A')}\n"
            feedback_text += f"- **Weaknesses:** {feedback_data.get('Weaknesses', 'N/A')}\n"
            feedback_text += f"- **Suggestions for Improvement:** {feedback_data.get('Suggestions for Improvement', 'N/A')}\n\n"

        self.score.setPlainText(feedback_text)

    def parse_model_output(self, model_output):
        grade_pattern = r"Grade:\s*(\d+)"
        feedback_pattern = r"Feedback:\s*- Strengths:(.*?)\n- Weaknesses:(.*?)\n- Suggestions for Improvement:(.*)"

        grade_match = re.search(grade_pattern, model_output)
        feedback_match = re.search(feedback_pattern, model_output, re.DOTALL)

        if grade_match and feedback_match:
            grade = grade_match.group(1).strip()
            strengths = feedback_match.group(1).strip()
            weaknesses = feedback_match.group(2).strip()
            suggestions = feedback_match.group(3).strip()

            feedback = {
                "Strengths": strengths,
                "Weaknesses": weaknesses,
                "Suggestions for Improvement": suggestions
            }

            return {"Grade": grade, "Feedback": feedback}
        else:
            return None

    def calculate_score(self):
        self.score.setPlainText(str(self.score1))

    def insert_quiz(self):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        course = self.dropdown_course.currentText()
        difficulty = self.dropdown_diff.currentText()
        question_limit = self.dropdown_ques.currentText()
        quiz_type = self.quiz_type_selector.currentText()
        course_name, syllabus, difficulty, question_limit, quiz_type = self.inputs()
        quiz_data = self.multiturn_generate_content()
        marks = self.score.toPlainText()
        date_taken = QtCore.QDate.currentDate().toString(QtCore.Qt.ISODate)

        insert_query = """
        INSERT INTO quizzes (course, difficulty, question_limit, quiz_type, quiz, marks, date_taken)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cursor.execute(insert_query, (course, difficulty, question_limit, quiz_type, str(quiz_data), marks, date_taken))
            conn.commit()
        except Exception as e:
            print(f"Error inserting quiz data: {e}")
            QtWidgets.QMessageBox.warning(self.widget, "Error", f"Failed to save quiz data: {e}")

        cursor.close()
        conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_quiz()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
