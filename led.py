#!/usr/bin/env python

from threading import Thread
import subprocess
import draw
import time
import sys
import platform
import run
import datetime
import globals
import os

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
          self.pygame.draw.rect(self.surface, self.values[i][j].toRGB(), self.pygame.Rect(x, y, self.pixelModifier, self.pixelModifier))
          x += self.pixelModifier + 1
        x = 0
        y += self.pixelModifier + 1
      
      self.pygame.display.flip()

    else:
      self.canvas.Clear()
      for i in range(self.height):
        for j in range(self.width):
          if self.values[i][j].toRGB() != (0,0,0):
            self.canvas.SetPixel(j, i, self.values[i][j].r, self.values[i][j].g, self.values[i][j].b)

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

    print("Running LED Manager. Pres Ctrl+C to quit.")

    with open("./data/clockcolour", "r") as file:
      rgbStr = file.read()
      rgbStr = rgbStr.split(",")

      globals.r = rgbStr[0]
      globals.g = rgbStr[1]
      globals.b = rgbStr[2]
    
    storedBrightness = 1

    while True:
      r = int(globals.r)
      g = int(globals.g)
      b = int(globals.b)

      brightness = storedBrightness

      hour = datetime.datetime.now().hour

      if not self.debug:
        try:
          proc = subprocess.Popen("gpio -g mode 2 out; gpio -g mode 19 in; gpio -g write 2 1; gpio -g read 19", shell=True, stdout=subprocess.PIPE)
          switch = int(proc.stdout.read())
        except LookupError:
          print("Reading switch GPIO failed! Defaulting to On. This probably means that the SD card has slipped out D:")
          switch = 1

        if switch == 0:
          brightness = 0
        else:
          brightness = storedBrightness

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

      else:
        timeBrightness = 1

        if hour > 20 or hour < 8:
          timeBrightness = 0.25
        elif hour > 17 or hour < 9:
          timeBrightness = 0.5

        brightness = float(timeBrightness * brightness)
        color = Color(r * brightness, g * brightness, b * brightness)

        self.clear()

        draw.clock(color, self)
        daywidth = draw.clockDay(color, self)
        draw.clockDate(color, self, daywidth)

      if self.update() == -1:
        return

      if not self.debug:
        time.sleep(5)

if __name__ == '__main__':
  try:
   # print("Updating time...")
   # os.system("sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\"")

    webThread = Thread(target=run.start)
    webThread.daemon = True
    webThread.start()

    matrix = Matrix()
    matrix.start()
    
  except KeyboardInterrupt:
    sys.exit(0)

  
    
   
  
  
