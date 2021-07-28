#!/usr/bin/env python

from threading import Thread
import draw
import time
import sys

DEBUG = False

class Color:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b

  def toString(self):
    return "(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

  def toRGB(self):
    return (self.r, self.g, self.b)

class Grid:
  def __init__(self, debug=False):
    self.debug = debug
    self.width = 64
    self.height = 32
    defaultColor = Color(0,0,0)
    self.values = []
    self.oldvalues = []

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
      options.brightness = 5
      options.hardware_mapping = 'adafruit-hat'

      self.matrix = RGBMatrix(options = options)
      self.canvas = self.matrix.CreateFrameCanvas()

  def update(self):
    if self.values == self.oldvalues:
      return
    
    self.oldvalues = self.values

    if self.debug:
      self.pygame.event.get()
      self.surface.fill((0,0,0))
      #self.surface.fill((255,0,255))
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



def __main__():

  grid = Grid(DEBUG)

  try:
    print("Running LED Manager. Pres Ctrl+C to quit.")

    x = 0
    y = 0

    r = 255
    g = 255
    b = 255

    brightness = 1

    i = 1
    while True:

      grid.clear()
      step = 15
      if r == 255 and b < 255 and g ==0:
        b += step
      elif b == 255 and g == 0 and r <= 255 and r > 0:
        r -= step
      elif r == 0 and b == 255 and g < 255:
        g += step
      elif r == 0 and g == 255 and b <= 255 and b > 0:
        b -= step
      elif b == 0 and r < 255 and g == 255:
        r += step
      elif b == 0 and r == 255 and g <= 255 and g > 0:
        g -= step

      #color = Color(r,g,b)
      color = Color(255*brightness,255*brightness,255*brightness)
      draw.clock(color, grid)
      daywidth = draw.clockDay(color, grid)
  
      draw.clockDate(color, grid, daywidth)
      #grid.setPixel(x, y, Color(255,255,255))
      #x += 1
      #if x == grid.width:
      #  y += 1
      #x = x % grid.width
      #y = y % grid.height

      grid.update()
      time.sleep(1/1)

  except KeyboardInterrupt:
    sys.exit(0)


__main__()
 
