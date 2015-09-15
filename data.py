import json
import pprint

def load(filename):
    try:
        with open(filename) as file:
            unsorted_json = json.loads(file.read())
            sorted_json = sort(unsorted_json)
            return sorted_json
    except FileNotFoundError:
        return None
    


def get_project_count(db):
    return len(db)


def get_project(db, id):
    for project in db:
        if project['project_no'] == id:
            return project
    return None


def has_techniques(project, techniques):
    if techniques is None:
        return True
    project_techniques = set(project['techniques_used'])
    return set(techniques) <= project_techniques


def search_parameter_in_field(project, fields, search_parameter):
    if search_parameter is None:
        return True
    for field in fields:
        field_value = project[field]
        if isinstance(field_value, str):
            if search_parameter.lower() in field_value.lower():
                return True
        elif isinstance(field_value, int):
            try:
                search_number = int(search_parameter)
                if search_number == field_value:
                    return True
            except:
                pass
    return False


def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=0):
    filtered_projects = []

    for project in db:
        if has_techniques(project, techniques) and search_parameter_in_field(project, search_fields, search):
            filtered_projects.append(project)

    filtered_projects = sort(filtered_projects, sort_by, sort_order)

    return filtered_projects

def sort(db, sort_by='project_no',sort_order='desc'):
	return sorted(db, key=lambda x: x[sort_by], reverse=sort_order == 'desc')

def get_techniques(db):
    techniques = []
    for project in db:
        techniques.extend(project['techniques_used'])
    return sorted(list(set(techniques)))


def get_technique_stats(db):
    technique_stats = {}
    for project in db:
        for technique in project['techniques_used']:
            if technique not in technique_stats:
                technique_stats[technique] = [{'id': project['project_no'], 'name': project['project_name']}]
            else:
                technique_stats[technique].append({'id': project['project_no'], 'name': project['project_name']})
    return technique_stats
