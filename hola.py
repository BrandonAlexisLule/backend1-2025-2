from flask import Flask, render_template
from flask import Flask, jsonify
app = Flask(__name__)

#python dictionary
data = {
    "name":"Alice",
    "age":"30",
    "city":"New York",
    "is_student": False,
    "hobbies":["reading", "coding"]
}

#ejecutar código html con render_templates


@app.route('/')
def hello_world():
    return '<marquee> <p>Hello, ITE</p> </marquee>'

@app.route('/jason')
def saluda():
    return data

@app.route('/json')
def saludajson():
    return jsonify(data)

@app.route('/pagina')
@app.route('/pagina<name>')
def pagina(name = None):
    return render_template('pagina.html', person=name)

if __name__=='__main__':
    app.run()





