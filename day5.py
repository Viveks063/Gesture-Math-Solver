import pytesseract
import cv2

img = cv2.imread("snapshot.png")

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

text = pytesseract.image_to_string(grey, config='--psm 6')

print("Result: ", text)