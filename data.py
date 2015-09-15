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

def has_techniques(project, techniques):
    if techniques == None: return True
    project_techniques = set(project['techniques_used'])
    return set(techniques) <= project_techniques

def search_parameter_in_field(project, fields, search_parameter):
    if search_parameter == None: return True
    for field in fields:
        field_value = project[field]
        if isinstance(field_value,str):
            if search_parameter.lower() in field_value.lower(): return True
        elif isinstance(field_value,int):
            try:
                search_number = int(search_parameter)
                if search_number == field_value: return True
            except:
                pass
    return False

def search(db, sort_by = 'start_date', sort_order = 'desc', techniques = None, search = None, search_fields = 0):
    filtered_projects = []

    for project in db:
        pprint.pprint(project)
        print(has_techniques(project, techniques) and search_parameter_in_field(project, search_fields, search))
        if has_techniques(project, techniques) and search_parameter_in_field(project, search_fields, search):
            filtered_projects.append(project)

    filtered_projects = sorted(filtered_projects,key=lambda x: x[sort_by], reverse=sort_order=='desc')

    return filtered_projects

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
