# Face Recognition Attendance System

This project is a desktop application built with Python and Tkinter that uses face recognition to take and manage student attendance.

## Features

*   **Add New Students:** Easily register new students by capturing their face using a webcam and entering their name and ID.
*   **Take Attendance:** Automatically mark attendance by recognizing registered students' faces in real-time via the webcam.
*   **View Attendance Reports:** Access and view monthly attendance records, which are stored in CSV files.
*   **User-Friendly Interface:** Simple graphical user interface built with Tkinter for easy navigation and operation.

## Project Structure

The project is organized as follows:

```
.
├── add_student.py        # Handles adding new students (GUI and logic)
├── attendence_take.py    # Manages taking attendance via face recognition (GUI and logic)
├── csv_view.py           # Displays monthly attendance reports (GUI and logic)
├── main.py               # Main application file, sets up Tkinter window and navigation
├── README.md             # This file
└── data/
    ├── students.csv      # Stores registered student data (ID, Name, Face Encoding)
    ├── attendence YYYY-MM.csv # Stores monthly attendance records (e.g., attendence 2023-10.csv)
    └── images/
        ├── add student.jpg       # Image for 'Add Student' button
        ├── display attendence.jpg # Image for 'View Attendence' button
        ├── icon.jpg              # Application icon
        └── take attendence.jpg   # Image for 'Take Attendence' button
```

### File Descriptions:

*   **`main.py`**: The entry point of the application. It initializes the main Tkinter window and handles navigation between different pages/frames (Add Student, Take Attendance, View Attendance).
*   **`add_student.py`**: Contains the `AddStudent` class. This module provides the UI and functionality for capturing a student's face via webcam, inputting their details (name, ID), and saving this information (including the face encoding) to `data/students.csv`.
*   **`attendence_take.py`**: Contains the `TakeAttendence` class. This module is responsible for the real-time attendance process. It loads known student face encodings, captures video from the webcam, detects faces, compares them against known faces, and records attendance in a monthly CSV file (e.g., `data/attendence 2023-10.csv`).
*   **`csv_view.py`**: Contains the `CSVViewer` class. This module allows users to view the attendance report for the current month. It reads the relevant attendance CSV file and displays it in a tabular format.
*   **`data/` directory**:
    *   `students.csv`: A CSV file where each row stores a student's ID, name, and the 128-dimension face encoding.
    *   `attendence YYYY-MM.csv`: CSV files generated monthly (e.g., `attendence 2023-10.csv`) that log the attendance. Each row typically contains student ID, name, and timestamps for each day they were marked present.
    *   `images/`: Contains static image files used within the application's GUI.

## Dependencies

This project relies on the following Python libraries:

*   **Tkinter:** For the graphical user interface. (Usually comes standard with Python)
*   **Pillow (PIL):** For image manipulation, specifically for handling images in the Tkinter UI.
    *   Installation: `pip install Pillow`
*   **pandas:** For data manipulation and CSV file operations (reading/writing student data and attendance records).
    *   Installation: `pip install pandas`
*   **NumPy:** Required by `face_recognition` for numerical operations, especially array manipulations.
    *   Installation: `pip install numpy`
*   **face_recognition:** For the core face detection and recognition capabilities.
    *   Installation: `pip install face_recognition`
    *   Note: This library depends on `dlib`, which might require C++ build tools. Refer to the official `face_recognition` documentation for detailed installation instructions if you encounter issues.
*   **OpenCV (cv2):** Used for accessing the webcam and capturing video frames.
    *   Installation: `pip install opencv-python`

## Setup and Usage

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/reshamgaire/Face-Recognization-Attendence-System.git
    cd https://github.com/reshamgaire/Face-Recognization-Attendence-System.git
    ```

2.  **Install Dependencies:**
    Ensure you have Python 3.x installed. Then, install the required libraries using pip:
    ```bash
    pip install Pillow pandas numpy face_recognition opencv-python
    ```
    *   **Important Note for `face_recognition`:** The `face_recognition` library relies on `dlib`. If you encounter issues during installation (especially on Windows or macOS), you might need to install CMake and a C++ compiler first. Please refer to the [face_recognition installation guide](https://github.com/ageitgey/face_recognition#installation) for detailed instructions specific to your operating system.

3.  **Prepare the `data` directory:**
    *   Ensure the `data/images/` directory exists and contains the necessary UI images ( `add student.jpg`, `display attendence.jpg`, `icon.jpg`, `take attendence.jpg`).
    *   The `data/students.csv` file will be created automatically when you add the first student.
    *   Attendance files (`data/attendence YYYY-MM.csv`) will be created automatically when attendance is taken for a new month.

4.  **Run the Application:**
    Execute the `main.py` script:
    ```bash
    python main.py
    ```

5.  **Using the Application:**
    *   **Add Student:** Click the "Add Student" button. The application will access your webcam. Position your face clearly in the frame and click "Capture Face". Fill in your Name and a unique ID, then click "Submit".
    *   **Take Attendance:** Click "Take Attendance". The system will use the webcam to detect and recognize registered students. Attendance will be automatically recorded.
    *   **View Attendance:** Click "View Attendance" to see the attendance report for the current month.

## Data Storage

*   **Student Information (`data/students.csv`):**
    *   This CSV file stores the information for all registered students.
    *   Each row represents a student and contains:
        *   `ID`: The unique identifier for the student.
        *   `Name`: The name of the student.
        *   `Face Encoding`: A 128-dimension numerical representation of the student's face, used for recognition. (Stored across 128 columns).
    *   This file is created if it doesn't exist when the first student is added.

*   **Attendance Records (`data/attendence YYYY-MM.csv`):**
    *   Attendance is recorded in separate CSV files for each month (e.g., `attendence 2023-10.csv` for October 2023).
    *   These files are stored in the `data/` directory.
    *   Each file contains:
        *   `ID`: Student's ID.
        *   `Name`: Student's Name.
        *   `Day 1`, `Day 2`, ..., `Day 31`: Columns representing each day of the month. The cell for a particular student and day will contain the timestamp (HH:MM:SS) when they were marked present. If absent, it might be empty or marked as "ABS" (depending on the `csv_view.py` display logic).
    *   A new attendance file is created automatically if one doesn't exist when attendance is taken for the first time in a new month.

## Screenshots

The application's user interface is straightforward. Key visual elements and workflow can be understood easily from the main navigation buttons.
