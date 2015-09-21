#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html', heading = "Projektnamn", long_text = "Lorem ipsum text text text osv osv you get the point")

if __name__ == '__main__':
    app.run(debug=True)

