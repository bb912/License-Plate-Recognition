import cv2
import time

frameWidth = 640
frameHeght = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeght)
cap.set(10, 150)


ret, frame1 = cap.read()
ret, frame2 = cap.read()
counter = 0
while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    _, thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 1000:
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    image = cv2.resize(frame1, (1280, 720))
    # out.write(image)
    cv2.imshow("LiveFeed", frame1)
    #cv2.imshow("LiveFeed", dilated)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
