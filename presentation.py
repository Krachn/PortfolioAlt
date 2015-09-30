#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import data
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)



@app.route('/')
def main_page():
	db = data.load("data.json")
	example_project = data.search(db)[0]
	return render_template('main.html', project_data = example_project)

@app.route('/list', methods=['POST','GET'])
def list_page():
	db = data.load("data.json")
	full_list = data.search(db)
	techniques = data.get_technique_stats(db)
	if request.method == 'POST':

		technique_list = request.form.getlist('technique')
		order = request.form['sort_order']
		free_text_search = request.form['free_text_search']
		if free_text_search == '':
			free_text_search = None
		search_results = data.search(full_list, techniques=technique_list,
												sort_order=order,
												search = free_text_search)

		return render_template('list.html', project_list=search_results, techniques = techniques.keys()) 


	else:
		return render_template('list.html', project_list = full_list, techniques = techniques.keys())

@app.route('/techniques')
def technique_page():
	db = data.load("data.json")
	result_dict = data.get_technique_stats(db)
	return render_template('techniques.html', techniques = result_dict)

if __name__ == '__main__':
    app.run(debug=True)

