#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import data
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


log_file = "server.log"


@app.before_request
def request_logging():
    """
    This function logs each request the server gets.

    This function is called before each request is handled.
    """
    app.logger.info("Request: " + str(request) + " Form data: " + str(dict((key, request.form.getlist(key)) for key in request.form.keys())))


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
            """.format(
                method = request.method,
                path = request.path,
                ip = request.remote_addr,
                agent_platform = request.user_agent.platform,
                agent_browser = request.user_agent.browser,
                agent_browser_version = request.user_agent.version,
                agent = request.user_agent.string,
                form_data = str(dict((key, request.form.getlist(key)) for key in request.form.keys()))
            )
        )
    return render_template('500.html')


@app.route('/')
def main_page():
    """
    Using the data layer, Jinja2, and the main.html template this function
    returns the main page of the portfolio to whoever sent the request.

    This function is called when the URL '/' is requested.

    :return: The main page HTML of our portfolio.
    """
    db = data.load("data.json")
    example_project = data.search(db)[0]
    return render_template('main.html', project_data = example_project)


@app.route('/list', methods=['POST','GET'])
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
        requested_order = request.form['sort_order']
        requested_free_text_search = request.form['free_text_search']
        if requested_free_text_search == '':
            requested_free_text_search = None
        search_results = data.search(full_list, techniques=requested_technique_list,
                                                sort_order=requested_order,
                                                search = requested_free_text_search)

        return render_template('list.html', project_list=search_results,
                                            previous_freetext_search= requested_free_text_search or '',
                                            previous_techniques =requested_technique_list,
                                            techniques = sorted(techniques.keys()))


    else:
        return render_template('list.html', project_list = full_list,
                                            techniques = techniques.keys())


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
    return render_template('techniques.html', techniques = result_dict)


@app.errorhandler(404)
def page_not_found(e):
    """
    Using the data layer, Jinja2, and the 404.html template this function
    returns a basic page informing the user that a 404 error occurred.

    This function is called when the server can't find a page fitting the requested
    URL(404).

    :return: A basic 404 information page.
    """
    return render_template("404.html", non_existent_url = request.path)


if __name__ == '__main__':
    app.logger.setLevel(0)
    app.run(debug=True)
