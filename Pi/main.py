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

  def setBG(self, color):
    for y in range(self.height):
      for x in range(self.width):
        self.values[y][x] = color

  def setPixel(self, x, y, color):
    if x > self.width:
      print(x + " is out of bounds.")
      return
    if y > self.height:
      print(y + " is out of bounds.")
      return

    self.values[y][x] = color

  def update(self):
    if self.debug:
      self.pygame.event.get()
      self.surface.fill((255,0,255))
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
          self.canvas.SetPixel(j, i, self.values[i][j].r, self.values[i][j].g, self.values[i][j].b)

      self.canvas = self.matrix.SwapOnVSync(self.canvas)


def __main__():

  grid = Grid(True)
  grid.setBG(Color(0,0,255))
  grid.setPixel(10, 10, Color(255,0,0))

  while True:
    grid.update()

__main__()
 
