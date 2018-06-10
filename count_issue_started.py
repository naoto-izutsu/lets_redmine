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
import get_redmine_list as grl
import codecs

# UTF-8で出力するためのおまじない
sys.stdout= io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 変数定義
projects_list_name = []
projects_list_id = []
num_limit = 100
num_pager = 0
num_count = 0
ticket_sum = 0


# 引数チェック
args = sys.argv
argc = len(args)

if argc <= 1:
    sys.exit("E0001:引数が足りません")
elif argc == 1:
    yesterday = date.today() - timedelta(days=1)
    FROM_DATE = yesterday.strftime('%Y-%m-%d')
elif argc == 2:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[2]):
        target_date = args[2]
    else:
        print ("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[2] + ")")
        sys.exit()
#        sys.exit("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[2] + ")")
elif argc == 3:
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[2]) and re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$',args[3]):
        if args[2] <= args[3]:
            FROM_DATE = args[2]
            TO_DATE = args[3]
        else:
            print ("E0004:日付の範囲指定は、From < To となるように指定してください。(引数：" + args[2] + ", " + args[3] + ")")
            sys.exit()
#            sys.exit("E0004:日付の範囲指定は、From < To となるように指定してください。(引数：" + args[2] + ", " + args[3] + ")")
    else:
        print ("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[2] + ", " + args[3] + ")")
        sys.exit()
#        sys.exit("E0003:引数は「YYYY-mm-DD」の形でおねがいします。(引数：" + args[2] + ", " + args[3] + ")")


# Load configuration
inifile = configparser.SafeConfigParser()
inifile.read('redmine.conf')

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
with open("bin/redmine/project_list.conf", "r", encoding="UTF-8") as fh:
    for line in fh:
        line = line.rstrip('\r\n')
        project_elements = line.split(',')

        # アラート件数を取る
        if argc == 4:
            URL_PARAM = "/issues.json?key="+REDMINE_API_KEY+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on=%3E%3C"+str(FROM_DATE)+"|"+str(TO_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*"
        else:
            URL_PARAM = "/issues.json?key="+REDMINE_API_KEY+"&project_id="+str(REDMINE_PROJECT_ID)+"&created_on="+str(FROM_DATE)+"&tracker_id="+str(tracker_id)+"&status_id=*"

        json_data = grl.get_project_list(REDMINE_URL, URL_PARAM)
        ticket_count = json_data['total_count']
        ticket_sum = ticket_sum + ticket_count

        # 件数を表示
        print (project_elements[2] + "," + str(ticket_count))
#        output = project_elements[2] + "," + str(ticket_count)
#        print output.decode('utf-8')

# 合計件数を表示
print ("合計," + str(ticket_sum))
