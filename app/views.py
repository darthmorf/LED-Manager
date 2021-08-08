from flask import render_template, json, request, redirect, url_for
from app import app
import globals

import random

@app.route('/', methods=['GET', 'POST'])
def index():

    hexColour = '#%02x%02x%02x' % (int(globals.r), int(globals.g), int(globals.b))

    return render_template('index.html', title='Home', hexColour=hexColour)

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


@app.route('/imagesubmit', methods=['GET', 'POST'])
def imageSubmit():
    imageData = list(eval(request.args.get("imageData")))

    globals.image = imageData

    return redirect(url_for('index'))

@app.route('/reset', methods=['GET', 'POST'])
def reset():

    globals.image = []

    return redirect(url_for('index'))

