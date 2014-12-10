#set these up in your google account
import getpass
import os.path

class Credential:
    def __init__(self):
        self.filename = '.credentials'

        if os.path.exists(self.filename):
            f = open(self.filename)
            self.key = f.readline().strip()
            self.value = f.readline().strip()
        else:
            self.key = raw_input('Google Username:')
            self.value = getpass.getpass('App Specific Password')
            f = open(self.filename, 'w')
            f.write(self.key + '\n')
            f.write(self.value + '\n')


cred = Credential()
username = cred.key
password = cred.value
gmailUser = username
gmailPassword = password
n_count = 0

TIMELAPSE = 30 ## use 0 for no time lapse photos, at least 3 (seconds)
### set up GUI
BUTTON_FONT = ('Times', 24)
CANVAS_FONT = ("times", 50)

# SIGN_ME_IN = True
SIGN_ME_IN = False; print 'DBG:: not signing in'
ARCHIVE = False
EXT = 'jpg'
RAW_FILENAME = 'image.' + EXT
PROC_FILENAME = 'photo.' + EXT
