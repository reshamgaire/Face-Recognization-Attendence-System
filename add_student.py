import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import face_recognition
import cv2


class AddStudent(tk.Frame):
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
        self.pack(fill="both", expand=True)
        self.student_file = student_file
        self.student_face = ()
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

        img = Image.fromarray(img)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = np.array(img)

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
            self.student_face = self.face
            self.camera_issue_label["text"] = "Face captured!"
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

        elif len(self.student_face) == 0:
            self.form_issue_label["text"] = "Face has not captured yet!"
            self.form_issue_label.pack()

        elif name and id:
            imgs, loc = self.student_face
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
