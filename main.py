import cv2
import mediapipe as mp
import numpy as np
import pytesseract
import re
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam capture
cap = cv2.VideoCapture(0)

# Drawing canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)
drawing = False
prev_x, prev_y = 0, 0

# Cooldown control
last_trigger_time = 0
trigger_cooldown = 2  # seconds
result_text = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            tip_ids = [4, 8, 12, 16, 20]

            fingers_up = [int(lm_list[tip_ids[i]][1] < lm_list[tip_ids[i]-2][1]) for i in range(1, 5)]
            finger_count = sum(fingers_up)
            index_tip = lm_list[8]

            if finger_count == 1:
                cv2.circle(frame, index_tip, 8, (255, 0, 255), -1)
                if not drawing:
                    drawing = True
                    prev_x, prev_y = index_tip
                cv2.line(canvas, (prev_x, prev_y), index_tip, (255, 255, 255), 5)
                prev_x, prev_y = index_tip
            else:
                drawing = False
                prev_x, prev_y = 0, 0

            if finger_count == 2:
                if time.time() - last_trigger_time > trigger_cooldown:
                    last_trigger_time = time.time()
                    cv2.putText(frame, "Processing...", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    cv2.imwrite("drawn_expression.png", canvas)
                    print("Saved drawing as 'drawn_expression.png'")

                    # OCR and evaluate
                    ocr_result = pytesseract.image_to_string("drawn_expression.png", config="--psm 6")
                    print("OCR Output:", ocr_result)
                    expression = re.sub(r'[^0-9+\-*/().]', '', ocr_result)
                    print("Parsed Expression:", expression)
                    try:
                        result_text = f"{expression} = {eval(expression)}"
                    except:
                        result_text = "Could not evaluate"

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    merged = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Display result text if any
    if result_text:
        cv2.putText(merged, result_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Air Math Drawing", merged)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        result_text = ""

cap.release()
cv2.destroyAllWindows()
