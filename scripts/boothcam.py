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

    
SCREEN_W = 1366
SCREEN_H = 788 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COUNTDOWN_LOCATION = (500, 635)
N_COUNTDOWN = 5

FONTSIZE=100
font = ('Times', FONTSIZE)

def setup_google():
    global client
    # Create a client class which will make HTTP requests with Google Docs server.
    client = gdata.photos.service.PhotosService()
    # Authenticate using your Google Docs email address and password.
    client.ClientLogin(config.username, config.password)

def countdown(camera, can):
    camera.start_preview()
    can.delete("image")
    camera.led = False
    camera.preview_alpha = 100
    camera.preview_window = (0, 0, SCREEN_W, SCREEN_H)
    camera.preview_fullscreen = False

    led_state = False
    can.delete("all")

    for i in range(N_COUNTDOWN):
        can.delete("text")
        can.update()
        can.create_text(SCREEN_W/2 - 50, 300, text=str(N_COUNTDOWN - i), font=font, tags="text")
        can.update()
        if i < N_COUNTDOWN - 2:
            time.sleep(1)
            led_state = not led_state
            camera.led = led_state
        else:
            for j in range(5):
                time.sleep(.2)
                led_state = not led_state
                camera.led = led_state
    can.delete("text")
    can.update()
    camera.stop_preview()

def snap(can):
    global logo ,client

    camera = picamera.PiCamera()
    countdown(camera, can)
    camera.capture('image.jpg')
    camera.close()

    snap = Image.open('image.jpg')
    snap.paste(logo,(0,550),logo)
    snap.save('photo.jpg')
    return snap

def findser():
    ser = serial.Serial('/dev/ttyS0',19200, timeout=.1)
    print 'using AlaMode'
    return ser

def googleUpload(filen):
    #upload to picasa album
    album_url ='/data/feed/api/user/%s/albumid/%s' % (config.username, '5991503150459533249')
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap','Northern Virginia Mini-Maker Faire', filen ,content_type='image/jpeg')
