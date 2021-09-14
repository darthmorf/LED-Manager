from flask import render_template, json, request, redirect, url_for
from app import app
import globals

import random

@app.route('/', methods=['GET', 'POST'])
def index():

    hexColour = '#%02x%02x%02x' % (int(globals.r), int(globals.g), int(globals.b))

    checked = ""
    if globals.useTimeBrightness:
        checked = "checked"

    return render_template('index.html', title='Home', hexColour=hexColour, brightness=globals.brightness, checked=checked)

@app.route('/coloursubmit', methods=['POST'])
def colourSubmit():
    data = json.loads(request.data)
    rgb = data.get('rgb')
    rgb = rgb[4:len(rgb)-1]
    rgb = rgb.split(",")
    
    globals.r = rgb[0]
    globals.g = rgb[1]
    globals.b = rgb[2]

    with open("./data/clockcolour", "w") as file:
        file.write(globals.r + "," + globals.g + "," + globals.b)

    return json.dumps({'status':'Success'})

@app.route('/brightnesssubmit', methods=['POST'])
def brightnesssubmit():
    data = json.loads(request.data)
    globals.brightness = data.get('brightness')
    globals.useTimeBrightness = data.get('useTimeBrightness')

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

@app.route('/togglehue', methods=['POST'])
def togglehue():

    globals.useHue = not globals.useHue

    return json.dumps({'status':'Success'})


