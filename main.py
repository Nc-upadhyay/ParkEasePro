import cv2
import easyocr
from cv2.gapi.wip.draw import Image

harcascade = "haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)
cap.set(3, 440)  # width
cap.set(4, 480)  # height

min_area = 500
count = 0

while True:
    success, img = cap.read()
    plateCasCade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plate = plateCasCade.detectMultiScale(img_gray, 1.1, 4)
    for (x, y, w, h) in plate:
        area = w * h
        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "number plate ", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_crop = img[y:y + h, x:x + w]
            cv2.imshow("Vehicle Number  ", img_crop)

    cv2.imshow("result", img)

    if (cv2.waitKey(1) & 0xFF == ord('s')):
        cv2.imwrite("plates/scaned_image" + str(count) + ".jpg", img_crop)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "plated Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Result ", img)
        cv2.waitKey(500)
        count += 1
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

# image = Image("plates/scaned_image0.jpg")
reader = easyocr.Reader(['en'])
output = reader.readtext('plates/scaned_image0.jpg')
cord = output[0][1]  # number plate
print(cord)
