import tkSimpleDialog
import os.path
import Image
import ImageTk
import ConfigParser
import os.path

install_dir = os.path.split(os.path.abspath(__file__))[0]
conf_filename = os.path.join(install_dir, 'openselfie.conf')

def restore_conf():
    global emailSubject, emailMsg, photoCaption, logopng, albumID, countdown1, countdown2
    global TIMELAPSE, SIGN_ME_IN, ARCHIVE, archive_dir, logo, lxsize, lysize

    if not os.path.exists('openselfie.conf'):
        conf_file = open(conf_filename, 'w')
        default_conf = '''[main]
emailsubject = Your Postcard from the Wyolum Photobooth
emailmsg = Here's your picture from the http://wyolum.com photobooth!
photocaption = postcard from the xxx event
logopng = logo.png
photo_tk = None
albumid = None
countdown1 = 5
countdown2 = 3
timelapse = 0
sign_me_in = True
archive = True
archive_dir = %s/Photos/
''' % install_dir
        conf_file.write(default_conf)
        conf_file.close()
    if not os.path.exists('openselfie.conf'):
        raise ValueError('Configuration file "openselfie.conf" is missing.')

    conf = ConfigParser.ConfigParser()
    conf.read('openselfie.conf')

    emailSubject = conf.get('main', 'emailSubject') # "Your Postcard from the Wyolum Photobooth"
    emailMsg = conf.get('main', 'emailMsg') # "Here's your picture from the http://wyolum.com photobooth!"
    logopng = conf.get('main', 'logopng') # "logo.png"

    if os.path.exists(logopng):
        logo = Image.open(logopng)
        lxsize, lysize = logo.size
    else:
        logo = None
        lxsize = 0
        lysize = 0

    photoCaption = conf.get('main', 'photoCaption') # "postcard from the xxxx event"
    # albumID='6066338417811409889' ### Kevin
    # albumID='5991903863088919889' ### WyoLum
    albumID = conf.get('main', 'albumID') # None ### Put your own album ID here in single quotes like '5991903863088919889'

    countdown1 = int(conf.get('main', 'countdown1')) # 5 ## how many seconds to count down before a photo is taken
    countdown2 = int(conf.get('main', 'countdown2')) # 3 ## how many seconds to count down before subsequent photos are taken

    TIMELAPSE = int(conf.get('main', 'TIMELAPSE')) # 0 ## use 0 for no time lapse photos, at least 3 (seconds)
    SIGN_ME_IN = bool(conf.get('main', 'SIGN_ME_IN')) # True

    ARCHIVE = bool(conf.get('main', 'ARCHIVE')) # True ## archive photos?
    archive_dir = conf.get('main', 'archive_dir') # './'

restore_conf()

### set up GUI
BUTTON_FONT = ('Times', 24)
CANVAS_FONT = ("times", 50)

## usually not need to change these.
EXT = 'jpg'     
RAW_FILENAME = 'image.' + EXT
PROC_FILENAME = 'photo.' + EXT

class AskBoolean(tkSimpleDialog.Dialog):
    def apply(self):
        self.result = True

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
        
    def update_countdown1(var, wid):
        global countdown1
        try:
            wid.config(bg='white')
            countdown1 = int(var.get())
        except:
            wid.config(bg='red')
            pass

    def update_countdown2(var, wid):
        global countdown2
        try:
            wid.config(bg='white')
            countdown2 = int(var.get())
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
        global logopng, photo_tk
        if os.path.exists(logo_var.get()):
            entry.config(bg='white')
            logopng = logo_var.get()
            if True: ## DISPLAY_LOGO 
                photo = Image.open(logopng)
                photo_tk = ImageTk.PhotoImage(photo)
                logo_label.config(image=photo_tk)
                logo_label.photo = photo_tk
        else:
            entry.config(bg='red')
            logopng = 'None'

    def update_and_close(*argss):
        global logo, lxsize, lysize
        if os.path.exists(logopng):
            logo = Image.open(logopng)
            lxsize, lysize = logo.size
        else:
            logo = None
            lxsize = 0
            lysize = 0

        ## save popup dialog
        save_dialog = AskBoolean(self, title='Save configuration?')
        if save_dialog.result:
            conf = ConfigParser.ConfigParser()
            conf.add_section('main')
            conf.set('main', 'emailSubject', emailSubject)
            conf.set('main', 'emailMsg', emailMsg)
            conf.set('main', 'photoCaption', photoCaption)
            conf.set('main', 'logopng', logopng)
            conf.set('main', 'albumID', albumID)
            conf.set('main', 'countdown1', countdown1)
            conf.set('main', 'countdown2', countdown2)
            conf.set('main', 'TIMELAPSE', TIMELAPSE)
            conf.set('main', 'SIGN_ME_IN', SIGN_ME_IN)
            conf.set('main', 'ARCHIVE', ARCHIVE)
            conf.set('main', 'archive_dir', archive_dir)
            f = open(conf_filename, 'w')
            conf.write(f)
            print 'wrote', f.name
        else:
            restore_conf()
        self.destroy()
        

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
    string_customizer('Countdown1', countdown1, update_countdown1)
    string_customizer('Countdown2', countdown2, update_countdown2)
    string_customizer('Timelapse', TIMELAPSE, update_timelapse)

    archive_var = Tkinter.StringVar()
    archive_var.set(archive_dir)
    archive_frame = Tkinter.Frame(self)
    Tkinter.Label(archive_frame, text='Archive Directory').pack(side=Tkinter.LEFT)
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
    buttonbox = Tkinter.Frame(self)
    ##  Tkinter.Button(buttonbox, text='Cancel', command=self.destroy).pack(side=Tkinter.LEFT) changes are stored when they are made. cancel is harder than this
    Tkinter.Button(buttonbox, text='Done', command=update_and_close).pack(side=Tkinter.LEFT)
    buttonbox.pack()
    
    if True: # DISPLAY_LOGO:
        photo = Image.open(logopng)
        photo_tk = ImageTk.PhotoImage(photo) ## does not work
        #photo_tk = Tkinter.PhotoImage(file=logopng) ## works but not on raspberry pi
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
    print emailMsg
    print photoCaption
    print countdown1
    print countdown2
    print TIMELAPSE
    print ARCHIVE
    print archive_dir
    print logopng
    



    
