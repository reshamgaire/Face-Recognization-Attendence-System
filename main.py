import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import face_recognition
import cv2
from datetime import datetime
from os.path import exists

date = datetime.today().date()


class FacialAttendence(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Face Recognition Attendence System")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        img = Image.open("data/icon.jpg")
        self.iconphoto(True, ImageTk.PhotoImage(img))
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        heading_label = tk.Label(
            self, text="Face Recognition Attendence System", font=("Arial", 25)
        )
        heading_label.grid(row=0, column=0, columnspan=4, padx=(250, 0), pady=(15, 28))

        img = Image.open("data/add student.jpg")
        self.image1 = ImageTk.PhotoImage(img.resize((270, 350), 1))
        img = Image.open("data/take attendence.jpg")
        self.image2 = ImageTk.PhotoImage(img.resize((270, 350), 1))
        img = Image.open("data/display attendence.jpg")
        self.image3 = ImageTk.PhotoImage(img.resize((270, 350), 1))

        image_label1 = tk.Label(self, image=self.image1, width=270, height=350)
        image_label1.grid(row=1, column=0, padx=(180, 45))
        image_label2 = tk.Label(self, image=self.image2, width=270, height=350)
        image_label2.grid(row=1, column=1, padx=45)
        image_label3 = tk.Label(self, image=self.image3, width=270, height=350)
        image_label3.grid(row=1, column=2, padx=45)

        button1 = tk.Button(
            self,
            text="Add Student",
            command=lambda: master.switch_frame(AddStudent),
            font=("Arial", 15),
            background="lightblue",
        )
        button1.grid(row=2, column=0, padx=(150, 0), pady=10)
        button2 = tk.Button(
            self,
            text="Take Attendence",
            command=lambda: master.switch_frame(TakeAttendence),
            font=("Arial", 15),
            background="lightblue",
        )
        button2.grid(row=2, column=1, pady=10)
        button3 = tk.Button(
            self,
            text="View Attendence",
            command=lambda: master.switch_frame(CSVViewer),
            font=("Arial", 15),
            background="lightblue",
        )
        button3.grid(row=2, column=2, pady=10)


class AddStudent(tk.Frame):
    def __init__(self, master, student_file="data/students.csv"):
        super().__init__(master)
        tk.Button(
            self,
            text="Back",
            command=lambda: master.switch_frame(StartPage),
            font=("Arial", 10),
            background="lightblue",
        ).pack(pady=(5, 0))
        self.master = master
        self.pack(fill="both", expand=True)
        self.student_file = student_file
        self.student_faces = []
        self.face = ()
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.camera_issue_label = tk.Label(self.left_frame, font=("Arial", 15))
        self.form_issue_label = tk.Label(self.right_frame, font=("Arial", 15))

        self.webcam_label = tk.Label(self.left_frame)
        self.webcam_label.pack(padx=10, pady=(40, 0))

        self.capture_button = tk.Button(
            self.left_frame,
            text="Capture Face",
            command=self.capture_image,
            height=1,
            width=15,
            font=("Arial", 15),
            background="lightblue",
        )
        self.capture_button.pack(padx=10, pady=10)

        self.name_label = tk.Label(self.right_frame, text="Name:", font=("Arial", 15))
        self.name_label.pack(padx=0, pady=(80, 0))

        self.name_entry = tk.Entry(self.right_frame, width=30)
        self.name_entry.pack(padx=10, pady=10)

        self.id_label = tk.Label(self.right_frame, text="ID:", font=("Arial", 15))
        self.id_label.pack(padx=0, pady=0)

        self.id_entry = tk.Entry(self.right_frame, width=30)
        self.id_entry.pack(padx=10, pady=10)

        self.submit_button = tk.Button(
            self.right_frame,
            text="Submit",
            command=self.submit_form,
            height=1,
            width=11,
            font=("Arial", 15),
            background="lightblue",
        )
        self.submit_button.pack(padx=10, pady=10)

        self.video_capture = cv2.VideoCapture(0)
        self.display_video()

    def display_video(self):
        ret, img = self.video_capture.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        curFaceLocations = face_recognition.face_locations(imgS)
        if len(curFaceLocations) > 0:
            faceLoc = curFaceLocations[0]
            y1, x2, y2, x1 = faceLoc
            self.face = (imgS, faceLoc)
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img)
        self.webcam_label.config(image=img_tk)
        self.webcam_label.image = img_tk
        self.after(1, self.display_video)

    def capture_image(self):
        if len(self.face) != 0:
            self.student_faces.append(self.face)
            self.camera_issue_label["text"] = (
                f"Captured {len(self.student_faces)} faces!"
            )
            self.camera_issue_label.pack()
        else:
            self.camera_issue_label["text"] = "Face not found yet!"
            self.camera_issue_label.pack()

    def submit_form(self):
        name = self.name_entry.get()
        id = self.id_entry.get()
        try:
            df = pd.read_csv(self.student_file, header=None)
            ids = df.iloc[:, 0].astype(str).tolist()
        except:
            ids = []
        if id in ids:
            self.form_issue_label["text"] = f"Id {id} is already taken!"
            self.form_issue_label.pack()

        elif len(self.student_faces) == 0:
            self.form_issue_label["text"] = "Face has not captured yet!"
            self.form_issue_label.pack()

        elif name and id:
            for face in self.student_faces:
                imgs, loc = face
                faceEncodings = face_recognition.face_encodings(imgs, [loc])[0]
                row = [id, name, *faceEncodings]
                self.store_to_csv([row])
            self.form_issue_label["text"] = "Student added successfully."
            self.form_issue_label.pack()
        else:
            self.form_issue_label["text"] = "Please fill all fields!"
            self.form_issue_label.pack()

    def store_to_csv(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.student_file, mode="a", index=False, header=False)


class TakeAttendence(tk.Frame):
    def __init__(self, master, student_file="data/students.csv"):
        super().__init__(master)
        tk.Button(
            self,
            text="Back",
            command=lambda: master.switch_frame(StartPage),
            font=("Arial", 10),
            background="lightblue",
        ).pack(pady=(5, 0))

        self.master = master
        if not exists(student_file):
            self.date = tk.Label(
                self, text=f"Student data is not available!", font=("Arial", 15)
            )
            self.date.pack(pady=(8))
            return
        df = pd.read_csv(student_file, header=None)
        data = df.to_numpy()
        self.student_ids, self.student_names, self.student_encodings = (
            data[:, 0].astype(str),
            data[:, 1].astype(str),
            data[:, 2:130].astype(float),
        )
        self.all_students = dict()
        for i, id in enumerate(self.student_ids):
            self.all_students[id] = self.student_names[i]

        self.marked = []
        self.oldfaceLoc = ()

        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.webcam_label = tk.Label(self.left_frame)
        self.webcam_label.pack(padx=10, pady=(40, 0))

        self.blank = tk.Label(self.right_frame)
        self.blank.pack(padx=0, pady=7)

        self.video_capture = cv2.VideoCapture(0)
        self.display_video()

    def display_video(self):
        ret, img = self.video_capture.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        self.curFaceLocations = face_recognition.face_locations(imgS)
        if self.oldfaceLoc != self.curFaceLocations:
            self.CurFrameEncodes = face_recognition.face_encodings(
                imgS, self.curFaceLocations
            )
        self.oldfaceLoc = self.curFaceLocations

        for encodeFace, faceLoc in zip(self.CurFrameEncodes, self.curFaceLocations):
            faceDis = np.sqrt(
                np.sum((self.student_encodings - np.array([encodeFace])) ** 2, axis=1)
            )
            matchIndex = np.argmin(faceDis)
            if faceDis[matchIndex] < 0.5:
                name = self.student_names[matchIndex].split(" ")[0]
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 30), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(
                    img,
                    name,
                    (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255),
                    1,
                )
                if self.student_ids[matchIndex] not in self.marked:
                    self.mark_attendence(self.student_ids[matchIndex])
                    self.marked.append(self.student_ids[matchIndex])

                    self.id_label = tk.Label(
                        self.right_frame,
                        text=self.student_names[matchIndex] + " is present.",
                    )
                    self.id_label.pack(padx=0, pady=0)

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_im)
        img_tk = ImageTk.PhotoImage(image=img)
        self.webcam_label.config(image=img_tk)
        self.webcam_label.image = img_tk
        self.after(1, self.display_video)

    def mark_attendence(self, id, attendence_file=""):
        year, month, day = date.year, date.month, date.day
        time = datetime.now().strftime("%H:%M:%S")
        attendence_file = rf"data/attendence {year}-{month}.csv"

        if exists(attendence_file):
            df = pd.read_csv(attendence_file)
            if str(id) in list(df["ID"].astype(str)):
                df.loc[df["ID"].astype(str) == str(id), f"Day {day}"] = time
            else:
                new_student = {
                    "ID": id,
                    "Name": self.all_students[id],
                    f"Day {day}": time,
                }
                df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
            df.to_csv(attendence_file, index=False)
        else:
            data = {"ID": self.all_students.keys(), "Name": self.all_students.values()}
            for i in range(1, 32):
                data[f"Day {i}"] = [""] * len(self.all_students)
            df = pd.DataFrame(data)
            df.loc[df["ID"] == id, f"Day {day}"] = time
            df.to_csv(attendence_file, index=False)


class CSVViewer(tk.Frame):
    def __init__(
        self, master, csv_file=rf"data/attendence {date.year}-{date.month}.csv"
    ):
        super().__init__(master)
        tk.Button(
            self,
            text="Back",
            command=lambda: master.switch_frame(StartPage),
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


if __name__ == "__main__":
    app = FacialAttendence()
    app.mainloop()
