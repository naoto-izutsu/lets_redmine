# coding: utf-8
import configparser
import json
import requests
import datetime
from datetime import datetime, date, timedelta
import time
import sys
import re
import os
import get_redmine_list as grl

# 引数チェック
args = sys.argv
argc = len(args)
if argc == 2:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[1]):
        from_date = args[1]
        to_date = ""
    else:
        print ("引数は「YYYY-mm-DD」の形でおねがいします。")
elif argc == 3:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[1]) and re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[2]):
        from_date = args[1]
        to_date = args[2]
    else:
        print ("引数は「YYYY-mm-DD」の形でおねがいします。")
else:
    yesterday = date.today() - timedelta(days=1)
    from_date = yesterday.strftime('%Y-%m-%d')
    to_date = ""

# 変数定義
projects_list_name = []
projects_list_id = []
num_limit = 100
num_pager = 0
num_count = 0
ticket_alert_sum = 0
ticket_incident_sum = 0

inifile = configparser.SafeConfigParser()
inifile.read('./redmine_bot.conf')

# Load configuration
redmine_url = inifile.get('RedmineSettings','redmine_url')
api_key = inifile.get('RedmineSettings', 'api_key')
projet_list = inifile.get('Parameter', 'projet_list')

# print header
if argc == 2 or argc == 1:
    print ("■チケット起票数(アラート,インシデント)(" + str(from_date) + ")")
elif argc == 3:
    print ("■チケット起票数(アラート,インシデント)(" + str(from_date) + "〜" + str(to_date) +")")

## 1行ずつ読み込む
## ファイルを開く
with open("project_list.conf", "r", encoding="UTF-8") as fh:
    for line in fh:
        line = line.rstrip('\r\n')
        project_elements = line.split(',')

        # アラート件数を取る
        tracker_id = 28
        status_id = "*"
        json_data = grl.get_project_list(param_url = redmine_url, param_key = api_key, param_project = project_elements[1], param_from = from_date, param_to = to_date, param_tracker = tracker_id, param_status = status_id)
        ticket_alert_count = json_data['total_count']
        ticket_alert_sum = ticket_alert_sum + ticket_alert_count

        # インシデント件数を取る
        tracker_id = 29
        status_id = "*"

        json_data = grl.get_project_list(param_url = redmine_url, param_key = api_key, param_project = project_elements[1], param_from = from_date, param_to = to_date, param_tracker = tracker_id, param_status = status_id)
        ticket_incident_count = json_data['total_count']
        ticket_incident_sum = ticket_incident_sum + ticket_incident_count

        # 件数を表示
        print (project_elements[2] + "," + str(ticket_alert_count) + "," + str(ticket_incident_count))

# 合計件数を表示
print ("合計," + str(ticket_alert_sum) + "," + str(ticket_incident_sum))
