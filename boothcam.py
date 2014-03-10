import picamera
from time import sleep
import gdata.photos.service
from PIL import Image
import serial

logo = Image.open('logo.png')
lxsize, lysize = logo.size
#set these up in your google account
username = 'XXXXXXX@gmail.com'
password = 'YYYYYYYYYYYYY'
def setup_google():
    global client,username,password
    # Create a client class which will make HTTP requests with Google Docs server.
    client = gdata.photos.service.PhotosService()
    # Authenticate using your Google Docs email address and password.
    client.ClientLogin(username, password)

def snap():
    global logo, username,client
    camera = picamera.PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture('image.jpg')
    camera.stop_preview()
    camera.close()
    snap = Image.open('image.jpg')
    snap.paste(logo,(0,550),logo)
    snap.save('photo.jpg')
    #upload to picasa album
    album_url ='/data/feed/api/user/%s/albumid/%s' % (username, '5989223732309633793')
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap','Northern Virginia Mini-Maker Faire', 'photo.jpg',content_type='image/jpeg')
    return snap

def findser():
    ser = serial.Serial('/dev/ttyS0',19200, timeout=.1)
    print 'using AlaMode'
    return ser

