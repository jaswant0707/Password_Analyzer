
import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime


# Color theme
BG = "#080D1B"
CARD = "#111A2E"
CARD2 = "#16223A"
BLUE = "#3987FF"
PURPLE = "#9B5CFF"
CYAN = "#24D6D0"
WHITE = "#F2F5FF"
GREY = "#9AAAC4"
RED = "#FF5577"
GREEN = "#35D69A"
YELLOW = "#FFC857"

special_characters = "!@#$%^&*()_+-=[]{};:,.?/"
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"

weak_passwords = [
    "password", "123456", "12345678", "qwerty",
    "abc123", "admin", "welcome", "password123",
    "iloveyou", "000000"
]


# Password checking function
def check_weak_password(password):
    lower_password = password.lower()

    for word in weak_passwords:
        if word in lower_password:
            return True

    for year in range(1900, datetime.now().year + 1):
        if str(year) in password:
            return True

    sequences = [
        "123456", "abcdef", "qwerty",
        "654321", "987654"
    ]

    for sequence in sequences:
        if sequence in lower_password:
            return True

    return False


# Password analysis function
def analyze_password(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(char in special_characters for char in password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    if check_weak_password(password):
        strength = "Weak"
        color = RED
        suggestions.append("Avoid common words, sequences and years.")

    elif score <= 2:
        strength = "Weak"
        color = RED

    elif score == 3:
        strength = "Medium"
        color = YELLOW

    elif score == 4:
        strength = "Strong"
        color = CYAN

    else:
        strength = "Very Strong"
        color = GREEN

    return score, strength, color, suggestions


# Saving password history
def save_log(password, strength):
    try:
        with open("password_history.txt", "a") as file:
            file.write(
                f"Date: {datetime.now()} | "
                f"Length: {len(password)} | "
                f"Strength: {strength}\n"
            )
    except:
        messagebox.showerror("Error", "Unable to save history.")


# Password generator
def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8 or length > 50:
            messagebox.showwarning(
                "Invalid Length",
                "Enter password length between 8 and 50."
            )
            return

        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_characters)
        ]

        all_characters = lowercase + uppercase + digits + special_characters

        for i in range(length - 4):
            password.append(random.choice(all_characters))

        random.shuffle(password)

        final_password = "".join(password)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, final_password)

        analyze_and_display()

    except ValueError:
        messagebox.showwarning(
            "Invalid Input",
            "Please enter a valid number."
        )


# Analyze and display result
def analyze_and_display():
    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "Empty Password",
            "Please enter a password first."
        )
        return

    score, strength, color, suggestions = analyze_password(password)

    result_label.config(text=strength, fg=color)
    score_label.config(text=f"{score}/5")

    progress.delete("all")

    progress_width = 300
    progress.create_rectangle(
        0, 0, progress_width, 12,
        fill=CARD2, outline=""
    )

    progress.create_rectangle(
        0, 0, progress_width * score / 5, 12,
        fill=color, outline=""
    )

    output.delete("1.0", tk.END)

    output.insert(tk.END, "PASSWORD ANALYSIS\n\n")
    output.insert(tk.END, f"Password Length: {len(password)}\n")
    output.insert(tk.END, f"Security Score: {score}/5\n")
    output.insert(tk.END, f"Strength: {strength}\n\n")

    if suggestions:
        output.insert(tk.END, "SUGGESTIONS\n\n")

        for suggestion in suggestions:
            output.insert(tk.END, "• " + suggestion + "\n")
    else:
        output.insert(
            tk.END,
            "Great! Your password meets all basic checks."
        )

    save_log(password, strength)


# Clear all fields
def clear_fields():
    password_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)

    result_label.config(text="Not Analyzed", fg=GREY)
    score_label.config(text="0/5")

    progress.delete("all")

    output.delete("1.0", tk.END)


# Circular decoration
root = tk.Tk()
root.title("Password Security System")
root.geometry("900x700")
root.minsize(800, 650)
root.configure(bg=BG)

background = tk.Canvas(
    root,
    bg=BG,
    highlightthickness=0
)
background.place(x=0, y=0, relwidth=1, relheight=1)

background.create_oval(
    680, -170, 1030, 180,
    outline="#172C59",
    width=3
)

background.create_oval(
    720, -130, 990, 140,
    outline="#243D78",
    width=2
)

background.create_oval(
    -150, 530, 180, 860,
    outline="#24204F",
    width=3
)

background.create_oval(
    -110, 570, 140, 820,
    outline="#342568",
    width=2
)


# Main heading
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=45, pady=(25, 15))

tk.Label(
    header,
    text="PASSWORD SECURITY",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    header,
    text="Analyze  •  Generate  •  Protect",
    font=("Segoe UI", 10),
    bg=BG,
    fg=CYAN
).pack(anchor="w", pady=(3, 0))


# Main card
main_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground="#263B68",
    highlightthickness=2
)
main_card.pack(fill="both", expand=True, padx=45, pady=10)

content = tk.Frame(main_card, bg=CARD)
content.pack(fill="both", expand=True, padx=25, pady=20)


# Password input section
tk.Label(
    content,
    text="ENTER YOUR PASSWORD",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=GREY
).pack(anchor="w", pady=(0, 8))

password_entry = tk.Entry(
    content,
    font=("Segoe UI", 14),
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
password_entry.pack(fill="x", ipady=12, pady=(0, 18))


# Password length section
tk.Label(
    content,
    text="PASSWORD LENGTH",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=GREY
).pack(anchor="w", pady=(0, 8))

length_entry = tk.Entry(
    content,
    font=("Segoe UI", 12),
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
length_entry.insert(0, "12")
length_entry.pack(fill="x", ipady=9, pady=(0, 18))


# Action buttons
button_frame = tk.Frame(content, bg=CARD)
button_frame.pack(fill="x", pady=(0, 22))


def create_button(parent, text, command, color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=11
    )


analyze_button = create_button(
    button_frame,
    "ANALYZE",
    analyze_and_display,
    BLUE
)
analyze_button.pack(side="left", fill="x", expand=True, padx=(0, 7))

generate_button = create_button(
    button_frame,
    "GENERATE",
    generate_password,
    PURPLE
)
generate_button.pack(side="left", fill="x", expand=True, padx=7)

clear_button = create_button(
    button_frame,
    "CLEAR",
    clear_fields,
    "#34445F"
)
clear_button.pack(side="left", fill="x", expand=True, padx=(7, 0))


# Result section
result_card = tk.Frame(
    content,
    bg=CARD2,
    highlightbackground="#314B78",
    highlightthickness=1
)
result_card.pack(fill="x", pady=(0, 15))

result_top = tk.Frame(result_card, bg=CARD2)
result_top.pack(fill="x", padx=15, pady=(12, 5))

tk.Label(
    result_top,
    text="PASSWORD STRENGTH",
    font=("Segoe UI", 10, "bold"),
    bg=CARD2,
    fg=GREY
).pack(side="left")

score_label = tk.Label(
    result_top,
    text="0/5",
    font=("Segoe UI", 12, "bold"),
    bg=CARD2,
    fg=CYAN
)
score_label.pack(side="right")

result_label = tk.Label(
    result_card,
    text="Not Analyzed",
    font=("Segoe UI", 19, "bold"),
    bg=CARD2,
    fg=GREY
)
result_label.pack(anchor="w", padx=15, pady=(0, 10))

progress = tk.Canvas(
    result_card,
    height=12,
    bg=CARD2,
    highlightthickness=0
)
progress.pack(fill="x", padx=15, pady=(0, 15))


# Output section
tk.Label(
    content,
    text="ANALYSIS DETAILS",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=GREY
).pack(anchor="w", pady=(0, 8))

output = tk.Text(
    content,
    height=7,
    font=("Consolas", 10),
    bg="#0C1426",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    wrap="word",
    padx=12,
    pady=10
)
output.pack(fill="both", expand=True)


# Footer
tk.Label(
    root,
    text="PASSWORD SECURITY SYSTEM  |  PYTHON PROJECT",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg="#637694"
).pack(pady=(5, 12))


root.mainloop()
