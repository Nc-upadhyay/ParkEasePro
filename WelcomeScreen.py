import base64
import datetime
import json
from tkinter import *
from tkinter import filedialog

import cv2
import requests
from PIL import ImageTk, Image

from authKey import SECRET_KEY
from dbConnection import mycursor, connection


# GUI
root = Tk()
root.title("Welcome Screen")
# root.attributes('-fullscreen',True)
root.configure(background='#17202A')
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BG_WHITE = "#FFF"
COLOR_GREEN = "#008000"
COLOR_RED = "#FF0000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

root.geometry("1300x800")
# set minimum window size value
root.minsize(700, 700)
# set maximum window size value
root.maxsize(1350, 800)

global fare_text
fare_text = "Nothing to Show"


def show_fare():
    fare_label = Label(root, text=fare_text, bg="grey", font=("Helvetica", 15), fg="white", width=30, height=3,
                       borderwidth=5, relief="solid").place(relx=0.17, rely=0.83)


def exit_command():
    root.quit()


def select_from_camera():
    cam = cv2.VideoCapture(0)
    while True:

        _, img = cam.read()
        key = cv2.waitKey(1) & 0xff
        cv2.imshow("Capture License Number", img)
        if (key == ord('q')):
            cv2.destroyAllWindows()
            print("Captured...")
            cv2.imwrite("first1.jpg", img)
            # time.sleep(5)
            IMAGE_PATH1 = "first1.jpg"
            my_image1 = ImageTk.PhotoImage(Image.open(IMAGE_PATH1))
            my_image_label = Label(root, image=my_image1, width=650, height=300)
            my_image_label.image = my_image1
            my_image_label.place(relx=0.03, rely=0.4)

            with open(IMAGE_PATH1, 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())


            url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (
                SECRET_KEY)
            r = requests.post(url, data=img_base64)
            data = r.json()
            print(data)
            results = data.get("results", [])
            # if results is None
            first_result = results[0]
            plate_info = first_result.get("plate", "")
            print("plate_info===>" + plate_info)

            # num_plate = (json.dumps(r.json(), indent=2))
            # info = (list(num_plate.split("candidates")))
            # print(info)
            # plate = info[0]
            # plate = plate.split(',')[0:3]
            # p = plate[1]
            # print("p "+p)
            # p1 = p.split(":")
            # number = p1[1]
            # number = number.replace('"', '')
            # number = number.lstrip()
            print("==========number plate===============")
            print(plate_info)
            # print("plate "+plate[0])
            # print("plate "+plate)

            getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(plate_info)
            mycursor.execute(getnumber)
            templist = list(mycursor)
            # print(len(templist))
            # print(templist)
            if len(templist) == 0:
                temp_time = datetime.datetime.now()
                entered_time = temp_time.strftime("%Y %m %d %H %M %S")
                print("entered time ", entered_time)
                # mycursor.execute("INSERT INTO users VALUES ('{}', '{}','{}')".format(number, entered_time,))
                mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(plate_info, entered_time))
                list_of_globals = globals()
                list_of_globals['fare_text'] = "Vehicle details has been \n entered into the database"
                show_fare()
                connection.commit()
            else:
                for temp in templist:
                    # print(temp)
                    if plate_info == temp[0]:
                        print(temp[1])
                        # result = datetime.datetime.now() - temp[1]
                        current_time = datetime.datetime.now()
                        arrival_time_temp = temp[1].split('.')
                        print("arrival time temp ", arrival_time_temp[0])
                        arrival_time_temp[0] = str(arrival_time_temp[0])
                        arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                        result = current_time - arrival_time
                        print("result = ", result)
                        days = result.days
                        hours = result.seconds / 3600
                        print("hours : ", hours, "days : ", days)
                        fare = (days * 24 + hours) * 20
                        if hours < 6:
                            fare = 20

                        query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                        mycursor.execute(query)
                        connection.commit()
                        list_of_globals = globals()
                        list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0],
                                                                                                           fare)
                        show_fare()
                        print("deleted")
                        print(temp[0], fare)
            break


        elif (key == ord('w')):
            break

    cam.release()
    cv2.destroyAllWindows()
    showBoxes()


def select_from_file():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="E:/Python machine learning projects/ParkingChargeCalc_ML",
                                               title="Select A File",
                                               filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    print(root.filename)
    IMAGE_PATH = root.filename
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(root, image=my_image, width=650, height=300).place(relx=0.03, rely=0.4)

    # IMAGE_PATH = 'first1.jpg'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data=img_base64)

    num_plate = (json.dumps(r.json(), indent=2))
    data = r.json()
    print(data)
    results = data.get("results", [])
    # if results is None
    first_result = results[0]
    plate_number = first_result.get("plate", "")
    print("plate_info===>" + plate_number)
    # info = (list(num_plate.split("candidates")))
    # print("======================")
    # print(info)
    # print(num_plate)
    # plate = info[1]
    # print("plate : ", plate)
    # plate = plate.split(',')[0:3]
    # p = plate[1]
    # print("p : ", p)
    # p1 = p.split(":")
    # print("p1 : ", p1)
    # number = p1[1]
    # print("number : ", number)
    # number = number.replace('"', '')
    # number = number.lstrip()
    print(plate_number)

    getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(plate_number)
    mycursor.execute(getnumber)
    templist = list(mycursor)
    # print(len(templist))
    # print(templist)
    if len(templist) == 0:
        temp_time = datetime.datetime.now()
        entered_time = temp_time.strftime("%Y %m %d %H %M %S")
        print("entered time ", entered_time)
        mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(plate_number, entered_time))
        list_of_globals = globals()
        list_of_globals['fare_text'] = "Vehicle details has been\nentered into the database"
        show_fare()
        connection.commit()

    else:
        for temp in templist:
            # print(temp)
            if plate_number == temp[0]:
                print(temp[1])
                # result = datetime.datetime.now() - temp[1]
                current_time = datetime.datetime.now()
                arrival_time_temp = temp[1].split('.')
                print("arrival time temp ", arrival_time_temp[0])
                arrival_time_temp[0] = str(arrival_time_temp[0])
                arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                result = current_time - arrival_time
                print("result = ", result)
                days = result.days
                hours = result.seconds / 3600
                print("hours : ", hours, "days : ", days)
                fare = (days * 24 + hours) * 20
                if hours < 6:
                    fare = 20

                query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                mycursor.execute(query)
                connection.commit()
                list_of_globals = globals()
                list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0], fare)
                show_fare()
                print("deleted")
                print(temp[0], fare)

    showBoxes()


lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, justify=CENTER, padx=10, pady=10,
               width=140, height=1).grid(row=0)

parking_slot_lable = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Slot", font=FONT_BOLD).place(relx=0.8, rely=0.1)

# Creating a photoimage object to use image
photo = PhotoImage(file="images/admin.png")

# Button(root, text='Click Me !', ).pack(side=TOP)
image_from_file_button = Button(root, text="Select Image From File System", bg="yellow", font=("Helvetica", 15),
                                fg="green", bd=4, padx=1, pady=1, command=select_from_file)
image_from_camera_button = Button(root, text="Image From Camera", bg="yellow", font=("Helvetica", 15),
                                  fg="green", bd=4, padx=1, pady=1, command=select_from_camera)


def countNumberOfSlotInDB():
    query = "select count(*) from users"
    mycursor.execute(query)
    print("============number of car in parking slot")
    # print(list(mycursor)[0][0])
    n = list(mycursor)[0][0]
    return n


def createLable(param, param1, color, text):
    lable = Label(root, bg=color, fg=TEXT_COLOR, padx=3, pady=1, text=text, font=FONT_BOLD).place(relx=param,
                                                                                                  rely=param1)


def showBoxes():
    n = countNumberOfSlotInDB()
    r = 0.6
    c = 0.2
    increase = 0.06
    count_fill_color = 1
    for row in range(6):
        temp = r
        for col in range(5):
            if (count_fill_color <= n):
                createLable(temp, c, COLOR_RED, "F")
            else:
                createLable(temp, c, COLOR_GREEN, "E")
            temp += increase
            count_fill_color += 1
        c += 0.1


showBoxes()
image_from_file_button.place(relx=0.03, rely=0.1)
image_from_camera_button.place(relx=0.3, rely=0.10)
root.mainloop()
