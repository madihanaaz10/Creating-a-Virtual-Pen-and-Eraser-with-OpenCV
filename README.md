# Creating-a-Virtual-Pen-and-Eraser-with-OpenCV
# Project Overview
This project presents an interactive **Virtual Canvas** application that leverages Computer Vision and Human-Computer Interaction (HCI) concepts. Using a standard webcam, the system tracks hand gestures in real-time, allowing users to draw, paint, select custom shapes (like rectangles or ellipses), adjust brush thickness, and erase sketches directly in the air without any physical hardware.

The system uses advanced landmark tracking to switch between **Selection Mode** (two fingers raised) to navigate the header menu, and **Drawing Mode** (index finger raised) to paint on a digital canvas.

# Tech Stack & Dependencies
* **Language:** Python
* **Core Frameworks:** * `OpenCV` (Real-time image frame processing, canvas blending, and matrix manipulation)
  * `MediaPipe` / `cvzone` (Hand landmark tracking and finger gesture classification)
  * `NumPy` (Black canvas generation and matrix logic)

# Hand Gestures & Control Logic
* Selection Mode:* Raise both the **Index and Middle fingers**. This allows you to hover over the header template images to pick colors or choose shapes.
* Drawing/Freestyle Mode:** Raise **only the Index finger**. Move your hand in the air to draw on screen.
* Shape Confirmation:*Raise your **Pinky finger** while positioning a shape to stamp it permanently onto your canvas layers.
* Clear Screen:* Raise **three fingers (Middle, Ring, Pinky)** simultaneously to instantly clear the digital canvas matrix back to empty.
