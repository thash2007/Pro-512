import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import get_all_resources
from database import delete_resource
from database import add_resource
from database import get_campus_bookings
from database import update_resource
from database import get_resource_usage_by_campus


class AdminGUI:

    def __init__(self):

        self.window = tk.Toplevel()

        self.window.title(
            "Campus Administrator"
        )

        self.window.geometry("700x500")

        tk.Label(
            self.window,
            text="Resource ID"
        ).pack()

        self.resource_id = tk.Entry(
            self.window
        )

        self.resource_id.pack()

        tk.Label(
            self.window,
            text="Resource Name"
        ).pack()

        self.resource_name = tk.Entry(
            self.window
        )

        self.resource_name.pack()

        tk.Label(
            self.window,
            text="Campus"
        ).pack()

        self.campus = ttk.Combobox(
            self.window,
            values=[
                "Johannesburg",
                "Pretoria",
                "Durban"
            ]
        )

        self.campus.pack()

        tk.Button(
            self.window,
            text="Add Resource",
            command=self.add_resource
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="Refresh Resources",
            command=self.view_resources
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Delete Selected Resource",
            command=self.remove_resource
        ).pack(pady=10)

        self.resource_list = tk.Listbox(
            self.window,
            width=80
        )

        self.resource_list.pack(pady=20)

        tk.Button(
            self.window,
            text="View Campus Bookings",
            command=self.view_campus_bookings
        ).pack(pady=10)

        self.booking_list = tk.Listbox(
            self.window,
            width=90
        )

        self.booking_list.pack(pady=10)

        tk.Button(
            self.window,
            text="View Usage Trends",
            command=self.view_usage_trends
        ).pack(pady=10)

        self.usage_list = tk.Listbox(
            self.window,
            width=90
        )

        self.usage_list.pack(pady=10)

        tk.Label(
            self.window,
            text="New Resource Name"
        ).pack()

        self.new_name = tk.Entry(
            self.window
        )

        self.new_name.pack()

        tk.Button(
            self.window,
            text="Update Resource",
            command=self.edit_resource
        ).pack(pady=10)

    def add_resource(self):

        if (
            self.resource_id.get() == ""
            or
            self.resource_name.get() == ""
            or
            self.campus.get() == ""
        ):

            messagebox.showerror(
                "Error",
                "Complete all fields"
            )

            return

        success = add_resource(
            self.resource_id.get(),
            self.resource_name.get(),
            self.campus.get()
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Resource Added"
            )

            self.view_resources()

        else:

            messagebox.showerror(
                "Error",
                "Duplicate Resource ID"
            )

    def view_resources(self):

        self.resource_list.delete(
            0,
            tk.END
        )

        resources = get_all_resources()

        for resource in resources:

            resource_text = (
                f"{resource[0]} | "
                f"{resource[1]} | "
                f"{resource[2]}"
            )

            self.resource_list.insert(
                tk.END,
                resource_text
            )
    def remove_resource(self):

        selected = self.resource_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select a resource"
            )

            return

        resource = self.resource_list.get(
            selected[0]
        )

        resource_id = resource.split("|")[0].strip()

        delete_resource(resource_id)

        messagebox.showinfo(
            "Success",
            "Resource Deleted"
        )

        self.view_resources()

    def view_campus_bookings(self):

        self.booking_list.delete(
            0,
            tk.END
        )

        campus = self.campus.get()

        bookings = get_campus_bookings(
            campus
        )

        for booking in bookings:

            booking_text = (
                f"Lecturer: {booking[0]} | "
                f"Resource: {booking[1]} | "
                f"Date: {booking[2]} | "
                f"Time: {booking[3]} | "
                f"Duration: {booking[4]}"
            )

            self.booking_list.insert(
                tk.END,
                booking_text
            )

    def edit_resource(self):

        selected = self.resource_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Select Resource"
            )

            return

        resource = self.resource_list.get(
            selected[0]
        )

        resource_id = (
            resource
            .split("|")[0]
            .strip()
        )

        update_resource(
            resource_id,
            self.new_name.get()
        )

        messagebox.showinfo(
            "Success",
            "Resource Updated"
        )

        self.view_resources()

    def view_usage_trends(self):

        self.usage_list.delete(
            0,
            tk.END
        )

        campus = self.campus.get()

        usage = get_resource_usage_by_campus(
            campus
        )

        if not usage:

            self.usage_list.insert(
                tk.END,
                "No booking data available"
            )

            return

        for item in usage:

            self.usage_list.insert(
                tk.END,
                f"Resource: {item[0]} | Total Bookings: {item[1]}"
            )
