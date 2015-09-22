#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import data
from flask import Flask
from flask import render_template


app = Flask(__name__)



@app.route('/')
def main_page():
	db = data.load("data.json")
	example_project = data.search(db)[0]
	return render_template('main.html', project_data = example_project)

@app.route('/list')
def list_page():
	db = data.load("data.json")
	result_list = data.search(db)
	return render_template('list.html', project_list = result_list)

if __name__ == '__main__':
    app.run(debug=True)

