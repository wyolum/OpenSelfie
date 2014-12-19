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

## usually not need to change these.
EXT = 'jpg'     
RAW_FILENAME = 'image.' + EXT
PROC_FILENAME = 'photo.' + EXT

