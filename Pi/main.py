import socket
import struct

class Color:
  def __init__(self, a, r, g, b):
    self.a = a
    self.r = r
    self.g = g
    self.b = b

  def toString(self):
    return "(" + str(self.a) + ", " + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

class StatusPacket:
  def __init__(self, data):
    data = struct.unpack("iiiifff", data)
    self.color = Color(data[0],data[1],data[2],data[3])
    self.cpuUsage = round(data[4])
    self.ramUsage = round(data[5])
    self.gpuUsage = round(data[6])

  def toString(self):
    return self.color.toString() + " " + str(self.cpuUsage) + "% " + str(self.ramUsage) + "% " + str(self.gpuUsage) + "%"

UDP_IP = "127.0.0.1"
UDP_PORT = 2610

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  statusPacket = StatusPacket(data)
  print(statusPacket.toString())
