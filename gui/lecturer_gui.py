import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_user_bookings
from database import cancel_booking
from database import get_booking_rule
from database import get_resources
from database import create_booking
from database import get_available_resources

class LecturerGUI:

    def __init__(self, username):

        self.username = username

        self.window = tk.Toplevel()

        self.window.title("Lecturer Dashboard")
        self.window.geometry("800x600")

        tk.Label(
            self.window,
            text=f"Welcome {username}",
            font=("Arial", 16)
        ).pack(pady=20)

        tk.Label(
            self.window,
            text="Select Campus"
        ).pack()

        self.campus_box = ttk.Combobox(
            self.window,
            values=[
                "Johannesburg",
                "Pretoria",
                "Durban"
            ]
        )

        self.campus_box.pack()

        self.policy_label = tk.Label(
            self.window,
            text=""
        )

        self.policy_label.pack()

        tk.Button(
            self.window,
            text="Load Resources",
            command=self.load_resources
        ).pack(pady=10)

        self.resource_box = ttk.Combobox(
            self.window
        )

        self.resource_box.pack()

        self.availability_label = tk.Label(
            self.window,
            text="Available Resources"
        )

        self.availability_label.pack()

        tk.Label(
            self.window,
            text="Booking Date (DD/MM/YYYY)"
        ).pack()

        self.date_entry = tk.Entry(
            self.window
        )

        self.date_entry.pack()

        tk.Label(
            self.window,
            text="Start Time"
        ).pack()

        self.time_entry = tk.Entry(
            self.window
        )

        self.time_entry.pack()

        tk.Label(
            self.window,
            text="Duration"
        ).pack()

        self.duration_entry = tk.Entry(
            self.window
        )

        self.duration_entry.pack()

        tk.Button(
            self.window,
            text="Book Resource",
            command=self.book_resource
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="View My Bookings",
            command=self.view_bookings
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Cancel Selected Booking",
            command=self.delete_booking
        ).pack(pady=10)

        self.booking_list = tk.Listbox(
            self.window,
            width=80
        )

        self.booking_list.pack(pady=20)

    def view_bookings(self):

        self.booking_list.delete(
         0,
            tk.END
        )

        bookings = get_user_bookings(
            self.username
        )

        for booking in bookings:

            booking_text = (
                f"{booking[0]} | "
                f"{booking[1]} | "
                f"{booking[2]} | "
                f"{booking[3]} | "
                f"{booking[4]} | "
                f"{booking[5]} hour(s)"
            )

            self.booking_list.insert(
                tk.END,
                booking_text
            )

    def delete_booking(self):

        selected = self.booking_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a booking first"
            )

            return

        booking = self.booking_list.get(
            selected[0]
        )

        booking_id = booking.split("|")[0].strip()

        cancel_booking(
            booking_id
        )

        messagebox.showinfo(
            "Success",
            "Booking Cancelled"
        )

        self.view_bookings()

    def load_resources(self):

        self.update_policy()

        campus = self.campus_box.get()

        resources = get_available_resources(
            campus
        )

        self.resource_box["values"] = resources

    def book_resource(self):

        try:

            campus = self.campus_box.get()

            duration = int(
                self.duration_entry.get()
            )

            max_duration = get_booking_rule(
                campus
            )

            if duration > max_duration:

                messagebox.showerror(
                    "Policy Rule",
                    f"Maximum booking duration is {max_duration} hours"
                )

                return

            if self.resource_box.get() == "":

                messagebox.showerror(
                    "Error",
                    "Select a resource"
                )

                return

            success = create_booking(
                self.username,
                campus,
                self.resource_box.get(),
                self.date_entry.get(),
                self.time_entry.get(),
                duration
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Booking Created"
                )

                self.load_resources()

            else:

                messagebox.showerror(
                    "Error",
                    "Resource Unavailable"
                )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Duration must be a number"
            )

    def update_policy(self):

        campus = self.campus_box.get()

        if campus == "Johannesburg":

            self.policy_label.config(
                text="Policy: Maximum 4 Hours"
            )

        elif campus == "Pretoria":

            self.policy_label.config(
                text="Policy: Maximum 3 Hours"
            )

        elif campus == "Durban":

            self.policy_label.config(
                text="Policy: Maximum 2 Hours"
            )