from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<marquee> <p>Hello, ITE</p> </marquee>'

@app.route('/jason')
def saluda():
    return data

@app.route('/json')
def saludajson():
    return jsonify(data)



