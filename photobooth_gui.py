from boothcam import *
from Tkinter import *
import ImageTk
from mailfile import *

WIDTH = 1280
HEIGHT = 800
SCALE = 2

root = Tk()
Button_enabled = False

def quit():
    root.destroy()

import signal
TIMEOUT = .3 # number of seconds your want for timeout

def interrupted(signum, frame):
    "called when read times out"
    print 'interrupted!'
    signal.signal(signal.SIGALRM, interrupted)

def check_and_snap():
    global  wiftk, Button_enabled

    can.delete("text")
    tid = can.create_text(WIDTH/2, HEIGHT - 110, text="Press button when ready", font=("times", 50), tags="text")
    can.update()
    if (Button_enabled == False):
       ser.write('e') #enable button
       Button_enabled = True
    command = ser.readline().strip()
    if command == "snap":
       Button_enabled = False
       im = snap()
       x,y = im.size
       x/= SCALE
       y/= SCALE
       im = im.resize((x,y));
       wiftk = ImageTk.PhotoImage(im)
            
       can.delete("image")
       can.create_image([(WIDTH + x) / 2 - x/2,
                              0 + y / 2], 
                            image=wiftk, 
                            tags="image")
       can.delete("text")

       tid = can.create_text(WIDTH/2, HEIGHT - 110, text="Uploading Image", font=("times", 50), tags="text")
       can.update()
       googleUpload('photo.jpg')
    else:
       print command
    root.after(100, check_and_snap)

#if they enter an email address send photo. add error checking
def sendPic():
    global email_addr;
    print 'sending photo by email to %s' % email_addr.get()
    sendMail(email_addr.get(),"Greetings from NoVa Maker Faire", "Here's your picture from the Wyolum Photobooth",'photo.jpg')
            
        

ser = findser()
#bound to text box for email
email_addr = StringVar()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
root.focus_set() # <-- move focus to this widget
frame = Frame(root)
#Button(frame, text="Exit", command=quit).pack(side=LEFT)
Button(frame, text="SendEmail", command=sendPic).pack(side=RIGHT)
etext = Entry(frame,textvariable=email_addr).pack(side=LEFT)
frame.pack()
can = Canvas(root, width=WIDTH, height=HEIGHT)
can.pack()
setup_google()
root.after(100, check_and_snap)
root.wm_title("Wyolum Photobooth")
root.mainloop()
