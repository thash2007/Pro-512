import tkinter as tk

from database import get_all_bookings
from database import get_total_bookings_per_campus
from database import get_most_used_resources
from database import get_average_duration
from database import get_total_users
from database import get_total_resources
from database import get_total_bookings


class OperatorGUI:

    def __init__(self):

        self.window = tk.Toplevel()

        self.window.title(
            "System Operator Dashboard"
        )

        self.window.geometry("900x600")

        tk.Button(
            self.window,
            text="Generate Reports",
            command=self.generate_report
        ).pack(pady=20)

        self.report_box = tk.Text(
            self.window,
            width=100,
            height=25
        )

        self.report_box.pack()

    def generate_report(self):

        self.report_box.delete(
            "1.0",
            tk.END
        )

        self.report_box.insert(
            tk.END,
            "SMART CAMPUS RESOURCE BOOKING SYSTEM\n"
        )

        self.report_box.insert(
            tk.END,
            "=====================================\n\n"
        )

        self.report_box.insert(
            tk.END,
            f"Total Users: {get_total_users()}\n"
        )

        self.report_box.insert(
            tk.END,
            f"Total Resources: {get_total_resources()}\n"
        )

        self.report_box.insert(
            tk.END,
            f"Total Bookings: {get_total_bookings()}\n\n"
        )

        campus_data = get_total_bookings_per_campus()

        self.report_box.insert(
            tk.END,
            "TOTAL BOOKINGS PER CAMPUS\n\n"
        )

        for row in campus_data:

            self.report_box.insert(
                tk.END,
                f"{row[0]} : {row[1]} bookings\n"
            )

        self.report_box.insert(
            tk.END,
            "\nMOST USED RESOURCES\n\n"
        )

        resources = get_most_used_resources()

        for row in resources:

            self.report_box.insert(
                tk.END,
                f"{row[0]} : {row[1]} bookings\n"
            )

        self.report_box.insert(
            tk.END,
            "\nAVERAGE BOOKING DURATION\n\n"
        )

        average = get_average_duration()

        self.report_box.insert(
            tk.END,
            f"{average[0]}\n"
        )

        self.report_box.insert(
            tk.END,
            "\nALL BOOKINGS\n\n"
        )

        bookings = get_all_bookings()

        for booking in bookings:

            self.report_box.insert(
                tk.END,
                f"{booking}\n"
            )