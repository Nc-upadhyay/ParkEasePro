import cv2
import pickle
import cvzone
import numpy as np


# cap = cv2.VideoCapture('http://192.168.0.104:8080/video')
cap = cv2.VideoCapture('./images/carPark.mp4')
width, height = 103, 43
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass


cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)


def checkSpaces():
    spaces = 0
    for pos in posList:
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)
            thic = 5
            spaces += 1

        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                       colorR=(0, 200, 0))


while True:

    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # img = cv2.imread('img.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    checkSpaces()
    # Display Output

    cv2.imshow("Image", img)
    # cv2.imshow("ImageGray", imgThres)
    # cv2.imshow("ImageBlur", imgBlur)
    key = cv2.waitKey(1)
    if key == ord('r'):
        pass
    if key == ord('q'):
        break






# from tkinter import *
#
# root = Tk()
# # root.attributes('-fullscreen',True) // this attribute show frame in full screen
# root.title("Parking System Design by DNR")
#
#
# def showTitle():
#     titleLabel = Label(root, text="Smart Parking System", font=("Helvetica", 15), width=30, height=3)
#     titleLabel.pack()
#
#
# def select_Image_From_System():
#     print("ok")
#
#
# def exit_command():
#     root.quit()
#
#
# showTitle()
# exit_button = Button(root, text="EXIT", command=exit_command, bg="brown", font=("Helvetica", 15), fg="white", bd=4,
#                      padx=2, pady=4)
# exit_button.pack()
# exit_button.place(relx="0.8", rely="0.9")
#
# image_from_file_btn = Button(root, text="Select Image From File System", bg="yellow", font=("Helvetica", 15),
#                                 fg="green", bd=4, padx=2, pady=4, command=select_Image_From_System)
# image_from_file_btn.pack()
# image_from_file_btn.place(relx="0.05", rely="0.2")
#
# # titleLabel.grid(column=0,row=1,padx=150,pady=5) // show label in specific location
# # myLabel.pack()
# # Window frame size
# root.geometry("600x600")
# # set minimum window size value
# root.minsize(200, 200)
# # set maximum window size value
# root.maxsize(800, 800)
# root.mainloop()
