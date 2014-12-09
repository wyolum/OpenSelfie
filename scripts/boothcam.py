import glob
import os
import os.path
import time
import picamera
from time import sleep
import gdata.photos.service
from PIL import Image
import serial
import config
import custom

if os.path.exists(custom.logopng):
    logo = Image.open(custom.logopng)
    lxsize, lysize = logo.size
else:
    logo = None
    lxsize = 0
    lysize = 0

    
SCREEN_W = 1366
SCREEN_H = 768 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
N_COUNTDOWN = 5

FONTSIZE=100
font = ('Times', FONTSIZE)

def safe_set_led(camera, state):
    try:
        camera.led = state
    except:
        pass

def setup_google():
    global client

    out = True
    try:
        # Create a client class which will make HTTP requests with Google Docs server.
        client = gdata.photos.service.PhotosService()
        # Authenticate using your Google Docs email address and password.
        client.ClientLogin(config.username, config.password)
    except KeyboardInterrupt:
        raise
    except:
        print 'could not login to Google, check .credential file'
        out = False
    return out

def countdown(camera, can, n_count):
    camera.start_preview()
    can.delete("image")
    led_state = False
    safe_set_led(camera, led_state)
    camera.preview_alpha = 100
    camera.preview_window = (0, 0, SCREEN_W, SCREEN_H)
    camera.preview_fullscreen = False

    can.delete("all")

    for i in range(n_count):
        can.delete("text")
        can.update()
        can.create_text(SCREEN_W/2 - 50, 300, text=str(n_count - i), font=font, tags="text")
        can.update()
        if i < n_count - 2:
            time.sleep(1)
            led_state = not led_state
            safe_set_led(camera, led_state)
        else:
            for j in range(5):
                time.sleep(.2)
                led_state = not led_state
                safe_set_led(camera, led_state)
    can.delete("text")
    can.update()
    camera.stop_preview()

def snap(can, n_count):
    global image_idx

    try:
        if config.ARCHIVE and os.path.exists(config.PROC_FILENAME):
            ### copy image to archive
            image_idx += 1
            os.rename(config.PROC_FILENAME, 'Archive/%s_%05d.%s' % (config.PROC_FILENAME[:-4], image_idx, config.EXT))
        camera = picamera.PiCamera()
        countdown(camera, can, n_count)
        camera.capture(config.RAW_FILENAME)
        camera.close()
    
        snapshot = Image.open(config.RAW_FILENAME)
        if logo is not None:
            # snapshot.paste(logo,(0,SCREEN_H -lysize ),logo)
            snapshot.paste(logo,(SCREEN_W/2 - logo.size[0]/2,SCREEN_H -lysize ),logo)
        snapshot.save(config.PROC_FILENAME)
    except Exception, e:
        print e
        snapshot = None
    return snapshot
snap.active = False

if config.ARCHIVE:
    if not os.path.exists('Archive'):
        os.mkdir('Archive')
    image_idx = len(glob.glob('Archive/%s_*.%s' % (config.PROC_FILENAME[:-4], config.EXT)))

def findser():
    ser = serial.Serial('/dev/ttyS0',19200, timeout=.1)
    print 'using AlaMode'
    return ser

def googleUpload(filen):
    #upload to picasa album
    album_url ='/data/feed/api/user/%s/albumid/%s' % (config.username, custom.albumID)
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap',custom.photoCaption, filen ,content_type='image/jpeg')
