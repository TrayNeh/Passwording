import customtkinter as ctk
import random
import string
from datetime import datetime

#  APP CONFIG
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("520x520")
app.title("PASSWORLDING")
app.resizable(False, False)

# FUNCTIONS

def password_strength(password):
    score = 0
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    if len(password) >= 12: score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"

def generate_password():
    length = int(slider.get())
    chars = ""

    if upper_var.get(): chars += string.ascii_uppercase
    if lower_var.get(): chars += string.ascii_lowercase
    if numbers_var.get(): chars += string.digits
    if symbols_var.get(): chars += string.punctuation

    if chars == "":
        result_label.configure(text="Select at least one option")
        strength_label.configure(text="Strength: ---")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    result_label.configure(text=password)

    strength, color = password_strength(password)
    strength_label.configure(text=f"Strength: {strength}", text_color=color)

def copy_password():
    app.clipboard_clear()
    app.clipboard_append(result_label.cget("text"))

def save_password():
    password = result_label.cget("text")
    if password == "":
        return

    with open("passwords.txt", "a", encoding="utf-8") as f:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{date}] {password}\n")

def change_theme(mode):
    ctk.set_appearance_mode(mode)

# UI

title = ctk.CTkLabel(
    app,
    text="🔐 PASSWORLDING",
    font=("Arial", 24, "bold")
)
title.pack(pady=15)

subtitle = ctk.CTkLabel(
    app,
    text="Professional Password Generator",
    font=("Arial", 14)
)
subtitle.pack()

slider = ctk.CTkSlider(app, from_=6, to=32, number_of_steps=26)
slider.set(14)
slider.pack(pady=15)

length_label = ctk.CTkLabel(app, text="Length: 14")
length_label.pack()

slider.configure(command=lambda v: length_label.configure(text=f"Length: {int(v)}"))

upper_var = ctk.BooleanVar(value=True)
lower_var = ctk.BooleanVar(value=True)
numbers_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=False)

ctk.CTkCheckBox(app, text="Uppercase (A-Z)", variable=upper_var).pack()
ctk.CTkCheckBox(app, text="Lowercase (a-z)", variable=lower_var).pack()
ctk.CTkCheckBox(app, text="Numbers (0-9)", variable=numbers_var).pack()
ctk.CTkCheckBox(app, text="Symbols (!@#)", variable=symbols_var).pack()

ctk.CTkButton(
    app,
    text="Generate Password",
    height=40,
    command=generate_password
).pack(pady=15)

result_label = ctk.CTkLabel(
    app,
    text="",
    font=("Consolas", 16),
    wraplength=480
)
result_label.pack(pady=10)

strength_label = ctk.CTkLabel(
    app,
    text="Strength: ---",
    font=("Arial", 14)
)
strength_label.pack(pady=5)

buttons_frame = ctk.CTkFrame(app, fg_color="transparent")
buttons_frame.pack(pady=10)

ctk.CTkButton(
    buttons_frame,
    text="📋 Copy",
    width=140,
    command=copy_password
).grid(row=0, column=0, padx=10)

ctk.CTkButton(
    buttons_frame,
    text="💾 Save",
    width=140,
    command=save_password
).grid(row=0, column=1, padx=10)

theme_var = ctk.StringVar(value="dark")
ctk.CTkOptionMenu(
    app,
    values=["dark", "light"],
    variable=theme_var,
    command=change_theme
).pack(pady=15)

app.mainloop()

