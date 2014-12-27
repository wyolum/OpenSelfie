import os.path
import Image
import ImageTk

#customize this file for each event
emailSubject = "Your Postcard from the Wyolum Photobooth"
emailMsg = "Here's your picture from the http://wyolum.com photobooth!"
logopng = "logo.png"
#logopng = None
photoCaption="postcard from the xxxx event"
# albumID='6066338417811409889' ### Kevin
# albumID='5991903863088919889' ### WyoLum
albumID=None ### Put your own album ID here in single quotes like '5991903863088919889'

n_count = 5 ## how many seconds to count down before a photo is taken
m_count = 3 ## how many seconds to count for subsequent photos (like quad)

TIMELAPSE = 0 ## use 0 for no time lapse photos, at least 3 (seconds)
### set up GUI
BUTTON_FONT = ('Times', 24)
CANVAS_FONT = ("times", 50)

SIGN_ME_IN = True
#SIGN_ME_IN = False; print 'DBG:: not signing in'

ARCHIVE = True ## archive photos?
archive_dir = None

## usually not need to change these.
EXT = 'jpg'     
RAW_FILENAME = 'image.' + EXT
PROC_FILENAME = 'photo.' + EXT


class curry:
    def __init__(self, callable, *args):
        self.callable = callable
        self.args = args
    
    def __call__(self, *args):
        return self.callable(*self.args)

def customize(master):
    import Tkinter
    import tkFileDialog
    self = Tkinter.Toplevel(master)

    def string_customizer(label, initial_val, listener):
        label = ' ' * (20 - len(label)) + label
        frame = Tkinter.Frame(self)
        var = Tkinter.StringVar()
        var.set(initial_val)
        Tkinter.Label(frame, text=label).pack(side=Tkinter.LEFT)
        entry = Tkinter.Entry(frame, textvariable=var, width=60)
        var.trace('w', lambda *args:listener(var, entry))
        entry.pack(side=Tkinter.RIGHT)
        frame.pack()

    def bool_customizer(label, initial_val, listener):
        frame = Tkinter.Frame(self)
        var = Tkinter.BooleanVar()
        var.set(initial_val)
        checkbox = Tkinter.Checkbutton(self, text=label, variable=var)
        var.trace('w', lambda *args:listener(var, checkbox))
        checkbox.pack()
        frame.pack()

    def update_subj(var, wid):
        global emailSubject
        emailSubject = var.get()

    def update_msg(var, wid):
        global emailMsg
        emailMsg = var.get()
        
    def update_caption(var, wid):
        global photoCaption
        photoCaption = var.get()

    def update_albumID(var, wid):
        global albumID
        albumID = var.get()
        
    def update_n_count(var, wid):
        global n_count
        try:
            wid.config(bg='white')
            n_count = int(var.get())
        except:
            wid.config(bg='red')
            pass

    def update_m_count(var, wid):
        global n_count
        try:
            wid.config(bg='white')
            n_count = int(var.get())
        except:
            wid.config(bg='red')
            pass

    def update_timelapse(var, wid):
        global TIMELAPSE
        try:
            wid.config(bg='white')
            TIMELAPSE = int(var.get())
        except:
            wid.config(bg='red')

    def update_archive(var):
        global ARCHIVE, archive_dir
        archive_dir = var.get()
        if os.path.exists(archive_dir):
            ARCHIVE = True
        else:
            ARCHIVE = False
        
    def update_logo(entry):
        if os.path.exists(logo_var.get()):
            entry.config(bg='white')
            logopng = logo_var.get()
            photo = Image.open(logopng)
            ## photo_tk = ImageTk.PhotoImage(file=logopng) ## does not work
            photo_tk = Tkinter.PhotoImage(file=logopng) ## works on laptop, not on raspberry pi
            logo_label.config(image=photo_tk)
            logo_label.photo = photo_tk
        else:
            entry.config(bg='red')

    def logo_dialog():
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('Images', '.png'), ('all files', '.*')]
        options['initialdir'] = './'
        options['initialfile'] = logo_var.get()
        options['title'] = 'Logo finder'
        logo_file = tkFileDialog.askopenfilename(**options)
        logo_var.set(logo_file)

    def archive_dialog():
        options = {}
        options['initialdir'] = '/media'
        options['title'] = 'Select Archive Directory'
        archive_dir = tkFileDialog.askdirectory(**options)
        archive_var.set(archive_dir)

    string_customizer('Email Subject', emailSubject, update_subj)
    string_customizer('Email Msg', emailMsg, update_msg)
    string_customizer('Caption', photoCaption, update_caption)
    string_customizer('albumID', albumID, update_albumID)
    string_customizer('Countdown1', n_count, update_n_count)
    string_customizer('Countdown2', m_count, update_m_count)
    string_customizer('Timelapse', TIMELAPSE, update_timelapse)

    archive_var = Tkinter.StringVar()
    archive_var.set(archive_dir)
    archive_frame = Tkinter.Frame(self)
    Tkinter.Label(archive_frame, text='Archive File').pack(side=Tkinter.LEFT)
    archive_entry = Tkinter.Entry(archive_frame, textvariable=archive_var, width=60)
    archive_entry.pack(side=Tkinter.LEFT)
    archive_var.trace('w', curry(update_archive, archive_entry))
    Tkinter.Button(archive_frame, text='Browse', command=archive_dialog).pack(side=Tkinter.LEFT)
    archive_frame.pack(side=Tkinter.TOP)

    logo_var = Tkinter.StringVar()
    logo_var.set(logopng)
    logo_frame = Tkinter.Frame(self)
    Tkinter.Label(logo_frame, text='Logo File').pack(side=Tkinter.LEFT)
    logo_entry = Tkinter.Entry(logo_frame, textvariable=logo_var, width=60)
    logo_entry.pack(side=Tkinter.LEFT)
    logo_var.trace('w', curry(update_logo, logo_entry))
    Tkinter.Button(logo_frame, text='Browse', command=logo_dialog).pack(side=Tkinter.LEFT)
    logo_frame.pack(side=Tkinter.TOP)
    Tkinter.Button(self, text='Done', command=self.destroy).pack()
    
    photo = Image.open(logopng)
    # photo_tk = ImageTk.PhotoImage(photo) ## does not work
    photo_tk = Tkinter.PhotoImage(file=logopng) ## works but not on raspberry pi
    logo_label = Tkinter.Label(self, image=photo_tk)
    logo_label.photo = photo
    logo_label.photo_tk = photo_tk
    logo_label.pack(side=Tkinter.LEFT)

if __name__ == '__main__':
    import Tkinter
    r = Tkinter.Tk()
    b = Tkinter.Button(r, text='help', command=lambda :customize(r))
    b.pack()
    r.mainloop()
    print emailSubject
    print n_count


    
