#!/usr/bin/env python

import json
import argparse
import requests
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
try:
    config.read(os.path.expanduser('~/.togglrc'))
    toggl_api_token = config.get('toggl', 'token')
except:
    LOG.error('Please create a ~/.togglrc file with your token. View README for setup instructions.')


def toggl_query(url, params, method, payload=None):
    api_url = 'https://www.toggl.com/api/v8' + url
    auth = (toggl_api_token, 'api_token')
    headers = {'content-type': 'application/json'}

    if method == "POST":
        response = requests.post(api_url, auth=auth, headers=headers, params=params, data=payload)
    elif method == "PUT":
        response = requests.put(api_url, auth=auth, headers=headers, params=params)
    elif method == "GET":
        response = requests.get(api_url, auth=auth, headers=headers, params=params)
    else:
        raise UserWarning('GET, POST and PUT are the only supported request methods.')

    # If the response errored, raise for that.
    if response.status_code != requests.codes.ok:
        response.raise_for_status()

    return response.json()


def get_workspaces():
    return toggl_query('/workspaces', None, 'GET')


def get_workspace_projects(workspace_id):
    return toggl_query('/workspaces/' + workspace_id + '/projects', None, 'GET')


def create_project(project_name, workspace_id):
    project_data = {"name": project_name, 'wid': workspace_id}
    project_data_json = json.dumps({'project': project_data})
    return toggl_query('/projects', None, 'POST', project_data_json)


def get_running_timer():
    return toggl_query('/time_entries/current', None, 'GET')


def stop_timer(timer_id):
    return toggl_query('/time_entries/' + str(timer_id) + '/stop', None, 'PUT')


def start_timer(description, project_id):
    time_entry_data = {"description": description, 'pid': project_id, 'created_with': 'kmtoggl'}
    time_entry_data_json = json.dumps({'time_entry': time_entry_data})
    return toggl_query('/time_entries/start', None, 'POST', time_entry_data_json)


workspaces = get_workspaces()
workspace_id = str(workspaces[0]['id'])

# Build a dict of existing projects
workspace_projects = get_workspace_projects(workspace_id)
all_projects = {}
for project in workspace_projects:
    all_projects[project['name']] = project['id']

# Get the values from the command line arguments
project_name = str(os.environ['KMVAR_Project'])
task_name = str(os.environ['KMVAR_Time_entry_description'])

if not project_name or not task_name:
    raise UserWarning('Could not get project or time entry description from KMToggl')

project_id = None
# Get a project ID for the time entry
if project_name in all_projects:
    project_id = all_projects[project_name]
else:
    # Create the project
    project = create_project(project_name, workspace_id)
    project_id = project['data']['id']

if project_id is not None:
    # Get running time entry
    running_timer = get_running_timer()
    if running_timer['data'] is not None:
        stop_timer(running_timer['data']['id'])

    # Start a new time entry
    start_timer(task_name, project_id)
    print "Started timer for", task_name, "in project", project_name

exit()
