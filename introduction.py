from pathlib import Path
from tkinter import Tk, Frame, Canvas, Button, Text, WORD, PhotoImage
from PIL import Image, ImageTk

class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("948x658")
        self.title("Introduction")
        icon_image = PhotoImage(file=r"data\assets\introduction_assets\Cascade.png") 
        self.iconphoto(False, icon_image)
        self.configure(bg="#121139")
        self.frames = {}
        self.create_frames()
        self.show_frame("FirstFrame")

    def create_frames(self):
        for F in (FirstFrame, SecondFrame, ThirdFrame, FourthFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

class BaseFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121139")
        self.controller = controller

        self.ASSETS_PATH = Path(__file__).parent / Path(r"data\assets\introduction_assets")

        self.canvas = Canvas(
            self,
            bg="#121139",
            height=658,
            width=948,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.setup_common_elements()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_common_elements(self):
        canvas = self.canvas

        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        canvas.create_image(603.0, 400.0, image=image_image_1)
        self.image_image_1 = image_image_1  # To prevent image from being garbage collected

        buttons_info = [
            ("button_1.png", 557.0, 37.0, 71.0, 13.0),
            ("button_2.png", 472.0, 36.0, 72.0, 13.0),
            ("button_3.png", 389.0, 36.0, 85.0, 13.0),
            ("button_4.png", 292.0, 36.0, 99.0, 13.0),
            ("button_5.png", 634.0, 36.0, 43.0, 13.0),
            ("button_6.png", 691.0, 36.0, 50.0, 13.0),
            ("button_7.png", 747.0, 36.0, 88.0, 13.0),
            ("button_8.png", 828.0, 31.0, 23.361921310424805, 25.0),
            ("button_9.png", 865.859619140625, 33.6034049987793, 23.361921310424805, 22.69281005859375),
            ("button_10.png", 904.0, 34.0, 23.360000610351562, 22.690000534057617),
            ("button_13.png", 528.1419067382812, 578.8392944335938, 12.810811042785645, 13.428571701049805),
            ("button_14.png", 488.10809326171875, 578.8392944335938, 12.810811042785645, 13.428571701049805),
            ("button_15.png", 448.0743103027344, 578.8392944335938, 12.810811042785645, 13.428571701049805),
            ("button_16.png", 407.2398376464844, 578.8392944335938, 12.810811042785645, 13.428571701049805),
        ]

        for info in buttons_info:
            button_image = PhotoImage(file=self.relative_to_assets(info[0]))
            button = Button(
                self,
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                background='#121139',
                activebackground='#121139',
                command=lambda name=info[0]: self.handle_button_click(name),  # Call handle_button_click
                relief="flat"
            )
            button.place(x=info[1], y=info[2], width=info[3], height=info[4])
            setattr(self, f"button_image_{info[0]}", button_image)

        canvas.create_rectangle(290.0, 56.0, 814.0, 57.0, fill="#FFFFFF", outline="")

        image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        canvas.create_image(473.0, 358.0, image=image_image_2)
        self.image_image_2 = image_image_2  # To prevent image from being garbage collected

        image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        canvas.create_image(470.0, 353.0, image=image_image_3)
        self.image_image_3 = image_image_3  # To prevent image from being garbage collected

        canvas.create_text(576.0, 96.0, anchor="nw", text="Introduction", fill="#A791CA", font=("MontserratRoman SemiBold", 46 * -1))

        image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        canvas.create_image(716.0, 155.0, image=image_image_4)
        self.image_image_4 = image_image_4  # To prevent image from being garbage collected

        image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        canvas.create_image(36.0, 41.0, image=image_image_5)
        self.image_image_5 = image_image_5  # To prevent image from being garbage collected

    def handle_button_click(self, button_name):
        if button_name == "button_16.png":
                self.controller.show_frame("FirstFrame")
        elif button_name == "button_15.png":
                self.controller.show_frame("SecondFrame")
        elif button_name == "button_14.png":
                self.controller.show_frame("ThirdFrame")
        elif button_name == "button_13.png":
                self.controller.show_frame("FourthFrame")   

class FirstFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.canvas.create_text(
            162.0,
            426.0,
            anchor="nw",
            text='''Welcome to CASCADE – your next-generation GenAI-driven study 
companion that’s set to transform the way you learn. We’re proud 
    to introduce a platform that’s not just another study tool, but a 
                          revolution in personalized education.''',
            fill="#FFFFFF",
            font=("Montserrat Light", 20 * -1)
        )

        image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.canvas.create_image(473.0, 318.0, image=image_image_6)
        self.image_image_6 = image_image_6  # To prevent image from being garbage collected

        button_image_11 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        nxt_button = Button(
            self,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("SecondFrame"),
            relief="flat"
        )
        nxt_button.place(x=576.1824340820312, y=578.0, width=12.01013469696045, height=14.267857551574707)
        self.button_image_11 = button_image_11  # To prevent image from being garbage collected

        button_image_12 = PhotoImage(file=self.relative_to_assets("button_12.png"))
        prev_button = Button(
            self,
            image=button_image_12,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("FourthFrame"),  # Placeholder, should go to previous frame
            relief="flat"
        )
        prev_button.place(x=359.99999713897705, y=578.0000257492065, width=12.01013469696045, height=14.267857551574707)
        self.button_image_12 = button_image_12  # To prevent image from being garbage collected

class SecondFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.canvas.create_text(113.0, 160.0, anchor="nw", text="GenAI Features", fill="#A791CA", font=("MontserratRoman", 40 * -1))

        # Add three images with 185x203 size and alignment
        image_paths = ["Group 347.png", "Group 348.png", "Group 349.png"]
        x_offset = 260  
        y_offset = 310  
        text_y_offset = y_offset + 120
        text_x_offset = 80
        text_data = [
            {
                "heading": '''Personalized Study Plans''',
                "paragraph": '''Share your syllabus and let 
CASCADE craft a study schedule 
that evolves with your
learning pace.'''
            },
            {
                "heading": "Quiz Generation",
                "paragraph": '''Its like having a personal
coach that challenges you with
questions tailored to your
current knowledge level,
pushing you towards 
mastery of the subject matter.'''
            },
            {
                "heading": "Skill Tracking & Roadmap",
                "paragraph": '''This is your compass in the academic
world, guiding you through the skills
you need to acquire and aligning them
with your future career aspirations.'''
            }]
        for i, image_path in enumerate(image_paths):

            # Load and resize image using Pillow
            if image_path == "Group 347.png":
                img = Image.open(self.relative_to_assets("Group 347.png"))
                img = img.resize((img.width - 18, img.height - 18), Image.LANCZOS) 
                image = ImageTk.PhotoImage(img) 

            else:
                img = Image.open(self.relative_to_assets(image_path)) 
                img = img.resize((img.width, img.height), Image.LANCZOS)  # Resize image
                image = ImageTk.PhotoImage(img) 

            self.canvas.create_image(x_offset + i * 220, y_offset, image=image)
            setattr(self, f"image_{image_path}", image)  

            # Add text under each image
            text_x = x_offset + i * 220 - text_x_offset
            self.canvas.create_text(text_x, text_y_offset, anchor="nw", text=text_data[i]["heading"], fill="#FFFFFF", font=("Montserrat SemiBold", 16 * -1))
            self.canvas.create_text(text_x, text_y_offset + 30, anchor="nw", text=text_data[i]["paragraph"], fill="#FFFFFF", font=("Montserrat", 12 * -1))


        button_image_11 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        nxt_button = Button(
            self,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("ThirdFrame"),
            relief="flat"
        )
        nxt_button.place(x=576.1824340820312, y=578.0, width=12.01013469696045, height=14.267857551574707)
        self.button_image_11 = button_image_11  # To prevent image from being garbage collected

        button_image_12 = PhotoImage(file=self.relative_to_assets("button_12.png"))
        prev_button = Button(
            self,
            image=button_image_12,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("FirstFrame"),
            relief="flat"
        )
        prev_button.place(x=359.99999713897705, y=578.0000257492065, width=12.01013469696045, height=14.267857551574707)
        self.button_image_12 = button_image_12  # To prevent image from being garbage collected


class ThirdFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.canvas.create_text(113.0, 160.0, anchor="nw", text="More features", fill="#A791CA", font=("MontserratRoman", 40 * -1))

        # Image and Text Data
        image_paths = [
            "Group 350.png", "Group 351.png", "Group 352.png", "Group 353.png",
            "Group 354.png", "Group 355.png", "Group 356.png", "Group 357.png"
        ]
        text_data = [
            "Customizable Timer", "Flashcards", "GenAI Chatbot", "Daily Schedule",
            "Notes", "To-Do List", "Music Player", "Statistics"
        ]

        # Image Dimensions
        image_width = 90
        image_height = 96
        x_offset = 200
        y_offset = 260

        for i, image_path in enumerate(image_paths):
            img = Image.open(self.relative_to_assets(image_path))
            img = img.resize((image_width, image_height), Image.LANCZOS)
            image = ImageTk.PhotoImage(img)

            # Calculate image position in grid
            row = i // 4  # Integer division for row
            col = i % 4  # Modulo for column
            x = x_offset + col * (image_width + 90)  # Spacing between images
            y = y_offset + row * (image_height + 90)

            self.canvas.create_image(x, y, image=image)
            setattr(self, f"image_{image_path}", image)  # Prevent garbage collection

            # Add text below image
            self.canvas.create_text(x, y + image_height -20, anchor="center", text=text_data[i], fill="#FFFFFF", font=("Montserrat", 12 * -1))

        button_image_11 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        nxt_button = Button(
            self,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("FourthFrame"),
            relief="flat"
        )
        nxt_button.place(x=576.1824340820312, y=578.0, width=12.01013469696045, height=14.267857551574707)
        self.button_image_11 = button_image_11  # To prevent image from being garbage collected

        button_image_12 = PhotoImage(file=self.relative_to_assets("button_12.png"))
        prev_button = Button(
            self,
            image=button_image_12,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("SecondFrame"),
            relief="flat"
        )
        prev_button.place(x=359.99999713897705, y=578.0000257492065, width=12.01013469696045, height=14.267857551574707)
        self.button_image_12 = button_image_12  # To prevent image from being garbage collected

class FourthFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.canvas.create_text(113.0, 160.0, anchor="nw", text="Our Ecosystem", fill="#A791CA", font=("MontserratRoman", 35 * -1))

        # Text Content
        text_content = [
    "In CASCADE, we've carefully designed a study ecosystem that combines powerful GenAI features with essential study tools.",
    "This creates a supportive environment for academic success. "
    "The GenAI features are at the heart of CASCADE, but they work ",
    "together with a range of tools to enhance your learning experience:"
    "",  # Empty line for spacing
    "               Timer:  Track your study sessions precisely. Customize the timer to match your focus span.",
    "               Flashcards: Strengthen your understanding and memory with flexible flashcards.",
    "               GenAI Chatbot:  Get instant help and answers to your academic questions, anytime.",
    "               Daily Schedule:  Organize your day with a clear schedule. Stay on track with your studies.",
    "               Notes: Take notes effortlessly. Keep your ideas and insights readily available.",
    "               To-Do List:  Manage your tasks efficiently.  See your goals clearly with a daily refresh.",
    "               Music Player:  Choose your study soundtrack. Listen to your favorite tunes to stay motivated.",
    "               Statistics:  Track your progress with detailed insights.  Understand your study habits and improve your performance.",
    "CASCADE combines these features to create a distraction-free environment that boosts efficiency. ",
    "This allows you to concentrate on what truly matters – your studies.",
    "We hope CASCADE becomes more than a study tool. We want it to be a trusted partner on your ",
    "academic journey.  Enjoy the experience, embrace the challenge, and let's achieve excellence together with CASCADE."
]
        
        # Bold the text within the ** **
        for i in range(len(text_content)):
            text_content[i] = text_content[i].replace("**", "<b>", 1).replace("**", "</b>", 1) 
        text_y_offset = 200
        text_x_offset = 100
        for i, text_line in enumerate(text_content):
            # Add text
            self.canvas.create_text(
                text_x_offset,
                text_y_offset + i * 25,
                anchor="nw",
                text=text_line,
                fill="#FFFFFF",
                font=("Montserrat ", 12 * -1)
            )

        button_image_11 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        nxt_button = Button(
            self,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("FirstFrame"),
            relief="flat"
        )
        nxt_button.place(x=576.1824340820312, y=578.0, width=12.01013469696045, height=14.267857551574707)
        self.button_image_11 = button_image_11  # To prevent image from being garbage collected

        button_image_12 = PhotoImage(file=self.relative_to_assets("button_12.png"))
        prev_button = Button(
            self,
            image=button_image_12,
            borderwidth=0,
            highlightthickness=0,
            background='#121139',
            activebackground='#121139',
            command=lambda: controller.show_frame("ThirdFrame"),
            relief="flat"
        )
        prev_button.place(x=359.99999713897705, y=578.0000257492065, width=12.01013469696045, height=14.267857551574707)
        self.button_image_12 = button_image_12  # To prevent image from being garbage collected

if __name__ == "__main__":
    app = App()
    app.mainloop()
