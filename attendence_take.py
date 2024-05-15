import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import face_recognition
import cv2
from datetime import datetime
from os.path import exists

date = datetime.today().date()

class TakeAttendence(tk.Frame):
    def __init__(self, master, student_file="data/students.csv"):
        super().__init__(master)
        tk.Button(
            self,
            text="Back",
            command=lambda: master.switch_frame(0),
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

        img = Image.fromarray(img)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = np.array(img)
        
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
            if faceDis[matchIndex] < 0.4:
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

