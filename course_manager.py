

class CourseManager:
    def __init__(self):
        self.course_title = ""
        self.course_syllabus = ""

    def set_course(self, title, syllabus):
        self.course_title = title
        self.course_syllabus = syllabus

    def get_course_title(self):
        return self.course_title

    def get_course_syllabus(self):
        return self.course_syllabus
