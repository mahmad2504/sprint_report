from requests.auth import HTTPBasicAuth
from termcolor import colored
import subprocess
import requests
import urllib3
import json
import os
from Jira import Jira
from datetime import  datetime, timedelta
import sys

if len(sys.argv)!=2:
    print(colored("The syntax of the command is incorrect", 'red'))
    print('(run main.py "sprint name")')
    exit()
    

sprint_field="customfield_11040"
sprint_name=sys.argv[1]
sprint_id=""
fields=["summary","assignee","status","timespent","timetracking","issuelinks","description"]
expand=["changelog"]

#project_id=12397

j=Jira(jiraurl="https://jira.alm.mentorg.com",jirauser="aGltcA==",jiratoken="aG1pcA==")
sprints=j.BoardSprints(349)


sprint=j.GetSprint(349,sprint_name)
if sprint==None:
    print(colored("Sprint not found", 'red'))
    exit()
    
sprint_id=sprint["id"]
boardid=sprint['originBoardId']


report=j.SprintReport(boardid,sprint_id)
print(colored(f"Report:{sprint_name}", 'green'))
print(colored(f"Issues not completed in sprint", 'cyan'))


for issue in report["issuesNotCompletedInCurrentSprint"]:
    print(issue["key"])


print(colored(f"Issues Rmoved from sprint", 'cyan'))

for issue in report["puntedIssues"]:
    print(issue["key"])
    
    



