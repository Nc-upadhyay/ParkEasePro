from tkinter import *

root = Tk()
# root.attributes('-fullscreen',True) // this attribute show frame in full screen
root.title("Parking System")


def showTitle():
    titleLabel = Label(root, text="Smart Parking System", font=("Helvetica", 15), width=30, height=3)
    titleLabel.pack()


def select_Image_From_System():
    print("ok")


def exit_command():
    root.quit()


showTitle()
exit_button = Button(root, text="EXIT", command=exit_command, bg="brown", font=("Helvetica", 15), fg="white", bd=4,
                     padx=2, pady=4)
exit_button.pack()
exit_button.place(relx="0.8", rely="0.9")

image_from_file_btn = Button(root, text="Select Image From File System", bg="yellow", font=("Helvetica", 15),
                                fg="green", bd=4, padx=2, pady=4, command=select_Image_From_System)
image_from_file_btn.pack()
image_from_file_btn.place(relx="0.05", rely="0.2")

# titleLabel.grid(column=0,row=1,padx=150,pady=5) // show label in specific location
# myLabel.pack()
# Window frame size
root.geometry("600x600")
# set minimum window size value
root.minsize(200, 200)
# set maximum window size value
root.maxsize(800, 800)
root.mainloop()
