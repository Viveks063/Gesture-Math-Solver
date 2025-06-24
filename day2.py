import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame,1)

    cv2.imshow("WebCam",frame)

    key = cv2.waitKey(1)

    if key==ord('s'):
        cv2.imwrite("snapshot.png",frame)
    elif key==27:
        break
cap.release()
cv2.destroyAllWindows()