import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


from database import register_user
from database import login_user
from gui.admin_gui import AdminGUI
from gui.lecturer_gui import LecturerGUI
from gui.operator_gui import OperatorGUI


root = tk.Tk()

root.title("Smart Campus Resource Booking System")
root.geometry("700x500")


def register():

    username = username_entry.get()
    password = password_entry.get()
    role = role_box.get()

    if username == "" or password == "":
        messagebox.showerror(
            "Error",
            "All fields required"
        )
        return

    success = register_user(
        username,
        password,
        role
    )

    if success:
        messagebox.showinfo(
            "Success",
            "Registration Successful"
        )
    else:
        messagebox.showerror(
            "Error",
            "User already exists"
        )


def login():

    username = username_entry.get()
    password = password_entry.get()

    result =login_user(
        username,
        password
    )

    if result:

        role = result[0]

        if role == "Administrator":

            AdminGUI()

        elif role == "Lecturer":

            LecturerGUI(username)

        elif role == "Operator":

            OperatorGUI()

        else:

            messagebox.showerror(
                "Error",
                "Unknown Role"
            )


title = tk.Label(
    root,
    text="Smart Campus Resource Booking System",
    font=("Arial",16,"bold")
)

title.pack(pady=20)

tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(
    root,
    text="Password"
).pack()

password_entry = tk.Entry(
    root,
    show="*"
)

password_entry.pack()

tk.Label(
    root,
    text="Role"
).pack()

role_box = ttk.Combobox(
    root,
    values=[
        "Lecturer",
        "Administrator",
        "Operator"
    ]
)

role_box.pack()

tk.Button(
    root,
    text="Register",
    command=register
).pack(pady=10)

tk.Button(
    root,
    text="Login",
    command=login
).pack()

root.mainloop()