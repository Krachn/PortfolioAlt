# -*- coding: UTF-8 -*-

from io import StringIO
import json
import pprint

def load(filename):
    try:
        file = open(filename)
    except FileNotFoundError:
        return None

    data = json.loads(file.read())
    file.close()
    return data

def get_project_count(db):
    return len(db)

def get_project(db, id):
    for project in db:
        if project['project_no'] == id:
            return project
    return None

def search(db, sort_by = 'start_date', sort_order = 'desc', techniques = None, search = None, search_fields = 0):
    return []

def get_techniques(db):
    techniques = []
    for project in db:
        techniques.extend(project['techniques_used'])
    return sorted(list(set(techniques)))

def get_technique_stats(db):
    technique_stats = {}
    for project in db:
        for technique in project['techniques_used']:
            if not technique in technique_stats:
                technique_stats[technique] = [{'id':project['project_no'], 'name':project['project_name']}]
            else:
                technique_stats[technique].append({'id':project['project_no'], 'name':project['project_name']})
    return technique_stats
