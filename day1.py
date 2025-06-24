import cv2 
import numpy as np

#black canvas
canvas = np.zeros((640,480,3), dtype=np.uint8)

drawing = False

def draw(event, x, y,flags,param):
    global drawing

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event==cv2.EVENT_MOUSEMOVE and drawing:
        cv2.circle(canvas,(x,y),5,(255,255,255),-1)
    elif event==cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.namedWindow("Draw")
cv2.setMouseCallback("Draw",draw)

while True:
    cv2.imshow("Draw",canvas)
    key = cv2.waitKey(1)

    if key==27:
        break
    elif key==ord('c'):
        canvas[:] = 0
cv2.destroyAllWindows()

