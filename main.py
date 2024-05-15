import tkinter as tk
from PIL import Image, ImageTk
from csv_view import CSVViewer
from add_student import AddStudent
from attendence_take import TakeAttendence

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Face Recognition Attendence System")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        img = Image.open("data/images/icon.jpg")
        self.iconphoto(True, ImageTk.PhotoImage(img))
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        if frame_class==0:
            frame_class = StartPage
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

        img = Image.open("data/images/add student.jpg")
        self.image1 = ImageTk.PhotoImage(img.resize((270, 350), 1))
        img = Image.open("data/images/take attendence.jpg")
        self.image2 = ImageTk.PhotoImage(img.resize((270, 350), 1))
        img = Image.open("data/images/display attendence.jpg")
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

if __name__ == "__main__":
    app = Application()
    app = Application()
    app.mainloop()
