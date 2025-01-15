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
from vertexai.generative_models import GenerativeModel
import math

CHECK = None
try:
    import vertexai
    genai_available = True
except ImportError:
    genai_available = False

class Ui_quiz(object):
    def __init__(self):
        self.score1 = 0
        self.questions_frames = []
        self.feedback_data = {} 
        self.quiz_data = None  
        self.current_course_name = None 

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

        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(60, 70, 1091, 681))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1089, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setLayout(QtWidgets.QVBoxLayout())
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

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

        self.load_initial_quiz()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon(":/images/images for cascade/dark_quiz_icon.png")
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle(_translate("MainWindow", "Quiz"))
        self.main_title_quiz.setText(_translate("MainWindow", "Quiz"))
        self.submit_quiz_button.setText(_translate("MainWindow", "Submit"))
        self.line_2.setText(_translate("MainWindow", "You scored: "))

    def get_last_added_course(self):
        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM courses")
        course_names = cursor.fetchall()
        conn.close()
        if course_names:
            self.current_course_name = course_names[-1][0]
            return self.current_course_name
        return None


    def inputs(self):
        global CHECK
        CHECK = self.get_last_added_course()
        if not CHECK:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "No courses found. Please add a course first.")
            return None, None, None, None

        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()
        course_name = CHECK
        cursor.execute("SELECT syllabus FROM courses WHERE name = ?", (course_name,))
        syllabus_row = cursor.fetchone()
        syllabus = syllabus_row[0] if syllabus_row else "N/A"
        question_limit = "15"
        difficulty = "Medium"
        conn.close()
        return CHECK, syllabus, difficulty, question_limit

    def load_initial_quiz(self):
        self.display_questions_from_content()

    def multiturn_generate_content(self):
        if not genai_available:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Gemini API library not found.")
            return None
        inputs_data = self.inputs()
        if not inputs_data or any(item is None for item in inputs_data):
            return None
        course_name, syllabus, difficulty, question_limit = inputs_data
        return self._generate_objective_quiz(syllabus, question_limit, difficulty)


    def _generate_objective_quiz(self, syllabus, question_limit, difficulty):
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
            prompt = f"""Create a quiz with {question_limit} questions of {difficulty} difficulty level based on the following syllabus: {syllabus}"""
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


    def display_questions_from_content(self):
        inputs_data = self.inputs()
        if not inputs_data or any(item is None for item in inputs_data):
            return
        _, syllabus, difficulty, question_limit = inputs_data
        questions_data = self._generate_objective_quiz(syllabus, question_limit, difficulty)
        if questions_data:
            self.quiz_data = questions_data  # Store the quiz data
            self.display_questions(questions_data)

    def display_questions(self, questions):
        # Clear previous questions
        for frame in self.questions_frames:
            frame.setParent(None)
        self.questions_frames = []

        for q_data in questions:
            question_frame = QtWidgets.QFrame()
            question_layout = QtWidgets.QVBoxLayout(question_frame)

            question_label = QtWidgets.QLabel(f"{q_data['question_number']}. {q_data['question_text']}")
            question_label.setStyleSheet("font: 13pt 'Montserrat'; color: white;")
            question_layout.addWidget(question_label)

            options_group = QtWidgets.QButtonGroup()

            for option_id, option_text in q_data["options"].items():
                option_button = QtWidgets.QRadioButton(f"{option_id}) {option_text}")
                option_button.setStyleSheet("font: 11pt 'Montserrat'; color: white;")
                option_button.option_id = option_id
                options_group.addButton(option_button)
                question_layout.addWidget(option_button)

            question_frame.correct_answer = q_data["correct_answer"]
            self.questions_frames.append(question_frame)
            self.scrollAreaWidgetContents.layout().addWidget(question_frame)

    def check_answer(self, question_frame, option_button):
        if option_button.isChecked() and option_button.option_id == question_frame.correct_answer:
            self.score1 += 1

    def calculate_score(self):
        self.score1 = 0
        for frame in self.questions_frames:
            for button in frame.findChildren(QtWidgets.QRadioButton):
                if button.isChecked() and button.option_id == frame.correct_answer:
                    self.score1 += 1
                    break  

        self.score.setPlainText(str(self.score1))

    def submit_quiz(self):
        self.calculate_score()
        self.update_course_assessment()
        if self.update_course_assessment():
            # After successful update, retrieve and display the proficiency score
            self.show_proficiency_message()

    def update_course_assessment(self):
        if self.current_course_name is None:
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Could not identify the current course.")
            return False

        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()

        cursor.execute("SELECT initial_user_said_score FROM courses WHERE name = ?", (self.current_course_name,))
        said_score_row = cursor.fetchone()
        # Ensure initial_user_said_score is not None
        initial_user_said_score = said_score_row[0] if said_score_row and said_score_row[0] is not None else 0

        initial_user_assessment_score = self.score1
        final_user_assessment_score = round(0.35 * initial_user_said_score + 0.65 * initial_user_assessment_score)

        update_query = """
        UPDATE courses
        SET final_user_assessment_score = ?
        WHERE name = ?
        """

        try:
            cursor.execute(update_query, (final_user_assessment_score, self.current_course_name))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating course scores: {e}")
            QtWidgets.QMessageBox.warning(self.widget, "Error", f"Failed to update course scores: {e}")
            conn.close()
            return False

    def show_proficiency_message(self):
        if self.current_course_name is None:
            return

        conn = sqlite3.connect('cascade_project.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name, final_user_assessment_score FROM courses WHERE name = ?", (self.current_course_name,))
        course_data = cursor.fetchone()
        conn.close()

        if course_data:
            course_name = course_data[0]
            proficiency_score = course_data[1]
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Quiz Submitted")
            msg_box.setText(f"Your actual proficiency in {course_name} is: {proficiency_score:.2f}")
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: rgb(40, 40, 90); /* Dark blue background */
                }
                QMessageBox QLabel {
                    color: rgb(255, 255, 255); /* White text */
                    font: 10pt 'Montserrat'; /* Adjust font if needed */
                }
                QMessageBox QPushButton {
                    background-color: rgb(167, 145, 203); /* Light purple button */
                    color: rgb(0, 0, 0); /* Black button text */
                    border: none;
                    padding: 8px 15px;
                    font: 9pt 'Montserrat';
                    border-radius: 5px;
                }
                QMessageBox QPushButton:hover {
                    background-color: rgb(147, 125, 183); /* Slightly darker on hover */
                }
            """)
            msg_box.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_quiz()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
