# ✋🤖 Gesture-Based Math Solver

This AI-powered app allows users to draw math equations in the air using their **fingers** and solves them in real time. It uses **MediaPipe** for hand tracking, **OpenCV** for visual interaction, and **Tesseract OCR** to read the drawn math expression and calculate the result.


## Features

- **Hand-tracking-based drawing** using only your index finger
- Solve simple math equations drawn in the air
- Recognizes the drawn expression using **Tesseract OCR**
- Displays both the handwritten expression and the result
- Real-time interaction using webcam



## Tech Stack

- Python
- OpenCV
- MediaPipe (for finger tracking)
- Pytesseract (for OCR)
- Numpy


## How It Works

1. Open your webcam
2. Use your **index finger** to write in the air — the path will appear on screen
3. When you're done writing, press a key (e.g., `e`) to extract the expression
4. The app runs OCR on the drawing and solves the equation
5. Result is printed on the screen

