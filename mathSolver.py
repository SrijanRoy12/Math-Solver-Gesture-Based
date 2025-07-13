import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import pyttsx3

# ========== INIT VOICE ==========
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== INIT MEDIAPIPE ==========
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ========== UTILS ==========
def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def detectGesture(hand1_data, hand2_data):
    (hand1, label1), (hand2, label2) = hand1_data, hand2_data
    f1 = count_fingers(hand1, label1)
    f2 = count_fingers(hand2, label2)
    dist = euclidean_distance(hand1.landmark[8], hand2.landmark[8])
    if f1 == 1 and f2 == 1:
        if dist < 0.06:
            return "exit"
        return "+"
    elif (f1 == 1 and f2 == 2) or (f1 == 2 and f2 == 1):
        return "-"
    elif (f1 == 1 and f2 == 3) or (f1 == 3 and f2 == 1):
        return "*"
    elif (f1 == 1 and f2 == 4) or (f1 == 4 and f2 == 1):
        return "/"
    elif f1 == 2 and f2 == 2:
        return "del"
    elif (f1 == 1 and f2 == 5) or (f1 == 5 and f2 == 1):
        return "6"
    elif (f1 == 2 and f2 == 5) or (f1 == 5 and f2 == 2):
        return "7"
    elif (f1 == 3 and f2 == 5) or (f1 == 5 and f2 == 3):
        return "8"
    elif (f1 == 4 and f2 == 5) or (f1 == 5 and f2 == 4):
        return "9"
    elif f1 == 0 and f2 == 0:
        return "="
    elif f1 == 5 and f2 == 5:
        return "clear"
    return None

def count_fingers(hand_landmarks, label):
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []
    if label == "Left":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    for ids in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[ids]].y < hand_landmarks.landmark[tip_ids[ids]-2].y else 0)
    return fingers.count(1)

# ========== INIT ==========
last_update_time = 0
delay = 1.25
expression = ""
res = ""
history = []
gesture = ""

# ========== CAMERA ==========
cap = cv.VideoCapture(0)

while True:
    success, image = cap.read()
    image = cv.flip(image, 1)
    img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    current_time = time.time()
    hand_data = []

    # Custom dark neon theme background
    image[:] = (15, 15, 25)  # Deep dark gray-blue

    # Header Bar
    cv.rectangle(image, (0, 0), (640, 40), (50, 50, 100), -1)
    cv.putText(image, 'Gesture-Based Math Solver', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 100), 2)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            label = hand_handedness.classification[0].label
            hand_data.append((hand_landmarks, label))
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv.putText(image, f'{label} Hand', 
                       (int(hand_landmarks.landmark[0].x * image.shape[1]), 
                        int(hand_landmarks.landmark[0].y * image.shape[0]) - 20),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if len(hand_data) == 1:
            hand_landmarks, label = hand_data[0]
            fingers_up = count_fingers(hand_landmarks, label)
            if 0 <= fingers_up <= 5 and current_time - last_update_time > delay:
                expression += str(fingers_up)
                last_update_time = current_time

        if len(hand_data) == 2:
            gesture = detectGesture(hand_data[0], hand_data[1])
            if gesture == "clear":
                expression = ""
                res = ""
                gesture = ""
            elif gesture == "exit":
                break
            elif gesture and current_time - last_update_time > delay:
                if gesture == "del":
                    expression = expression[:-1]
                elif gesture == "=":
                    try:
                        res = str(eval(expression))
                        history.append(f"{expression} = {res}")
                        history = history[-5:]
                        speak(f"The result is {res}")
                    except:
                        res = "Error"
                        speak("There was an error")
                else:
                    expression += gesture
                last_update_time = current_time

    # Expression
    cv.putText(image, f'Expr: {expression}', (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Result
    color = (0, 255, 128) if res != "Error" else (0, 0, 255)
    cv.putText(image, f'Result: {res}', (10, 110), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)

    # Gesture Info
    if gesture:
        cv.putText(image, f'Gesture: {gesture}', (10, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (180, 255, 180), 2)

    # History Log
    for i, line in enumerate(reversed(history)):
        cv.putText(image, line, (10, 190 + i * 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 200), 2)

    # Footer
    cv.rectangle(image, (0, 460), (640, 480), (40, 40, 90), -1)
    cv.putText(image, "Press 'Q' to Quit | 'C' to Clear", (10, 475), cv.FONT_HERSHEY_SIMPLEX, 0.6, (200, 255, 255), 1)

    cv.imshow("Math Solver", image)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
    elif key == ord('c'):
        expression = ""
        res = ""
        gesture = ""

cap.release()
cv.destroyAllWindows()
