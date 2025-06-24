import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    h,w,_ = frame.shape
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
           lm_list =  [(int(lm.x * w), int(lm.y *h)) for lm in hand_landmarks.landmark]
           tips_ids = [4,8,12,16,20]
           fingers = [int(lm_list[tips_ids[i]][1] < lm_list[tips_ids[i]-2][1]) for i in range(1,5)]

           total = sum(fingers)

           cv2.putText(frame, f'Fingers:{total}', (10,40), cv2.FONT_HERSHEY_COMPLEX, 1.2, (0,255,0), 2)

           mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Finger Counter', frame)

    if cv2.waitKey(1) == 27:
       break
cap.release()
cv2.destroyAllWindows()



