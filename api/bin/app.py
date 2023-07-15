from flask import Flask
import logging
from model import DbModel

logging.basicConfig(level=logging.INFO)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
neo = DbModel()

@app.route('/')
def smoke_test():
    cipher = 'UNWIND range(1, 3) AS n RETURN n, n * n as n_sq'
    d = neo.connect().run(cipher).data()
    return {'results': d}

@app.route('/dog')
def get_all():
    return neo.get_all()

@app.route('/dog/name/<name>')
def filter_by_name(name: str):
    return neo.filter_by_name(name)

@app.route('/dog/breed/<breed>')
def filter_by_breed(breed: str):
    return neo.filter_by_breed(breed)

@app.route('/dog/color/<color>')
def filter_by_color(color: str):
    return neo.filter_by_color(color)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)
