#!/usr/bin/env python

from threading import Thread
import time
import sys

DEBUG = True

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
      options.parallel = 1
      options.hardware_mapping = 'adafruit-hat'

      self.matrix = RGBMatrix(options = options)
      self.canvas = self.matrix.CreateFrameCanvas()

  def update(self):
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

  def drawClock(self, color):
    self.drawClockDigit(0,0, color)
    self.drawClockDigit(1,0, color)
    self.drawClockDigit(2,0, color)
    self.drawClockDigit(3,0, color)

    self.setPixel(31, 6, color)
    self.setPixel(32, 6, color)
    self.setPixel(31, 7, color)
    self.setPixel(32, 7, color)
    self.setPixel(31, 8, color)
    self.setPixel(32, 8, color)

    self.setPixel(31, 15, color)
    self.setPixel(32, 15, color)
    self.setPixel(31, 16, color)
    self.setPixel(32, 16, color)
    self.setPixel(31, 17, color)
    self.setPixel(32, 17, color)


  def drawClockDigit(self, index, value, color):
    x = 0
    y = 3

    if index == 0:
      x = 3
    elif index == 1:
      x = 3 + 10 + 4
    elif index == 2:
      x = 3 + 10 + 4 + 10 + 10
    else:
      x = 3 + 10 + 4 + 10 + 10 + 10 + 4

    if value == 0:
      #row 0
      self.setPixel(x+2, y, color)
      self.setPixel(x+3, y, color)
      self.setPixel(x+4, y, color)
      self.setPixel(x+5, y, color)
      self.setPixel(x+6, y, color)
      self.setPixel(x+7, y, color)
      #row 1
      self.setPixel(x+1, y+1, color)
      self.setPixel(x+2, y+1, color)
      self.setPixel(x+3, y+1, color)
      self.setPixel(x+4, y+1, color)
      self.setPixel(x+5, y+1, color)
      self.setPixel(x+6, y+1, color)
      self.setPixel(x+7, y+1, color)
      self.setPixel(x+8, y+1, color)
      #row 2
      self.setPixel(x,   y+2, color)
      self.setPixel(x+1, y+2, color)
      self.setPixel(x+2, y+2, color)
      self.setPixel(x+6, y+2, color)
      self.setPixel(x+7, y+2, color)
      self.setPixel(x+8, y+2, color)
      self.setPixel(x+9, y+2, color)
      #row 3
      self.setPixel(x,   y+3, color)
      self.setPixel(x+1, y+3, color)
      self.setPixel(x+6, y+3, color)
      self.setPixel(x+7, y+3, color)
      self.setPixel(x+8, y+3, color)
      self.setPixel(x+9, y+3, color)
      #row 4
      self.setPixel(x,   y+4, color)
      self.setPixel(x+1, y+4, color)
      self.setPixel(x+5, y+4, color)
      self.setPixel(x+6, y+4, color)
      self.setPixel(x+7, y+4, color)
      self.setPixel(x+8, y+4, color)
      self.setPixel(x+9, y+4, color)
      #row 5
      self.setPixel(x,   y+5, color)
      self.setPixel(x+1, y+5, color)
      self.setPixel(x+5, y+5, color)
      self.setPixel(x+6, y+5, color)
      self.setPixel(x+8, y+5, color)
      self.setPixel(x+9, y+5, color)
      #row 6
      self.setPixel(x,   y+6, color)
      self.setPixel(x+1, y+6, color)
      self.setPixel(x+5, y+6, color)
      self.setPixel(x+6, y+6, color)
      self.setPixel(x+8, y+6, color)
      self.setPixel(x+9, y+6, color)
      #row 7
      self.setPixel(x,   y+7, color)
      self.setPixel(x+1, y+7, color)
      self.setPixel(x+4, y+7, color)
      self.setPixel(x+5, y+7, color)
      self.setPixel(x+6, y+7, color)
      self.setPixel(x+8, y+7, color)
      self.setPixel(x+9, y+7, color)
      #row 8
      self.setPixel(x,   y+8, color)
      self.setPixel(x+1, y+8, color)
      self.setPixel(x+4, y+8, color)
      self.setPixel(x+5, y+8, color)
      self.setPixel(x+8, y+8, color)
      self.setPixel(x+9, y+8, color)
      #row 9
      self.setPixel(x,   y+9, color)
      self.setPixel(x+1, y+9, color)
      self.setPixel(x+4, y+9, color)
      self.setPixel(x+5, y+9, color)
      self.setPixel(x+8, y+9, color)
      self.setPixel(x+9, y+9, color)
      #row 10
      self.setPixel(x,   y+10, color)
      self.setPixel(x+1, y+10, color)
      self.setPixel(x+3, y+10, color)
      self.setPixel(x+4, y+10, color)
      self.setPixel(x+5, y+10, color)
      self.setPixel(x+8, y+10, color)
      self.setPixel(x+9, y+10, color)
      #row 11
      self.setPixel(x,   y+11, color)
      self.setPixel(x+1, y+11, color)
      self.setPixel(x+3, y+11, color)
      self.setPixel(x+4, y+11, color)
      self.setPixel(x+8, y+11, color)
      self.setPixel(x+9, y+11, color)
      #row 12
      self.setPixel(x,   y+12, color)
      self.setPixel(x+1, y+12, color)
      self.setPixel(x+3, y+12, color)
      self.setPixel(x+4, y+12, color)
      self.setPixel(x+8, y+12, color)
      self.setPixel(x+9, y+12, color)
      #row 13
      self.setPixel(x,   y+13, color)
      self.setPixel(x+1, y+13, color)
      self.setPixel(x+2, y+13, color)
      self.setPixel(x+3, y+13, color)
      self.setPixel(x+4, y+13, color)
      self.setPixel(x+8, y+13, color)
      self.setPixel(x+9, y+13, color)
      #row 14
      self.setPixel(x,   y+14, color)
      self.setPixel(x+1, y+14, color)
      self.setPixel(x+2, y+14, color)
      self.setPixel(x+3, y+14, color)
      self.setPixel(x+8, y+14, color)
      self.setPixel(x+9, y+14, color)
      #row 15
      self.setPixel(x,   y+15, color)
      self.setPixel(x+1, y+15, color)
      self.setPixel(x+2, y+15, color)
      self.setPixel(x+3, y+15, color)
      self.setPixel(x+8, y+15, color)
      self.setPixel(x+9, y+15, color)
      #row 16
      self.setPixel(x+1, y+16, color)
      self.setPixel(x+2, y+16, color)
      self.setPixel(x+3, y+16, color)
      self.setPixel(x+4, y+16, color)
      self.setPixel(x+5, y+16, color)
      self.setPixel(x+6, y+16, color)
      self.setPixel(x+7, y+16, color)
      self.setPixel(x+8, y+16, color)
      #row 17
      self.setPixel(x+2, y+17, color)
      self.setPixel(x+3, y+17, color)
      self.setPixel(x+4, y+17, color)
      self.setPixel(x+5, y+17, color)
      self.setPixel(x+6, y+17, color)
      self.setPixel(x+7, y+17, color)





def __main__():

  grid = Grid(DEBUG)

  try:
    print("Running LED Manager. Pres Ctrl+C to quit.")

    x = 0
    y = 0
    while True:

      grid.clear()

      grid.drawClock(Color(255,255,255))
      #grid.setPixel(x, y, Color(255,255,255))
      #x += 1
      #if x == grid.width:
      #  y += 1
      #x = x % grid.width
      #y = y % grid.height

      grid.update()
      time.sleep(1/120)

  except KeyboardInterrupt:
    sys.exit(0)


__main__()
 
