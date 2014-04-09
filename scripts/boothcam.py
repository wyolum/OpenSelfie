import picamera
from time import sleep
import gdata.photos.service
from PIL import Image
import serial
import config
import custom

logo = Image.open(custom.logopng)
lxsize, lysize = logo.size

def setup_google():
    global client
    # Create a client class which will make HTTP requests with Google Docs server.
    client = gdata.photos.service.PhotosService()
    # Authenticate using your Google Docs email address and password.
    client.ClientLogin(config.username, config.password)

def snap():
    global logo ,client
    camera = picamera.PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture('image.jpg')
    camera.stop_preview()
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
    album_url ='/data/feed/api/user/%s/albumid/%s' % (config.username, '5989223732309633793')
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap','Northern Virginia Mini-Maker Faire', filen ,content_type='image/jpeg')
