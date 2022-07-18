from flask import render_template, json, request, redirect, url_for
from app import app
import globals

import random

@app.route('/', methods=['GET', 'POST'])
def index():

    dayHexColour = '#%02x%02x%02x' % (int(globals.r), int(globals.g), int(globals.b))
    nightHexColour = '#%02x%02x%02x' % (int(globals.nightr), int(globals.nightg), int(globals.nightb))

    checked = ""
    if globals.useTimeBrightness:
        useTimeBrightness = "checked"

    return render_template('index.html', title='Home', dayHexColour=dayHexColour, nightHexColour=nightHexColour, brightness=globals.brightness, nightBrightness=globals.nightBrightness, useTimeBrightness=useTimeBrightness)

@app.route('/daysubmit', methods=['POST'])
def daySubmit():
    data = json.loads(request.data)
    rgb = data.get('rgb')
    rgb = rgb[4:len(rgb)-1]
    rgb = rgb.split(",")
    
    globals.r = int(rgb[0])
    globals.g = int(rgb[1])
    globals.b = int(rgb[2])
    
    globals.brightness = data.get('brightness')

    with open("./data/clockcolour", "w") as file:
        file.write(globals.r + "," + globals.g + "," + globals.b)

    return json.dumps({'status':'Success'})

@app.route('/nightsubmit', methods=['POST'])
def nightSubmit():
    data = json.loads(request.data)
    rgb = data.get('rgb')
    rgb = rgb[4:len(rgb)-1]
    rgb = rgb.split(",")
    
    globals.nightr = rgb[0]
    globals.nightg = rgb[1]
    globals.nightb = rgb[2]
    
    globals.nightBrightness = data.get('brightness')
    globals.useTimeBrightness = data.get('useNightBrightness')

    with open("./data/nightclockcolour", "w") as file:
        file.write(globals.r + "," + globals.g + "," + globals.b)

    return json.dumps({'status':'Success'})


@app.route('/imagesubmit', methods=['GET', 'POST'])
def imageSubmit():
    imageData = list(eval(request.args.get("imageData")))

    globals.image = imageData

    return redirect(url_for('index'))

@app.route('/reset', methods=['GET', 'POST'])
def reset():

    globals.image = []

    return redirect(url_for('index'))

@app.route('/togglestrobe', methods=['POST'])
def togglestrobe():

    globals.strobe = not globals.strobe

    return json.dumps({'status':'Success'})

@app.route('/togglerainbow', methods=['POST'])
def togglerainbow():

    globals.rainbow = not globals.rainbow

    return json.dumps({'status':'Success'})

@app.route('/togglehue', methods=['POST'])
def togglehue():

    globals.useHue = not globals.useHue

    return json.dumps({'status':'Success'})


