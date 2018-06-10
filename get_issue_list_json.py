import sys
import requests

def get_issue_list(redmine_url="", url_param=""):
    request_url = redmine_url + url_param
    response = requests.get(request_url)

    if response.status_code != 200:
        print ("Don't access Redemine.")
        print (request_url)
        print (response)
        sys.exit()

    return response.json()
