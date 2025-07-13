# ✨🖐️ VisionCalc – A Touchless Gesture-Powered Calculator
Gesture-Based Math Solver is a real-time calculator powered by hand gestures using OpenCV and MediaPipe. It lets you input digits and operations like +, -, *, / through gestures detected via webcam. Features include a dark-themed UI, voice feedback, expression history, and hands-free interaction.
VisionCalc is an innovative real-time calculator that interprets hand gestures through your webcam to build and solve mathematical expressions — no keyboard, no mouse, just movement. It’s designed to explore computer vision, accessibility, and futuristic human-computer interaction.

⚡ Key Highlights
🎥 Live gesture tracking via webcam

🔢 Intuitive number input with dynamic expression chaining

➕➖✖️➗ Fully gesture-controlled arithmetic operations

🧠 Instant evaluation of complex expressions

🔊 Smart voice feedback using text-to-speech

💻 No special equipment — just a standard webcam!

🧰 Tech Stack Overview
Technology	Role
Python	Programming backbone
OpenCV	Video capture, drawing, and interface rendering
MediaPipe	Landmark-based hand detection (21 keypoints)
NumPy	Distance math & logic operations
pyttsx3	Speech synthesis for vocal results

🤚 Gesture Map
Hand Gesture Combination	Function
Single hand,  1–5 fingers	Enter digits 1–5
1 hand (5 fingers) + other hand (1–4)	Input digits 6–9
Closed fist on one hand	Input digit 0
Index finger on both hands	Perform Addition (+)
Index + Two fingers	Perform Subtraction (-)
Index + Three fingers	Perform Multiplication (*)
Index + Four fingers	Perform Division (/)
Both hands closed	Evaluate (=) expression
Both hands open (5 fingers)	Reset the expression
Two fingers up on both hands	Delete last character
Index fingers close together	Exit the app

Gesture recognition is powered by spatial landmark analysis and finger position classification.
