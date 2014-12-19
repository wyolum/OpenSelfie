from subprocess import call
import tkFileDialog
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

if custom.logopng and os.path.exists(custom.logopng):
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

def setLights(r, g, b):
    ser = findser()
    rgb_command = 'c%s%s%s' % (chr(r), chr(g), chr(b))
    ser.write(rgb_command)

def snap(can, n_count, effect='None'):
    global image_idx

    try:
        if custom.ARCHIVE and os.path.exists(custom.PROC_FILENAME):
            ### copy image to archive
            image_idx += 1
            new_filename = os.path.join(custom.archive_dir, '%s_%05d.%s' % (custom.PROC_FILENAME[:-4], image_idx, custom.EXT))
            command = (['cp', custom.PROC_FILENAME, new_filename])
            call(command)
        camera = picamera.PiCamera()
        countdown(camera, can, n_count)
        if effect == 'None':
            camera.capture(custom.RAW_FILENAME, resize=(1366, 768))
            snapshot = Image.open(custom.RAW_FILENAME)
        elif effect == 'Warhol': 
            #  set light to R, take photo, G, take photo, B, take photo, Y, take photo
            # merge results into one image
            setLights(255, 0, 0) ## RED
            camera.capture(custom.RAW_FILENAME[:-4] + '_1.' + custom.EXT, resize=(683, 384))
            setLights(0, 255, 0) ## GREEN
            camera.capture(custom.RAW_FILENAME[:-4] + '_2.' + custom.EXT, resize=(683, 384))
            setLights(0, 0, 255) ## BLUE
            camera.capture(custom.RAW_FILENAME[:-4] + '_3.' + custom.EXT, resize=(683, 384))
            setLights(180, 180, 0) ## yellow of same intensity
            camera.capture(custom.RAW_FILENAME[:-4] + '_4.' + custom.EXT, resize=(683, 384))

            snapshot = Image.new('RGBA', (1366, 768))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_1.' + custom.EXT).resize((683, 384)), (  0,   0,  683, 384))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_2.' + custom.EXT).resize((683, 384)), (683,   0, 1366, 384))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_3.' + custom.EXT).resize((683, 384)), (  0, 384,  683, 768))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_4.' + custom.EXT).resize((683, 384)), (683, 384, 1366, 768))
        elif effect == "Four":
            # take 4 photos and merge into one image.
            camera.capture(custom.RAW_FILENAME[:-4] + '_1.' + custom.EXT, resize=(683, 384))
            countdown(camera, can, custom.m_count)
            camera.capture(custom.RAW_FILENAME[:-4] + '_2.' + custom.EXT, resize=(683, 384))
            countdown(camera, can, custom.m_count)
            camera.capture(custom.RAW_FILENAME[:-4] + '_3.' + custom.EXT, resize=(683, 384))
            countdown(camera, can, custom.m_count)
            camera.capture(custom.RAW_FILENAME[:-4] + '_4.' + custom.EXT, resize=(683, 384))

            snapshot = Image.new('RGBA', (1366, 768))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_1.' + custom.EXT).resize((683, 384)), (  0,   0,  683, 384))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_2.' + custom.EXT).resize((683, 384)), (683,   0, 1366, 384))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_3.' + custom.EXT).resize((683, 384)), (  0, 384,  683, 768))
            snapshot.paste(Image.open(custom.RAW_FILENAME[:-4] + '_4.' + custom.EXT).resize((683, 384)), (683, 384, 1366, 768))
            
        camera.close()
            
    
        if logo is not None:
            # snapshot.paste(logo,(0,SCREEN_H -lysize ),logo)
            snapshot.paste(logo,(SCREEN_W/2 - logo.size[0]/2,SCREEN_H -lysize ),logo)
        snapshot.save(custom.PROC_FILENAME)
    except Exception, e:
        print e
        snapshot = None
    return snapshot
snap.active = False

if custom.ARCHIVE:
    custom.archive_dir = tkFileDialog.askdirectory(message="Choose archive directory.", initialdir='/media/')
    if custom.archive_dir == '':
        print 'Directory not found.  Not archiving'
        custom.ARCHIVE = False
    elif not os.path.exists(custom.archive_dir):
        os.mkdir(custom.archive_dir)
    image_idx = len(glob.glob(os.path.join(custom.archive_dir, '%s_*.%s' % (custom.PROC_FILENAME[:-4], custom.EXT))))

SERIAL = None
def findser():
    global SERIAL
    if SERIAL is None: ## singleton
        SERIAL = serial.Serial('/dev/ttyS0',19200, timeout=.1)
        print 'using AlaMode'
    return SERIAL


def googleUpload(filen):
    #upload to picasa album
    album_url ='/data/feed/api/user/%s/albumid/%s' % (config.username, custom.albumID)
    photo = client.InsertPhotoSimple(album_url,'NoVa Snap',custom.photoCaption, filen ,content_type='image/jpeg')
