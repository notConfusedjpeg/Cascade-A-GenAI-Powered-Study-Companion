from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, Label, OptionMenu, StringVar, Listbox, messagebox, simpledialog
import tkinter.font as tkFont
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"data\assets\flashcard_assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

categories = []
category_var = None

def load_flashcards():
    global categories, category_var
    try:
        with open(OUTPUT_PATH / 'Data' / 'flashcard_data' / 'flashcards.jsonl', 'r') as f:
            data = json.load(f)
            categories = data.get("categories", [])
           
            if not all(isinstance(category, dict) and "name" in category and "flashcards" in category for category in categories):
                categories = [] 
    except FileNotFoundError:
        categories = []
        save_flashcards()

    category_var = tk.StringVar(window)
    category_var.set("(Default)")

def save_and_close():
    try:
        save_flashcards()
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save flashcards: {e}")
        window.destroy()

def save_flashcards():
    data = {
        "categories": categories
    }
    (OUTPUT_PATH / 'Data' / 'flashcard_data').mkdir(exist_ok=True)
    with open(OUTPUT_PATH / 'Data' / 'flashcard_data' / 'flashcards.jsonl', 'w') as f:
        json.dump(data, f, indent=2)

def add_flashcard():
    global category_var

    if not categories:
        messagebox.showinfo("No Categories", "Please create a category using 'Manage Categories' before adding flashcards.")
        return

    add_window = Toplevel(window)
    add_window.title("Add Flashcard")
    add_window.geometry("350x250")
    add_window.configure(bg="#321345")

    Label(add_window, text="Question:", bg="#321345", fg="#A791CB").pack(pady=5)
    question_entry = Entry(add_window, bg="#A791CB", fg="#321345")
    question_entry.pack(pady=5)

    Label(add_window, text="Answer:", bg="#321345", fg="#A791CB").pack(pady=5)
    answer_entry = Entry(add_window, bg="#A791CB", fg="#321345")
    answer_entry.pack(pady=5)

    Label(add_window, text="Category:", bg="#321345", fg="#A791CB").pack(pady=5)
    if not category_var:
        category_var = StringVar(add_window)
    category_dropdown = OptionMenu(add_window, category_var, *[category["name"] for category in categories])
    category_dropdown.configure(bg="#A791CB", fg="#321345", activebackground="#321345", activeforeground="#A791CB")
    category_dropdown.pack(pady=5)

    Button(add_window, text="Save", command=lambda: save_new_flashcard(question_entry.get(), answer_entry.get(), category_var.get(), add_window),
           bg="#A791CB", fg="#321345").pack(pady=10)

def save_new_flashcard(question, answer, category_name, add_window):
    if not category_name:
        messagebox.showerror("Error", "Please select a category.")
        return

    flashcard = {
        "question": question,
        "answer": answer,
        "current_text": "#1"
    }

    for category in categories:
        if category["name"] == category_name:
            flashcard["current_text"] = f"#{len(category['flashcards']) + 1}"
            category["flashcards"].append(flashcard)
            break
    else:
        flashcard["current_text"] = "#1"
        categories.append({
            "name": category_name,
            "flashcards": [flashcard]
        })

    update_flashcards()
    add_window.destroy()

def toggle_flashcard(category_index, flashcard_index):
    flashcard = categories[category_index]["flashcards"][flashcard_index]
    if flashcard["current_text"].startswith("#"):
        flashcard["current_text"] = flashcard["question"]
    elif flashcard["current_text"] == flashcard["question"]:
        flashcard["current_text"] = flashcard["answer"]
    else:
        flashcard["current_text"] = f"#{flashcard_index + 1}"
    update_flashcards()

def delete_flashcard(category_index, flashcard_index):
    categories[category_index]["flashcards"].pop(flashcard_index)
    update_flashcards()

def calculate_font_size(text, max_width, max_height):
    test_font = tkFont.Font(family="Montserrat ExtraBold", size=28)
    while True:
        text_width = test_font.measure(text)
        text_height = test_font.metrics("linespace")

        if text_width <= max_width and text_height <= max_height:
            break

        size = test_font.cget("size")
        if size <= 10:
            break
        test_font.config(size=size - 1)

    return test_font.cget("size")

def update_flashcards():
    global category_var

    canvas.delete("flashcard")

    add_button_x = 55
    add_button_y = 135
    add_button_width = 87
    add_button_height = 133
    add_button_image = PhotoImage(file=relative_to_assets("button_1.png"))
    add_button = Button(
        window,
        image=add_button_image,
        borderwidth=0,
        highlightthickness=0,
        fg="#554E15",
        bg="#EDE065",
        command=add_flashcard,
        relief="flat"
    )
    add_button.image = add_button_image
    add_button.place(x=add_button_x, y=add_button_y, width=add_button_width, height=add_button_height)

    if not category_var:
        category_var = StringVar(window)

    category_dropdown = tk.OptionMenu(
        window,
        category_var,
        "(Default)",
        *[category["name"] for category in categories],
        command=filter_flashcards
    )
    category_dropdown.config(bg="#261345", fg="#A791CB", borderwidth=0, highlightthickness=0, font=("Montserrat Medium", 12))

    dropdown_menu = category_dropdown.nametowidget(category_dropdown.menuname)
    dropdown_menu.config(bg="#261345", fg="#A791CB", font=("Montserrat Medium", 12), borderwidth=0)

    category_dropdown.place(x=310, y=80)

    selected_category = category_var.get()

    if selected_category == "(Default)":
        return

    flashcard_index = 0
    for category_index, category in enumerate(categories):
        if selected_category == "All Categories" or category["name"] == selected_category:
            for flashcard in category["flashcards"]:
                flashcard_index += 1
                if flashcard_index <= 3:
                    x = 165 + (flashcard_index - 1) * 111
                    y = 135
                else:
                    x = 55 + ((flashcard_index - 4) % 4) * 111
                    y = 288 + ((flashcard_index - 4) // 4) * 147

                rect = canvas.create_rectangle(x, y, x + 87, y + 133, fill="#EDE065", outline="", tags="flashcard")
                text = flashcard["current_text"]

                font_size = calculate_font_size(text, max_width=87, max_height=133)

                flashcard_button = Button(
                    window,
                    text=text,
                    width=20,
                    height=10,
                    bg="#EDE065",
                    fg="#554E15",
                    font=("Montserrat ExtraBold", font_size),
                    relief="flat",
                    bd=0,
                    command=lambda ci=category_index, fi=flashcard_index-1: toggle_flashcard(ci, fi)
                )
                flashcard_button.configure(wraplength=87)
                canvas.create_window(x + 43.5, y + 66.5, width=87, height=133, window=flashcard_button, anchor="center", tags="flashcard")

                delete_button_image = PhotoImage(file=relative_to_assets("button_9.png"))
                delete_button = Button(
                    image=delete_button_image,
                    borderwidth=0,
                    highlightthickness=0,
                    command=lambda ci=category_index, fi=flashcard_index-1: delete_flashcard(ci, fi),
                    relief="flat",
                    bg="#EDE065",
                    fg="#554E15"
                )
                delete_button.image = delete_button_image
                canvas.create_window(x + 70, y + 110, width=13, height=13, window=delete_button, anchor="nw", tags="flashcard")

    canvas.configure(scrollregion=canvas.bbox("all"))

def filter_flashcards(selected_category):
    update_flashcards()

def open_category_manager():
    def add_category():
        new_category = simpledialog.askstring("Add Category", "Enter new category name:", parent=category_window)
        if new_category:
            if new_category not in [category["name"] for category in categories]:
                categories.append({"name": new_category, "flashcards": []})
                refresh_category_listbox()
            else:
                messagebox.showerror("Error", "Category already exists.", parent=category_window)
        update_flashcards()

    def edit_category():
        selected_index = category_listbox.curselection()
        if selected_index:
            old_category = category_listbox.get(selected_index)
            new_category = simpledialog.askstring("Edit Category", "Enter new category name:", parent=category_window)
            if new_category and new_category != old_category:
                if new_category not in [category["name"] for category in categories]:
                    for category in categories:
                        if category["name"] == old_category:
                            category["name"] = new_category
                            break
                    refresh_category_listbox()
                else:
                    messagebox.showerror("Error", "Category already exists or no change made.", parent=category_window)
        else:
            messagebox.showwarning("Warning", "Please select a category to edit.", parent=category_window)
        update_flashcards()

    def delete_category():
        selected_index = category_listbox.curselection()
        if selected_index:
            category_name = category_listbox.get(selected_index)
            categories[:] = [category for category in categories if category["name"] != category_name]
            refresh_category_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a category to delete.", parent=category_window)
        update_flashcards()

    def refresh_category_listbox():
        category_listbox.delete(0, "end")
        for category in categories:
            category_listbox.insert("end", category["name"])

    category_window = Toplevel(window)
    category_window.title("Category Manager")
    category_window.geometry("232x385")
    category_window.configure(bg="#FFFFFF")
    canvas = Canvas(
        category_window,
        bg="#FFFFFF",
        height=385,
        width=232,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.pack(fill="both", expand=True)
    image_2 = canvas.create_image(
        116.0,
        192.0,
        image=subsampled_image
    )
  
    canvas.create_text(
        15.0,
        13.0,
        anchor="nw",
        text="Manage Categories",
        fill="#A791CA",
        font=("MontserratRoman SemiBold", 18)
    )

    canvas.create_rectangle(
        56.0,
        46.0,
        186.0,
        88.0,
        fill="#A791CB",
        outline=""
    )

    canvas = Canvas(
        category_window,
        bg="#FFFFFF",
        height=26,
        width=108,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    button_image_1 = PhotoImage(file=relative_to_assets("add_button.png"))
    add_button = Button(
        category_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        bg="#A791CB",
        command=add_category,
        relief="flat"
    )
    add_button.image = button_image_1
    add_button.place(
        x=59.0,
        y=48.0,
        width=38.0,
        height=38.0
    )

    button_image_2 = PhotoImage(file=relative_to_assets("edit_button.png"))
    edit_button = Button(
        category_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        bg="#A791CB",
        command=edit_category,
        relief="flat"
    )
    edit_button.image = button_image_2
    edit_button.place(
        x=107.0,  
        y=50.0,  
        width=34.0,  
        height=34.0 
    )

    button_image_3 = PhotoImage(file=relative_to_assets("delete_button.png"))
    delete_button = Button(
        category_window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        bg="#A791CB",
        command=delete_category,
        relief="flat"
    )
    delete_button.image = button_image_3
    delete_button.place(
        x=150.0,
        y=50.0,
        width=34,
        height=34
    )

    category_listbox = Listbox(category_window, bg="#17044D", fg="#FFFFFF", bd=0, highlightthickness=0, relief="flat", selectbackground="#A791CB", font=("MontserratRoman SemiBold", 10))
    category_listbox.place(x=15, y=95, width=200, height=280)

    refresh_category_listbox()

window = Tk()
window.title("Flashcard")
icon_image = PhotoImage(file=r"data\assets\flashcard_assets\dark_flash_icon.png") 
window.iconphoto(False, icon_image)
window.geometry("534x443")
window.configure(bg="#1B0057")
load_flashcards()
imagex = PhotoImage(file=r"data\assets\flashcard_assets\bg2.png")
subsampled_image = imagex.subsample(1, 1)

canvas = Canvas(
    window,
    bg="#1B0057",
    height=460,
    width=534,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("bg_img.png"))
scaled_image = image_image_1.subsample(2, 2)
image_1 = canvas.create_image(
    267, 221.5,  
    image=scaled_image
)

canvas.create_text(
    220.0,
    0.0,
    anchor="nw",
    text="Flashcards",
    fill="#A791CA",
    font=("Montserrat SemiBold", 40)
)
transparent_rectangle_image = PhotoImage(file=relative_to_assets('rectangle.png'))

canvas.create_image(
    30, 120,
    anchor='nw',
    image=transparent_rectangle_image
)

update_flashcards()

manage_icon = PhotoImage(file=relative_to_assets("set.png"))
manage_button = Button(window, image=manage_icon, command=open_category_manager, borderwidth=0, relief="flat", highlightthickness=0, bg="#1E0D5B")
manage_button.image = manage_icon
manage_button.place(x=475, y=80, anchor="nw")

def on_enter(event):
    tooltip.place(x=event.x_root - window.winfo_rootx(), y=event.y_root - window.winfo_rooty())

def on_leave(event):
    tooltip.place_forget()

tooltip = Label(window, text="Manage Categories", bg="#FFFFFF", fg="#000000", bd=1, relief="solid", font=("Montserrat Medium", 10))
tooltip.place_forget()

manage_button.bind("<Enter>", on_enter)
manage_button.bind("<Leave>", on_leave)

window.protocol("WM_DELETE_WINDOW", save_and_close)

window.resizable(False, False)
window.mainloop()