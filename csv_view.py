import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
from os.path import exists

date = datetime.today().date()

class CSVViewer(tk.Frame):
    def __init__(
        self, master, csv_file=rf"data/attendence {date.year}-{date.month}.csv"
    ):
        super().__init__(master)
        tk.Button(
            self,
            text="Back",
            command=lambda: master.switch_frame(0),
            font=("Arial", 10),
            background="lightblue",
        ).pack(pady=(5, 0))

        self.csv_file = csv_file
        self.master = master
        if not exists(self.csv_file):
            self.date = tk.Label(
                self, text=f"Attendence report is not available!", font=("Arial", 15)
            )
            self.date.pack(pady=(8))
            return
        self.date = tk.Label(
            self, text=f"Date: {date.year}-{date.month}", font=("Arial", 15)
        )
        self.tree = ttk.Treeview(self)
        self.date.pack(pady=(8))
        self.load_csv()

    def load_csv(self):
        df = pd.read_csv(self.csv_file)
        columns = df.columns
        last = 1
        for i, col in enumerate(columns):
            if not (df[col].astype(str) == "nan").all():
                last = i

        columns = columns[: last + 1]
        self.tree["column"] = list(columns)
        self.tree["show"] = "headings"

        for header in self.tree["column"]:
            if header == "ID":
                self.tree.column(header, width=30)
            elif header == "Name":
                self.tree.column(header, width=100)
            else:
                self.tree.column(header, width=60)
            self.tree.heading(header, text=header)

        for index, row in df.iterrows():
            row = list(
                map(
                    lambda x: str(x).replace("nan", "ABS") if str(x) == "nan" else x,
                    row,
                )
            )
            self.tree.insert("", "end", values=row)
        self.tree["height"] = index + 1
        self.tree["padding"] = 3
        self.tree.pack()
