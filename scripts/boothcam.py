import time
import picamera
from time import sleep
import gdata.photos.service
from PIL import Image
import serial
import config
import custom

logo = Image.open(custom.logopng)
lxsize, lysize = logo.size

    
SCREEN_W = 1280
SCREEN_H = 720 
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
        print 'could not login to Google'
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
    global logo ,client

    camera = picamera.PiCamera()
    countdown(camera, can, n_count)
    camera.capture('image.jpg')
    camera.close()

    snap = Image.open('image.jpg')
    snap.paste(logo,(0,SCREEN_H -lysize ),logo)
    snap.save('photo.jpg')
    return snap

def findser():
    ser = serial.Serial('/dev/ttyS0',19200, timeout=.1)
    print 'using AlaMode'
    return ser

def googleUpload(filen):
    #upload to picasa album
    album_url ='/data/feed/api/user/%s/albumid/%s' % (config.username, custom.albumID)
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap',custom.photoCaption, filen ,content_type='image/jpeg')
