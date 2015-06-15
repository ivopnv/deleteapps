#!/usr/bin/env python

import Tkinter as tk
import subprocess


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.get_all_packages()
        self.get_system_apps()
        self.get_data_apps()

        self.delete_button = tk.Button(self, width=100, text="Delete selected packages", command=self.click_event)
        self.delete_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

    def get_all_packages(self):
        proc = subprocess.Popen(["adb shell pm list packages -f"], stdout=subprocess.PIPE, shell=True)
        self.packages = proc.stdout.read()

    def get_data_apps(self):
        self.data_aps_label = tk.Label(self, text="Applications in data", bd=4)
        self.data_aps_label.grid(row=0, column=2)

        self.list_data_apps = tk.Listbox(self, width=60, height=40, selectmode=tk.MULTIPLE)
        self.list_data_apps.pack()

        for package in self.packages.split():
            if "data" in package:
                self.list_data_apps.insert(tk.END, package.split("=", 1)[1])

        self.list_data_apps.grid(row=1, column=2)

    def get_system_apps(self):
        self.system_aps_label = tk.Label(self, text="Applications in system", bd=4)
        self.system_aps_label.grid(row=0, column=1)

        self.list_system_apps = tk.Listbox(self, width=60, height=40, selectmode=tk.SINGLE)
        self.list_system_apps.pack()

        for package in self.packages.split():
            if "system" in package:
                self.list_system_apps.insert(tk.END, package.split("=", 1)[1])

        self.list_system_apps.grid(row=1, column=1)

    def click_event(self):
        x = 0
        while x < self.list_data_apps.size():

            if self.list_data_apps.selection_includes(x) == 1:
                subprocess.Popen(["adb uninstall " + self.list_data_apps.get(x)], stdout=subprocess.PIPE, shell=True)

            x += 1

        self.refresh_data_apps()

    def refresh_data_apps(self):
        self.list_data_apps.delete(0, tk.END)
        proc = subprocess.Popen(["adb shell pm list packages -f"], stdout=subprocess.PIPE, shell=True)
        packages = proc.stdout.read()

        for package in packages.split():
            if "data" in package:
                self.list_data_apps.insert(tk.END, package.split("=", 1)[1])


if __name__ == '__main__':
    app = Application()
    app.master.title('Simple application')
    app.mainloop()



