from flask import render_template, json, request
from app import app
import globals

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html', title='Home')

@app.route('/coloursubmit', methods=['POST'])
def registerSubmit():
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



