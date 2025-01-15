import tkinter as tk
from tkinter import ttk, PhotoImage
import sqlite3
from pathlib import Path
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_achievements(category="daily_streak"):
    conn = sqlite3.connect('cascade_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, icon_path FROM Achievements WHERE type=?", (category,))
    achievements = cursor.fetchall()
    conn.close()
    return achievements

def update_achievement_display(achievements):
    for widget in achievement_frame.winfo_children():
        widget.destroy()

    row, col = 0, 0
    for name, description, icon_path in achievements:
        try:
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((64, 64))  # Resize image
            icon_photo = ImageTk.PhotoImage(icon_image)

            frame = tk.Frame(achievement_frame, bg="#1E2D40", bd=1, relief="solid")
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            icon_label = tk.Label(frame, image=icon_photo, bg="#1E2D40")
            icon_label.image = icon_photo  # Keep a reference
            icon_label.pack()

            name_label = tk.Label(frame, text=name, fg="white", bg="#1E2D40", font=("Inter Medium", 12))
            name_label.pack()

            desc_label = tk.Label(frame, text=description, wraplength=150, fg="gray", bg="#1E2D40", font=("Inter", 10))
            desc_label.pack()

            col += 1
            if col == 4:
                row += 1
                col = 0



        except FileNotFoundError:
            print(f"Error: Icon not found at {icon_path}")



window = tk.Tk()
window.geometry("1204x801")
window.configure(bg="#101E39")
window.title("Achievements Page")

canvas = tk.Canvas(
    window,
    bg="#101E39",
    height=801,
    width=1204,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Background Images
image_image_1 = PhotoImage(file=r"data\assets\Background\image_1.png")
image_1 = canvas.create_image(603.0, 400.0, image=image_image_1)
canvas.tag_raise(image_1)
image_image_2 = PhotoImage(file=r"data\assets\Background\image_2.png")
image_2 = canvas.create_image(1092.0, 45.0, image=image_image_2)
image_image_3 = PhotoImage(file=r"data\assets\Background\image_3.png")
image_3 = canvas.create_image(1134.0, 48.0, image=image_image_3)
image_image_4 = PhotoImage(file=r"data\assets\Background\image_4.png")
image_4 = canvas.create_image(57.0, 46.0, image=image_image_4)
image_image_5 = PhotoImage(file=r"data\assets\Background\image_5.png")
image_5 = canvas.create_image(602.0, 432.0, image=image_image_5)
image_image_6 = PhotoImage(file=r"data\assets\Background\image_6.png")
image_6 = canvas.create_image(600.0, 427.0, image=image_image_6)


# Squares Images
image_image_7 = PhotoImage(r"data\assets\Squares\image_7.png")
image_7 = canvas.create_image(199.6962890625, 288.635498046875, image=image_image_7)
image_image_8 = PhotoImage(r"data\assets\Squares\image_8.png")
image_8 = canvas.create_image(199.6962890625, 457.697509765625, image=image_image_8)
image_image_9 = PhotoImage(r"data\assets\Squares\image_9.png")
image_9 = canvas.create_image(199.6962890625, 626.759765625, image=image_image_9)
image_image_10 = PhotoImage(r"data\assets\Squares\image_10.png")
image_10 = canvas.create_image(706.8828125, 288.635498046875, image=image_image_10)
image_image_11 = PhotoImage(r"data\assets\Squares\image_11.png")
image_11 = canvas.create_image(706.8828125, 457.697509765625, image=image_image_11)
image_image_12 = PhotoImage(r"data\assets\Squares\image_12.png")
image_12 = canvas.create_image(706.8828125, 627.759765625, image=image_image_12)
image_image_13 = PhotoImage(r"data\assets\Squares\image_13.png")
image_13 = canvas.create_image(459.939453125, 289.0, image=image_image_13)
image_image_14 = PhotoImage(r"data\assets\Squares\image_14.png")
image_14 = canvas.create_image(459.939453125, 458.0, image=image_image_14)
image_image_15 = PhotoImage(r"data\assets\Squares\image_15.png")
image_15 = canvas.create_image(459.86376953125, 626.759765625, image=image_image_15)
image_image_16 = PhotoImage(r"data\assets\Squares\image_16.png")
image_16 = canvas.create_image(967.05029296875, 288.635498046875, image=image_image_16)
image_image_17 = PhotoImage(r"data\assets\Squares\image_17.png")
image_17 = canvas.create_image(967.05029296875, 457.697509765625, image=image_image_17)
image_image_18 = PhotoImage(r"data\assets\Squares\image_18.png")
image_18 = canvas.create_image(966.11083984375, 621.124267578125, image=image_image_18)
canvas.create_text(
    758.0,
    39.0,
    anchor="nw",
    text="Statistics",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    662.0,
    39.0,
    anchor="nw",
    text="Calender",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    548.0,
    39.0,
    anchor="nw",
    text="Study Plan",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    421.0,
    39.0,
    anchor="nw",
    text="Introduction",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    854.0,
    39.0,
    anchor="nw",
    text="FAQs",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    922.0,
    39.0,
    anchor="nw",
    text="About",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_text(
    997.0,
    39.0,
    anchor="nw",
    text="Contact",
    fill="#FFFFFF",
    font=("MontserratRoman Medium", 15 * -1)
)
canvas.create_rectangle(418.0, 65.0, 1058.0, 66.0, fill="#BDBDBD", outline="")
canvas.create_text(
    752.0,
    107.0,
    anchor="nw",
    text="Achievements",
    fill="#AF92C6",
    font=("Montserrat Bold", 49 * -1)
)
canvas.create_rectangle(770.0, 172.0, 1121.0369873046875, 173.0, fill="#FFFFFF", outline="")


achievement_frame = tk.Frame(canvas, bg="#0d0c19")
achievement_frame.place(x=100, y=200)


category_var = tk.StringVar(value="daily_streak")  # Keep this line
categories = [  # Define your categories as dictionaries
    {"name": "daily_streak"},
    {"name": "quiz_streak"},
    {"name": "skills_developed"},
    {"name": "courses_completed"},
    {"name": "misc"},
    {"name": "domain_master"}
]

category_dropdown = tk.OptionMenu(
    window,        # Place on window, NOT canvas
    category_var,
    *(category["name"] for category in categories),  # Cleaner unpacking
    command=lambda x: update_achievement_display(load_achievements(category_var.get())) # Updated command
)
category_dropdown.config(
    bg="#A791CB",
    fg="#261345",
    borderwidth=0,
    highlightthickness=0,
    font=("Montserrat Medium", 12),
    width=20, # Maintain original width
    height=1 #For original height consistency, though might be ignored depending on platform
    
)

dropdown_menu = category_dropdown.nametowidget(category_dropdown.menuname)  # Access the menu
dropdown_menu.config(
    bg="#A791CB",
    fg="#261345",
    font=("Montserrat Medium", 12),
    borderwidth=0
)


category_dropdown.place(x=870.0, y=194.0)

initial_achievements = load_achievements()
update_achievement_display(initial_achievements)

window.resizable(False, False)
window.mainloop()