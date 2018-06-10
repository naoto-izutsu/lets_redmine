# coding: utf-8
import configparser
import json
import requests
import datetime
from datetime import datetime, date, timedelta
import time
import sys
import io
import re
import get_issue_list_json as gil
import codecs

# UTF-8で出力するためのおまじない
sys.stdout= io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 変数定義
projects_list_name = []
projects_list_id = []
ISSUE_LIST_LIMIT = 100
issue_list_offset = 0
issue_list_pager = 0
issue_list_remainder = 0
issue_list_count = 0
issue_sum = 0


# 引数チェック
args = sys.argv
argc = len(args)

print (argc)

if argc == 0:
    sys.exit("E0001:引数が足りません")
elif argc == 1:
    yesterday = date.today() - timedelta(days=1)
    FROM_DATE = yesterday.strftime('%Y-%m-%d')
    TO_DATE = FROM_DATE
elif argc == 2:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[1]):
        FROM_DATE = args[1]
        TO_DATE = FROM_DATE
    else:
        print ("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[1] + ")")
        sys.exit()
#        sys.exit("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[1] + ")")
elif argc == 3:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[1]) and re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[2]):
        if args[1] <= args[2]:
            FROM_DATE = args[1]
            TO_DATE = args[2]
        else:
            print ("E0004:日付の範囲指定は、From < To となるように指定してください。(引数：" + args[1] + ", " + args[2] + ")")
            sys.exit()
#            sys.exit("E0004:日付の範囲指定は、From < To となるように指定してください。(引数：" + args[1] + ", " + args[2] + ")")
    else:
        print ("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[1] + ", " + args[2] + ")")
        sys.exit()
#        sys.exit("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[1] + ", " + args[2] + ")")


# Load configuration
inifile = configparser.SafeConfigParser()
#inifile.read('redmine.conf')
inifile.read('redmine.conf.private')

REDMINE_URL = inifile.get('BASE_SETTINGS','REDMINE_URL')
REDMINE_API_KEY = inifile.get('BASE_SETTINGS', 'REDMINE_API_KEY')
REDMINE_PROJECT_ID = inifile.get('BASE_SETTINGS', 'REDMINE_PROJECT_ID')

# Print Header
#if argc == 4:
#    print ("■ISSUE起票数(" + str(tracker_name) + ")(" + str(FROM_DATE) + "～" + str(TO_DATE) + ")")
#else:
#    print ("■ISSUE起票数(" + str(tracker_name) + ")(" + str(FROM_DATE) + ")")

## 1行ずつ読み込む
## ファイルを開く
#with open("bin/redmine/project_list.conf", "r", encoding="UTF-8") as fh:
#    for line in fh:
#        line = line.rstrip('\r\n')
#        project_elements = line.split(',')
#
#        URL_PARAM = "/issues.json?key="+REDMINE_API_KEY+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on="+str(FROM_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*"
#
#        json_data = gil.get_issue_list(REDMINE_URL, URL_PARAM)
#        ticket_count = json_data['total_count']
#        issue_sum = issue_sum + ticket_count
#
#        # 件数を表示
#        print (project_elements[2] + "," + str(ticket_count))
##        output = project_elements[2] + "," + str(ticket_count)
##        print output.decode('utf-8')

# Issue JSON
tracker_id = 5
URL_PARAM = "/issues.json?key="+str(REDMINE_API_KEY)+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on=%3E%3C"+str(FROM_DATE)+"|"+str(TO_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*&offset="+str(issue_list_offset)+"&limit="+str(ISSUE_LIST_LIMIT)
json_data = gil.get_issue_list(REDMINE_URL, URL_PARAM)

#json_data = gil.get_issue_list('param_url':REDMINE_URL,'param_key':REDMINE_API_KEY,'param_project_id':REDMINE_PROJECT_ID,'','param_create':created_on,'param_tracker':tracker_id,'param_status_id':status_id,param_fromdate':FROM_DATE,'param_todate':TO_DATE,'param_offset':issue_list_offset,'param_limit':ISSUE_LIST_LIMIT)

TOTAL_ISSUE_COUNT = json_data['total_count']

print (TOTAL_ISSUE_COUNT)

issue_list_pager = TOTAL_ISSUE_COUNT // ISSUE_LIST_LIMIT
issue_list_remainder = TOTAL_ISSUE_COUNT % ISSUE_LIST_LIMIT
print (issue_list_pager)
print (issue_list_remainder)


if issue_list_pager == 0:
    ir = 0
    while ir < issue_list_remainder:
        print (u'{}\t{}'.format(json_data['issues'][ir]['id'],json_data['issues'][ir]['subject']))
        ir = ir + 1
else:
    ip = 0
    while ip < issue_list_pager:
        il = 0
        while il < ISSUE_LIST_LIMIT:
            print (u'{}\t{}'.format(json_data['issues'][il]['id'],json_data['issues'][il]['subject']))
            il = il + 1

        issue_list_pager = issue_list_pager - 1

        if issue_list_pager != 0:
            issue_list_offset = issue_list_offset + ISSUE_LIST_LIMIT
            URL_PARAM = "/issues.json?key="+str(REDMINE_API_KEY)+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on=%3E%3C"+str(FROM_DATE)+"|"+str(TO_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*&offset="+str(issue_list_offset)+"&limit="+str(ISSUE_LIST_LIMIT)
            json_data = gil.get_issue_list(REDMINE_URL, URL_PARAM)

    issue_list_offset = issue_list_offset + ISSUE_LIST_LIMIT
    URL_PARAM = "/issues.json?key="+str(REDMINE_API_KEY)+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on=%3E%3C"+str(FROM_DATE)+"|"+str(TO_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*&offset="+str(issue_list_offset)+"&limit="+str(ISSUE_LIST_LIMIT)
    json_data = gil.get_issue_list(REDMINE_URL, URL_PARAM)
    
    ir=0
    while ir < issue_list_remainder:
        print (u'{}\t{}'.format(json_data['issues'][ir]['id'],json_data['issues'][ir]['subject']))
        ir = ir + 1


#print ("合計," + str(issue_sum))
