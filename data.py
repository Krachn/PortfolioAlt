import json


def load(filename):
    """
    Loads JSON formatted project data from a file and returns a list of all projects, sorted after project number.
    :param filename: The filename(string) containing project data.
    :return: All the project data(list) from the read file, or None.
    """
    try:
        with open(filename) as file:
            unsorted_json = json.loads(file.read())
            sorted_json = sort(unsorted_json)
            return sorted_json
    except FileNotFoundError:
        return None


def get_project_count(db):
    """
    Retrieves the number of projects in a project list.
    :param db: A list as returned by load.
    :return: The number(int) of projects in the list.
    """
    return len(db)


def get_project(db, id):
    """
    Fetches the project with the specified id from the specified list.
    If the specified project id does not exist, None is returned.
    :param db: A list as returned by load.
    :param id: The ID number(int) of the wanted project.
    :return: All project data(dict) for the specified project, or None.
    """
    for project in db:
        if project['project_no'] == id:
            return project
    return None


def has_techniques(project, techniques):
    """
    Checks whether a project contains all techniques specified by a list.
    :param project: The project to check.
    :param techniques: The techniques to look for.
    :return: True if all techniques were used in the projects, otherwise False.
    """
    if techniques is None:
        return True
    project_techniques = set(project['techniques_used'])
    return set(techniques) <= project_techniques


def search_parameter_in_field(project, fields, search_parameter):
    """
    Checks whether a search parameter can be found in one of a list of fields.
    :param project: The project to check.
    :param fields: The fields to search in.
    :param search_parameter: The parameter to search for.
    :return: True if the search parameter can be found in any of the fields, otherwise False.
    """
    print("parameter: " + str(search_parameter))
    search_fields = fields
    if search_parameter is None:
        return True
    if search_fields is None:
        search_fields = project.keys()
    for field in search_fields:
        field_value = project[field]
        if isinstance(field_value, unicode):
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


def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    """
    Fetches and sorts projects matching criteria from the specified list.
    :param db: A list as returned by load.
    :param sort_by: The name of the field to sort by.
    :param sort_order: The order to sort in. 'asc' for ascending, 'desc' for descending.
    :param techniques: List of techniques that projects must have to be returned. An empty list
           means this field is ignored
    :param search: Free text search string.
    :param search_fields: The fields to search for search in. If search_fields is empty, no results are returned.
           If search_fields is None, all fields are searched.
    :return: A list containing dictionaries for all the projects conforming to the specified search criteria.
    """
    filtered_projects = []
    for project in db:
        if has_techniques(project, techniques) and search_parameter_in_field(project, search_fields, search):
            filtered_projects.append(project)
    filtered_projects = sort(filtered_projects, sort_by, sort_order)
    return filtered_projects


def sort(db, sort_by='project_no',sort_order='desc'):
    """
    Sorts a list of projects by the specified field.
    :param db: A list as returned by load.
    :param sort_by: The name of the field to sort by.
    :param sort_order: The order to sort in. 'asc' for ascending, 'desc' for descending.
    :return: A sorted list of projects
    """
    return sorted(db, key=lambda x: x[sort_by], reverse=sort_order == 'desc')


def get_techniques(db):
    """
    Fetches a list of all the techniques from the specified project list in lexicographical order.
    :param db: A list as returned by load.
    :return: A alphabetically sorted list containing the names of all techniques in db.
    """
    techniques = []
    for project in db:
        techniques.extend(project['techniques_used'])
    return sorted(list(set(techniques)))


def get_technique_stats(db):
    """
    Collects and returns statistics for all techniques in the specified project list.
    The key of each entry in the returned dictionary is the technique name, and the value is a list of dictionaries for
    each of the projects using the technique.

    Each of those dictionaries representing a project has the keys:
    * id (int): Project number
    * name (string): Name of the project

    The value of each key is sorted after the id-value of each dict in the list

    :param db: A list as returned by load.
    :return: Technique stats (see above).
    """
    technique_stats = {}
    for project in db:
        for technique in project['techniques_used']:
            if technique not in technique_stats:
                technique_stats[technique] = [{'id': project['project_no'], 'name': project['project_name']}]
            else:
                technique_stats[technique].append({'id': project['project_no'], 'name': project['project_name']})
    return technique_stats
