#!/usr/bin/env python

from threading import Thread, Timer
from phue import Bridge
import subprocess
import draw
import time
import sys
import platform
import run
import datetime
from datetime import  timedelta
import globals
import os
import colorsys
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from PIL import Image
import requests
from io import BytesIO
import pytz

if platform.system() == "Windows":
  debug = True
else:
  debug = False


if debug:
  import pygame
else:
  from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Color:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b

  def toString(self):
    return "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

  def toRGB(self):
    return (int(self.r), int(self.g), int(self.b))

class Matrix:
  def __init__(self):
    self.width = 64
    self.height = 32
    defaultColor = Color(0,0,0)
    self.values = []

    self.debug = debug

    for y in range(self.height):
      row = []
      for x in range(self.width):
        row.append(defaultColor)
      self.values.append(row)

    if self.debug:
      self.pygame = pygame
      self.pygame.init()
      self.pixelModifier = 8
      self.surface = pygame.display.set_mode((self.width*self.pixelModifier + self.width, self.height*self.pixelModifier + self.height))
      self.pygame.display.set_caption("LED Matrix Simulator")
    else:
      options = RGBMatrixOptions()
      options.rows = self.height
      options.cols = self.width
      options.hardware_mapping = 'adafruit-hat-pwm'

      self.matrix = RGBMatrix(options = options)
      self.canvas = self.matrix.CreateFrameCanvas()

  def calculateBrightness(self, ignoreGpio):

    if not ignoreGpio:
      try:
        proc = subprocess.Popen("gpio -g mode 2 out; gpio -g mode 19 in; gpio -g write 2 1; gpio -g read 19", shell=True, stdout=subprocess.PIPE)
        switch = int(proc.stdout.read())
      except LookupError:
        print("Reading switch GPIO failed! Defaulting to On. This probably means that the SD card has slipped out D:")
        switch = 1

    if not ignoreGpio and switch == 0:
      globals.brightness = 0

    elif globals.strobe or globals.rainbow or (globals.useHue and globals.hueConnected):
      globals.brightness = 1


  def calculateClockColour(self, rgb):

    try:
      bulbOn = globals.hueOnBulb.on
    except:
      bulbOn = False

    lightsOn = globals.hueConnected and bulbOn

    if lightsOn:
      rgb.r = globals.nightr
      rgb.g = globals.nightg
      rgb.b = globals.nightb
    else:
      rgb.r = globals.nightr
      rgb.g = globals.nightg
      rgb.b = globals.nightb
    return rgb

  def calculateBgBrightness(self):

    try:
      bulbOn = globals.hueOnBulb.on
    except:
      bulbOn = False

    lightsOn = globals.hueConnected and bulbOn

    if lightsOn:
      return globals.brightness
    
    return globals.nightBrightness

    

  def update(self):

    if self.debug:
      for event in self.pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == self.pygame.QUIT:
            return -1

      self.surface.fill((0,0,0))

      x = 0
      y = 0

      self.calculateBrightness(True)

      for i in range(self.height):
        for j in range(self.width):
          rgb = self.values[i][j]
          rgb = rgb.toRGB()

          self.pygame.draw.rect(self.surface, rgb, self.pygame.Rect(x, y, self.pixelModifier, self.pixelModifier))
          x += self.pixelModifier + 1
        x = 0
        y += self.pixelModifier + 1
      
      self.pygame.display.flip()

    else:
      self.canvas.Clear()
      self.calculateBrightness(False)

      for i in range(self.height):
        for j in range(self.width):
          if self.values[i][j].toRGB() != (0,0,0):
            rgb = self.values[i][j]
            self.canvas.SetPixel(j, i, int(rgb.r), int(rgb.g), int(rgb.b))

      self.canvas = self.matrix.SwapOnVSync(self.canvas)
    
    return 0

  def swap(self):
    if self.debug:
      self.pygame.display.flip()
    else:
      self.canvas = self.matrix.SwapOnVSync(self.canvas)

  def setBG(self, color):
    for y in range(self.height):
      for x in range(self.width):
        self.values[y][x] = color

  def clear(self):
    self.setBG(Color(0,0,0))

  def setPixel(self, x, y, color):
    if x >= self.width:
      print(str(x) + " is out of bounds.")
      return
    if y >= self.height:
      print(str(y) + " is out of bounds.")
      return

    self.values[y][x] = color

  def start(self):

    strobe = False

    print("Running LED Manager. Pres Ctrl+C to quit.")

    with open("./data/clockcolour", "r") as file:
      rgbStr = file.read()
      rgbStr = rgbStr.split(",")

      globals.r = rgbStr[0]
      globals.g = rgbStr[1]
      globals.b = rgbStr[2]

    with open("./data/nightclockcolour", "r") as file:
      rgbStr = file.read()
      rgbStr = rgbStr.split(",")

      globals.nightr = int(rgbStr[0])
      globals.nightg = int(rgbStr[1])
      globals.nightb = int(rgbStr[2])

    with open("./data/spotifykeys", "r") as file:
      keys = file.read()
      keys = keys.split(",")

    scope = 'user-read-currently-playing user-read-playback-state'
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=keys[0], client_secret=keys[1], redirect_uri="http://localhost:8888/callback", scope=scope))
      
    drawClock = True

    current_track = None

    im = Image.open('img/spring.png').convert('RGB')
    pxSpring = im.load()
    im = Image.open('img/summer.png').convert('RGB')
    pxSummer = im.load()
    im = Image.open('img/autumn.png').convert('RGB')
    pxAutumn = im.load()
    im = Image.open('img/winter.png').convert('RGB')
    pxWinter = im.load()

    px = pxSpring
  
    while True:

      r = int(globals.r)
      g = int(globals.g)
      b = int(globals.b)


      if globals.hueConnected and globals.useHue:

        try:
          color = getHueColor()

          r = color[0]
          g = color[1]
          b = color[2]

        except:
          print("Lost connection to Hue.")
          globals.hueConnected = False

        
      if globals.image != []:
        drawClock = False

        x = 0
        y = 0
        
        self.clear()

        for rgb in globals.image:
          self.setPixel(x, y, Color(rgb[0], rgb[1], rgb[2]))
          x += 1

          if x == 64:
            x = 0
            y += 1

      elif globals.strobe:
        drawClock = False
        self.setBG(Color(r, g, b))
        self.update()
        self.setBG(Color(0, 0, 0))
        self.update()

      elif globals.rainbow:
        drawClock = False
        h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
        r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]

        self.setBG(Color(r, g, b))
        self.update()
        time.sleep(0.5)

      else:
        month = int(datetime.datetime.now().strftime("%m"))
        brightness = self.calculateBgBrightness()

        if month > 2 and month < 6:
          px = pxSpring
        elif month > 5 and month < 9:
          px = pxSummer
        elif month > 8 and month < 12:
          px = pxAutumn
        else:
          px = pxWinter

        for x in range(64):
          for y in range(32):
            col = px[x, y]
            self.setPixel(x, y, Color(col[0] * brightness, col[1] * brightness, col[2] * brightness))

        try:
          current_track = spotify.current_playback(additional_types=["episode"])

          if current_track and current_track["is_playing"]:

            if current_track["currently_playing_type"] == "episode":
              url = current_track["item"]["images"][0]["url"]
            
            else:
              url = current_track["item"]["album"]["images"][0]["url"]

            response = requests.get(url)
            im = Image.open(BytesIO(response.content)).convert('RGB')
            im = im.resize((30, 30))
            px = im.load()

            for x in range(2, 30):
              for y in range(2, 30):
                col = px[x-2, y-2]
                self.setPixel(x, y, Color(col[0] * brightness, col[1] * brightness, col[2] * brightness))

            progress = float(current_track["progress_ms"])
            duration = current_track["item"]["duration_ms"]

            fraction = int((progress / duration) * 30)

            for x in range(32, 62):
              self.setPixel(x, 28, Color(0, 0, 0))

            for x in range(32, 32 + fraction):
              self.setPixel(x, 28, Color(255 * brightness, 255 * brightness, 255 * brightness)) 

        except Exception as e:
          print("Spotify Error")
          print(e)      
        
        color = self.calculateClockColour(Color(r, g, b))

        draw.clock(color, self)
        draw.clockDay(color, self)
        draw.clockDate(color, self)

      if self.update() == -1:
        return

      if globals.image == [] and not globals.strobe and not globals.rainbow:
       time.sleep(1)

def updateTime():
  #while True:
  print("Updating time...")
  os.system("sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\"")
  #  time.sleep(1)

def getHueColor():
  return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(float(globals.hueColourBulb.hue) / 65535, float(globals.hueColourBulb.saturation) / 255, float(globals.hueColourBulb.brightness) / 255))

def initHue():
  try:
    print("Connecting to Hue... ")
    bridge = Bridge('192.168.0.58')
    bridge.connect()
    bridge.get_api()
    lights = bridge.get_light_objects('list')

    globals.hueColourBulb = None
    globals.hueOnBulb = None

    for l in lights:
      if l.name == "Sams Room Light Left":
        globals.hueColourBulb = l
      elif l.name == "Lava Lamp":
        globals.hueOnBulb = l

    if globals.hueColourBulb == None:
      raise Exception("Could not find left light bulb")

    if globals.hueOnBulb == None:
      raise Exception("Could not find matrix bulb")

    globals.hueConnected = True
    print("Connected to Hue.")

  except Exception as e:
    globals.hueConnected = False
    print("Could not connect to Hue:\n" + str(e) + "\n")

if __name__ == '__main__':
  try:
   
    #timeSyncTimer = Thread(target=updateTime)
    #timeSyncTimer.start()
    #updateTime()

    initHue()

    webThread = Thread(target=run.start)
    webThread.daemon = True
    webThread.start()

    matrix = Matrix()

    matrix.start()

  except KeyboardInterrupt:
    sys.exit(0)
