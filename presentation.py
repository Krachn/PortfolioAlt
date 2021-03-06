#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import data
import logging
from logging import FileHandler
from flask import Flask
from flask import render_template
from flask import request
from random import choice
from collections import OrderedDict

from pprint import pprint

app = Flask(__name__)

log_file = "server.log"
sortable_fields = {'start_date':'Starting date',
                   'end_date':'End date',
                   'project_name':'Project name',
                   'project_no':'Project ID'}

searchable_fields = {'short_description':'Short description',
                    'course_name':'Course name',
                    'long_description':"Long description",
                    'group_size': "Group size",
                    'academic_credits' : "Academic credits",
                    'techniques_used':"Techniques used",
                    'project_name':'Project name',
                    'course_id':"Course ID"}


@app.before_request
def request_logging():
    """
    This function logs each request the server gets.

    This function is called before each request is handled.
    """
    app.logger.info("Request: " + str(request) + " Form data: " + str(
        dict((key, request.form.getlist(key)) for key in request.form.keys())))


@app.errorhandler(500)
def internal_error(e):
    """
    Using the data layer, Jinja2, and the 500.html template this function
    returns a basic page informing the user that a 500 error occurred.

    It also adds a lot of useful information to the log to help with debugging.

    This function is called when there is an internal server error(400).

    :return: A basic 500 information page.
    """
    app.logger.error(
        """
Request:   {method} {path}
IP:        {ip}
Agent:     {agent_platform} | {agent_browser} {agent_browser_version}
Raw Agent: {agent}
Form Data: {form_data}
        """.format(method=request.method,
                   path=request.path,
                   ip=request.remote_addr,
                   agent_platform=request.user_agent.platform,
                   agent_browser=request.user_agent.browser,
                   agent_browser_version=request.user_agent.version,
                   agent=request.user_agent.string,
                   form_data=str(dict((key, request.form.getlist(key)) for key in request.form.keys()))
                   )
    )
    return render_template('status_codes/500.html', page_name='Error Page')


@app.route('/')
def main_page():
    """
    Using the data layer, Jinja2, and the start.html template this function
    returns the main page of the portfolio to whoever sent the request.

    This function is called when the URL '/' is requested.

    :return: The main page HTML of our portfolio.
    """
    db = data.load("data.json")
    example_project = choice(data.search(db))
    return render_template('start.html', page_name='Homepage',
                           project_data=example_project, stylesheets=['full-project.css', 'start.css'])


@app.route('/project/<int:id>')
def project_page(id):
    """
    Using the data layer, Jinja2, and the project.html template this function
    returns a page containing information regarding the project that in the 
    database has the specified id. If the specified project does not exist, it
    returns the "404" page.

    This function is called when the URL '/project/<int:id>' is requested.

    :return: The specified projects page
    """
    db = data.load('data.json')
    project = data.get_project(db, id)
    pprint(project)
    if project is not None:
        return render_template('elements/project.html', page_name='Project', project_data=project,
                               stylesheets=['full-project.css'])
    else:
        return render_template('status_codes/404.html', page_name='Project', non_existent_url=request.path,
                               stylesheets=['status_codes/404.css'])


@app.route('/list', methods=['POST', 'GET'])
def list_page():
    """
    Using the data layer, Jinja2, and the list.html template this function
    EITHER returns the default list page (containing all the projects) OR
    if it has been requested using a POST it instead returns the list page
    containing a list of projects that fit the search parameters contained
    in the POST.

    This function is called when the URL '/list' is requested.

    :return: The list page of our portfolio(containing all or some projects from
            the data layer).
    """
    db = data.load("data.json")
    full_list = data.search(db)
    techniques = data.get_technique_stats(db)

    if request.method == 'POST':
        requested_technique_list = request.form.getlist('technique')
        requested_search_fields_list = request.form.getlist('search_fields')
        if not requested_search_fields_list: requested_search_fields_list = None
        requested_order = request.form['sort_order']
        requested_sort_field = request.form['sort_field']
        requested_text_search = request.form['text_search']
        if requested_text_search == '':
            requested_text_search = None
        search_results = data.search(full_list, techniques=requested_technique_list,
                                     search_fields = requested_search_fields_list,
                                     sort_order=requested_order,
                                     sort_by=requested_sort_field,
                                     search=requested_text_search)

        return render_template('list.html', page_name='List Page',
                               sortable_fields=sortable_fields,
                               searchable_fields=searchable_fields,
                               project_list=search_results,
                               previous_search_fields=requested_search_fields_list or [],
                               previous_text_search=requested_text_search or '',
                               previous_techniques=requested_technique_list,
                               previous_sort_field=requested_sort_field,
                               techniques=sorted(techniques.keys()),
                               stylesheets=['list.css', 'project-item.css', 'search-box.css'])

    else:
        return render_template('list.html', page_name='List Page',
                               sortable_fields=sortable_fields,
                               searchable_fields=searchable_fields or [],  
                               project_list=full_list,
                               techniques=sorted(techniques.keys()),
                               stylesheets=['list.css', 'project-item.css', 'search-box.css'])


@app.route('/techniques')
def technique_page():
    """
    Using the data layer, Jinja2, and the techniques.html template this function
    returns the techniques page of the portfolio populated with all the techniques
    found in our data layer to whoever sent the request.

    This function is called when the URL '/techniques' is requested.

    :return: The techniques page of our portfolio.
    """
    db = data.load("data.json")
    result_dict = data.get_technique_stats(db)
    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[0].lower()))
    return render_template('techniques.html', page_name='Techniques',
                           techniques=sorted_dict, stylesheets=['technique.css', 'techniques.css'])


@app.errorhandler(404)
def page_not_found(e):
    """
    Using the data layer, Jinja2, and the 404.html template this function
    returns a basic page informing the user that a 404 error occurred.

    This function is called when the server can't find a page fitting the requested
    URL(404).

    :return: A basic 404 information page.
    """
    return render_template("status_codes/404.html", page_name='Error Page',
                           non_existent_url=request.path, stylesheets=['status_codes/404.css'])


if __name__ == '__main__':
    file_handler = FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
