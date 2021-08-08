import requests
import wmi
import time
import sys

address = "http://192.168.0.30:5000"
urlbase = address + "/imagesubmit?imageData="

pixelCount = 32 * 64
cpuclockspeed = 0
cpuloads = []
cputemp = 0
cpuload = 0
gputemp = 0
ramuse = 0
gpuuse = 0
hdduses = []

w = wmi.WMI(namespace="root\OpenHardwareMonitor")

def getResourceValues():
    temperature_infos = w.Sensor()
    temperature_infos.sort(key=lambda x: x.Identifier, reverse=True)

    global cpuclockspeed
    global cpuloads
    global cputemp 
    global cpuload 
    global gputemp 
    global ramuse 
    global hdduses
    global gpuuse

    cpuloads = []
    hdduses = []

    for sensor in temperature_infos:
    
        if "/amdcpu/0/load/0" == sensor.Identifier:
            cpuload = sensor.Value

        elif "/amdcpu/0/load/" in sensor.Identifier:
            cpuloads.append(sensor.Value)

        elif "/amdcpu/0/clock" in sensor.Identifier:
            cpuclockspeed += sensor.Value

        elif "/amdcpu/0/temperature/0" == sensor.Identifier:
            cputemp = sensor.Value

        elif "/atigpu/0/temperature/9" == sensor.Identifier:
            gputemp = sensor.Value

        elif "/ram/load/0" == sensor.Identifier:
            ramuse = sensor.Value

        elif "/hdd/" in sensor.Identifier and "/load/0" in sensor.Identifier:
            hdduses.append(sensor.Value)
 
        elif "/atigpu/0/load/0" in sensor.Identifier:
            gpuuse = sensor.Value
        
    cpuclockspeed = cpuclockspeed / 6


def displaycpus(image):
    startx = 15
    starty = 1
    x = startx
    y = starty

    for cpu in cpuloads:
        cpuwidth = 13

        currentcpuload = cpu / 100
        currentcpuload = currentcpuload * cpuwidth
        currentcpuload = int(currentcpuload)     

        interval = 255 / cpuwidth
        r = 0
        g = 255

        while x < startx + currentcpuload:
            image[y][x] = "(" + str(r) + "," + str(g) + ",0)"
            r += interval
            g -= interval
            x += 1

        y += 2

        if y > 5:
            y = starty
            startx += 16
        
        x = startx

    return image

def display4bar(image, startx, starty, value, width):
    x = startx
    y = starty

    currentload = value / 100
    currentload = currentload * width
    currentload = int(currentload)

    interval = 255 / width
    r = 0
    g = 255

    while x < startx + currentload:
        image[y][x] = "(" + str(r) + "," + str(g) + ",0)"
        image[y+1][x] = "(" + str(r) + "," + str(g) + ",0)"
        image[y+2][x] = "(" + str(r) + "," + str(g) + ",0)"
        image[y+3][x] = "(" + str(r) + "," + str(g) + ",0)"
        r += interval
        g -= interval
        x += 1

    return image

def displayDisk(image, startx, starty, value, height):
    x = startx
    y = starty

    currentload = value / 100
    currentload = currentload * height
    currentload = int(currentload)

    interval = 255 / height
    r = 0
    g = 255

    while y > starty - currentload:
        image[y][x] = "(" + str(r) + "," + str(g) + ",0)"
        image[y][x+1] = "(" + str(r) + "," + str(g) + ",0)"
        image[y][x+2] = "(" + str(r) + "," + str(g) + ",0)"
        r += interval
        g -= interval
        y -= 1

    return image

bgcolour = "(0,0,0)"
fgcolour = "(255,255,255)"
mgcolour = "(32,32,32)"

matrix = [
         "                                                                ",
         "  11 111 1 1  10000000000000  10000000000000    000 000 000 000 ",
         " 1   1 1 1 1                                    000 000 000 000 ",
         " 1   111 1 1  10000000000000  10000000000000    000 000 000 000 ",
         "  11 1   111                                    000 000 000 000 ",
         "              10000000000000  10000000000000    000 000 000 000 ",
         "                                                000 000 000 000 ",
         " 111   111 111 111 1 1        111 111 111       000 000 000 000 ",
         "   1   1 1 1 1 1   1 1 111      1 1 1 1 1       000 000 000 000 ",
         "  11   111 111 1   111   1      1 1 1 111       000 000 000 000 ",
         "   1   1 1 1 1 1 1 1 1  1      1  1 1           000 000 000 000 ",
         " 111 1 111 111 111 1 1 111     1  111           000 000 000 000 ",
         "                                                000 000 000 000 ",
         " 100000000000000000000000000000000000000000000  000 000 000 000 ",
         " 100000000000000000000000000000000000000000000  000 000 000 000 ",
         " 100000000000000000000000000000000000000000000  000 000 000 000 ",
         " 100000000000000000000000000000000000000000000  000 000 000 000 ",
         "                                                000 000 000 000 ",
         "                                                000 000 000 000 ",
         "                                                000 000 000 000 ",
         "                                                000 000 000 000 ",
         " 111 111 1 1  111 111 111   111 111 1   1       000 000 000 000 ",
         " 1   1 1 1 1  1 1 1 1 1 1   1 1 1 1 11 11       000 000 000 000 ",
         " 1 1 111 1 1  111 111 111   11  111 1 1 1       000 000 000 000 ",
         " 111 1   111  1 1 1 1       1 1 1 1 1 1 1       111 111 111 111 ",
         "              111 111                                           ",
         "                                                 11 11  111 111 ",
         " 100000000000000000000000   100000000000000000  1   1 1 1   1   ",
         " 100000000000000000000000   100000000000000000  1   1 1 111 1   ",
         " 100000000000000000000000   100000000000000000  1   1 1 1   1 1 ",
         " 100000000000000000000000   100000000000000000   11 11  111 111 ",
         "                                                                "]

try:
    while True:
        getResourceValues()

        image = []

        for row in matrix:
            newRow = []

            for pixel in row:
                if pixel == " ":
                    newRow.append(bgcolour)
                elif pixel == "1":
                    newRow.append(fgcolour)
                elif pixel == "0":
                    newRow.append(mgcolour)

            image.append(newRow)

        image = displaycpus(image)
        image = display4bar(image, 2, 13, cpuload, 44)
        image = display4bar(image, 2, 27, gpuuse, 24)
        image = display4bar(image, 29, 27, ramuse, 17)

        image = displayDisk(image, 48, 23, hdduses[2], 22)
        image = displayDisk(image, 52, 23, hdduses[3], 22)
        image = displayDisk(image, 56, 23, hdduses[1], 22)
        image = displayDisk(image, 60, 23, hdduses[0], 22)

        strImage = ""

        for row in image:
            for pixel in row:
                strImage += pixel + ","

        requests.post(urlbase + strImage[:-1])
        time.sleep(5)

except KeyboardInterrupt:
    requests.post(address + "/reset")
    sys.exit(0)