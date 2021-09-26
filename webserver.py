from flask import Flask, render_template
from flask_pymongo import PyMongo

import json

app = Flask(__name__, static_folder='static')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/link')
def link():
    return render_template('views/link.html')


if __name__ == "__main__":
    app.run(debug=True)