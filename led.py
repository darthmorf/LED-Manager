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
import globals
import os
import colorsys

class Color:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b

  def toString(self):
    return "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

  def toRGB(self):
    return (self.r, self.g, self.b)

class Matrix:
  def __init__(self):
    self.width = 64
    self.height = 32
    defaultColor = Color(0,0,0)
    self.values = []

    if platform.system() == "Windows":
      self.debug = True
    else:
      self.debug = False

    for y in range(self.height):
      row = []
      for x in range(self.width):
        row.append(defaultColor)
      self.values.append(row)

    if self.debug:
      import pygame
      self.pygame = pygame
      self.pygame.init()
      self.pixelModifier = 8
      self.surface = pygame.display.set_mode((self.width*self.pixelModifier + self.width, self.height*self.pixelModifier + self.height))
      self.pygame.display.set_caption("LED Matrix Simulator")
    else:
      from rgbmatrix import RGBMatrix, RGBMatrixOptions
      options = RGBMatrixOptions()
      options.rows = self.height
      options.cols = self.width
      options.hardware_mapping = 'adafruit-hat-pwm'

      self.matrix = RGBMatrix(options = options)
      self.canvas = self.matrix.CreateFrameCanvas()

  def calculateBrightness(self):

    try:
      proc = subprocess.Popen("gpio -g mode 2 out; gpio -g mode 19 in; gpio -g write 2 1; gpio -g read 19", shell=True, stdout=subprocess.PIPE)
      switch = int(proc.stdout.read())
    except LookupError:
      print("Reading switch GPIO failed! Defaulting to On. This probably means that the SD card has slipped out D:")
      switch = 1

    if switch == 0:
      globals.brightness = 0

    elif globals.strobe or (globals.useHue and globals.hueConnected):
      globals.brightness = 1

    elif globals.useTimeBrightness:   
      
      hour = datetime.datetime.now().hour

      if hour > 21 or hour < 7:
        globals.brightness = 0.02
      elif hour > 20 or hour < 8:
        globals.brightness = 0.25
      elif hour > 17 or hour < 9:
        globals.brightness = 0.5

    

  def update(self):

    if self.debug:
      for event in self.pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == self.pygame.QUIT:
            return -1

      self.surface.fill((0,0,0))

      x = 0
      y = 0

      for i in range(self.height):
        for j in range(self.width):
          rgb = self.values[i][j].toRGB()
          rgb = (rgb[0] * globals.brightness, rgb[1] * globals.brightness, rgb[2] * globals.brightness)
          self.pygame.draw.rect(self.surface, rgb, self.pygame.Rect(x, y, self.pixelModifier, self.pixelModifier))
          x += self.pixelModifier + 1
        x = 0
        y += self.pixelModifier + 1
      
      self.pygame.display.flip()

    else:
      self.calculateBrightness()
      self.canvas.Clear()
      for i in range(self.height):
        for j in range(self.width):
          if self.values[i][j].toRGB() != (0,0,0):
            self.canvas.SetPixel(j, i, self.values[i][j].r * globals.brightness, self.values[i][j].g * globals.brightness, self.values[i][j].b * globals.brightness)

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
        self.setBG(Color(r, g, b))
        self.update()
        self.setBG(Color(0, 0, 0))
        self.update()

      else:
        color = Color(r, g, b)

        self.clear()

        draw.clock(color, self)
        daywidth = draw.clockDay(color, self)
        draw.clockDate(color, self, daywidth)

      if self.update() == -1:
        return

      if not self.debug and globals.image == [] and not globals.strobe:
        time.sleep(5)

def updateTime():
  #while True:
  print("Updating time...")
  os.system("sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\"")
  #  time.sleep(1)

def getHueColor():
  return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(float(globals.hueBulb.hue) / 65535, float(globals.hueBulb.saturation) / 255, float(globals.hueBulb.brightness) / 255))

def initHue():
  try:
    print("Connecting to Hue... ")
    bridge = Bridge('192.168.0.52')
    bridge.connect()
    bridge.get_api()
    lights = bridge.get_light_objects('id')

    globals.hueBulb = lights[1]
    globals.hueConnected = True
    print("Connected to Hue.")

  except:
    globals.hueConnected = False
    print("Could not connect to Hue.")

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
