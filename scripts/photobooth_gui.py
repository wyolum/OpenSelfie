from boothcam import *
from Tkinter import *
import ImageTk
from mailfile import *
import custom
import Image
import config

WIDTH = 1366
HEIGHT = 788
SCALE = 2
N_COUNT = 5

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

def display_image(im=None):
    global wiftk
    
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

def check_and_snap(force=False):
    global  wiftk, Button_enabled

    if signed_in:
        send_button.config(state=ACTIVE)
        etext.config(state=ACTIVE)
    else:
        send_button.config(state=DISABLED)
        etext.config(state=DISABLED)
    

    if (Button_enabled == False):
       ser.write('e') #enable button
       Button_enabled = True
       can.delete("text")
       can.create_text(WIDTH/2, HEIGHT - 210, text="Press button when ready", font=("times", 50), tags="text")
       can.update()
    command = ser.readline().strip()
    if Button_enabled and (force or command == "snap"):
       Button_enabled = False
       can.delete("text")
       can.update()
       im = snap(can, n_count=N_COUNT)
       display_image(im)
       can.delete("text")
       can.create_text(WIDTH/2, HEIGHT - 210, text="Uploading Image", font=("times", 50), tags="text")
       can.update()
       if signed_in:
           googleUpload('photo.jpg')
       can.delete("text")
       can.create_text(WIDTH/2, HEIGHT - 210, text="Press button when ready", font=("times", 50), tags="text")
       can.update()
    else:
        if command.strip():
            print command
    if not force:
        root.after(100, check_and_snap)

def force_snap():
    check_and_snap(force=True)
#if they enter an email address send photo. add error checking
def sendPic(*args):
    global email_addr;
    print 'sending photo by email to %s' % email_addr.get()
    try:
        sendMail(email_addr.get().strip(),custom.emailSubject,custom.emailMsg,'photo.jpg')
        etext.delete(0, END)
        etext.focus_set()
    except Exception, e:
        print 'Send Failed'
        can.delete("all")
        can.create_text(WIDTH/2, HEIGHT - 210, text="Send Failed", font=("times", 50), tags="text")
        can.update()
        time.sleep(1)
        can.delete("all")
        im = Image.open("photo.jpg")
        display_image(im)
        can.create_text(WIDTH/2, HEIGHT - 210, text="Press button when ready", font=("times", 50), tags="text")
        can.update()

        
FONT = ('Times', 24)
ser = findser()
#bound to text box for email
email_addr = StringVar()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (WIDTH, HEIGHT))
root.focus_set() # <-- move focus to this widget
frame = Frame(root)
#Button(frame, text="Exit", command=quit).pack(side=LEFT)
send_button = Button(frame, text="SendEmail", command=sendPic, font=FONT)
send_button.pack(side=RIGHT)

etext = Entry(frame,width=40, textvariable=email_addr, font=FONT)
etext.pack()
frame.pack()
snap_button = Button(root, text="*snap*", command=force_snap, font=FONT)
snap_button.pack(side=RIGHT)
can = Canvas(root, width=WIDTH, height=HEIGHT)
can.pack()

if config.SIGN_ME_IN:
    signed_in = setup_google()
else:
    signed_in = False
if not signed_in:
    send_button.config(state=DISABLED)
    etext.config(state=DISABLED)

root.after(200, check_and_snap)
root.wm_title("Wyolum Photobooth")
etext.focus_set()
# etext.bind("<Enter>", sendPic)
root.mainloop()
