# coding: utf-8
import sys
import requests

# param_url = redmine_url
# param_key = api_key
# param_project = project_id
# param_create = created_on
# param_from = from_date
# param_to = to_date
# param_tracker = tracker_id
# param_status = status_id

def get_issue_list(**kwargs):
    if kwargs['param_to'] == "" : # 日付指定
        request_url = kwargs['param_url'] + "/issues.json?key=" + kwargs['param_key'] + "&project_id=" + kwargs['param_project'] + "&created_on=" + kwargs['param_from'] + "&tracker_id=" + str(kwargs['param_tracker']) + "&status_id=" + kwargs['param_status']

    else: # 期間指定
        request_url = kwargs.get(param_url) + "/issues.json?key=" + kwargs.get(param_key) + "&project_id=" + str(kwargs.get(param_project)) + "&created_on=%3E%3C" + str(kwargs.get(param_from)) + "|" + str(kwargs.get(param_to))  + "&tracker_id=" + kwargs.get(param_tracker) + "&status_id=" + kwargs.get(param_status)

    response = requests.get(request_url)

    if response.status_code != 200:
        print ("Redemineへアクセスできませんでした。")
        print (request_url)
        print (response)
        sys.exit()

    return response.json()
