import socket
import struct
import pygame

class Color:
  def __init__(self, a, r, g, b):
    self.a = a
    self.r = r
    self.g = g
    self.b = b

  def toString(self):
    return "(" + str(self.a) + ", " + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

  def toRGB(self):
    return (self.r,self.g,self.b)



class ImageStatusPacket:
  def __init__(self, data):
    data = struct.unpack("fff", data)
    self.cpuUsage = round(data[0])
    self.ramUsage = round(data[1])
    self.gpuUsage = round(data[2])
    self.imageData = data[3]

  def toString(self):
    return "ImageStatus: " + str(self.cpuUsage) + "% " + str(self.ramUsage) + "% " + str(self.gpuUsage) + "%"


class StatusPacket:
  def __init__(self, data):
    data = struct.unpack("iiiifff", data)
    self.color = Color(data[0],data[1],data[2],data[3])
    self.cpuUsage = round(data[4])
    self.ramUsage = round(data[5])
    self.gpuUsage = round(data[6])

  def toString(self):
    return "Status: " + self.color.toString() + " " + str(self.cpuUsage) + "% " + str(self.ramUsage) + "% " + str(self.gpuUsage) + "%"



class Grid:
  def __init__(self):
    self.width = 32
    self.height = 32
    defaultColor = Color(255,255,255,255)
    self.contents = []
    self.barHeight = 22;
    self.cpuHistory = []
    self.ramHistory = []
    self.gpuHistory = []

    for x in range(self.width):
      row = []
      for y in range(self.height):
        row.append(defaultColor)
      self.contents.append(row)

  def setBG(self, color):
    for i in range(len(self.contents)):
      for j in range(len(self.contents[i])):
        self.contents[i][j] = color

  def drawOutlines(self):
    for x in range(len(self.contents)):
      for y in range(len(self.contents[x])):
        shouldSet = False
        if y == 4 or y == 27:
          if (x > 3 and x < 10) or (x > 12 and x < 19) or (x > 21 and x < 28):
            shouldSet = True
        elif y > 4 and y < 27:
          if x == 4 or x == 9 or x == 13 or x == 18 or x == 22 or x == 27:
            shouldSet = True

        if shouldSet:
           self.contents[y][x] = Color(255, 255, 255, 255)

  def drawBars(self, cpuValue, ramValue, gpuValue):
    self.drawBar(cpuValue, self.cpuHistory, 5)
    self.drawBar(ramValue, self.ramHistory, 14)
    self.drawBar(gpuValue, self.gpuHistory, 23)

  def drawBar(self, value, history, xStart):
    history.append(value)
    if len(history) > 4:
      del history[0]

    i = 0
    value = 0
    for value_ in history:
      value += value_
      i += 1

    value = int(value/i)

    yValue = int((value / 100) * self.barHeight)

    if yValue < 1:
      yValue = 1

    for i in range(yValue):
      for j in range(4):
        colorValue = int((i / self.barHeight) * 255)
        self.contents[26-i][xStart+j] = Color(255, colorValue, 255-colorValue, 0)

  def drawOutline(self, color):
    for x in range(len(self.contents)):
      for y in range(len(self.contents[x])):
        if y == 0 or y == 1 or y == 30 or y == 31 or x == 0 or x == 1 or x == 30 or x == 31:
          self.contents[y][x] = color


class GridDisplay:
  def __init__(self, grid):
    self.grid = grid
    pygame.init()
    self.pixelModifier = 8
    self.surface = pygame.display.set_mode((grid.width*self.pixelModifier + grid.width, grid.height*self.pixelModifier + grid.height))
    pygame.display.set_caption("LED Matrix Simulator")

  def update(self):
    pygame.event.get()
    self.surface.fill((100,0,100))
    x = 0
    y = 0

    for i in range(len(self.grid.contents)):
      for j in range(len(self.grid.contents[i])):
        pygame.draw.rect(self.surface, self.grid.contents[i][j].toRGB(), pygame.Rect(x, y, self.pixelModifier, self.pixelModifier))
        x += self.pixelModifier + 1
      x = 0
      y += self.pixelModifier + 1
    
    pygame.display.flip()



def __main__():
  UDP_IP = "127.0.0.1"
  UDP_PORT = 2610

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
  sock.bind((UDP_IP, UDP_PORT))

  grid = Grid()
  gridDisplay = GridDisplay(grid)

 

  while True:
    packetType, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    packetData, addr = sock.recvfrom(1024)
    packetType = packetType.decode("ASCII")
    
    if packetType == "Status":
      packet = StatusPacket(packetData)
      print(packet.toString())
      grid.setBG(Color(255, 0, 0, 0))
      grid.drawOutlines()
      grid.drawBars(packet.cpuUsage, packet.ramUsage, packet.gpuUsage)
      grid.drawOutline(packet.color)
      gridDisplay.update()

    elif packetType == "ImageStatus":
      packet = ImageStatusPacket(packetData)
      print(packet.toString())
      grid.setBG(Color(255, 0, 0, 0))
      grid.drawOutlines()
      grid.drawBars(packet.cpuUsage, packet.ramUsage, packet.gpuUsage)
      gridDisplay.update()
    
   

    




__main__()
