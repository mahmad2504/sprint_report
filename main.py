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
print(colored(f"Report-s:{sprint_name}", 'green'))
print(colored(f"Issues not completed in sprint", 'cyan'))


for issue in report["issuesNotCompletedInCurrentSprint"]:
    print(issue["key"])


print(colored(f"Issues Rmoved from sprint", 'cyan'))

for issue in report["puntedIssues"]:
    print(issue["key"])
#print(report["puntedIssues"])

exit()

print(sprint_name,"(",sprint["state"],")")

if sprint["state"] == 'closed':
    issues=j.Search(f'sprint in ("{sprint_name}")',fields=["key"])
    for issue in issues:
        #print(issue)
        print(issue['key'])
    #startDate=datetime.strptime(sprint['activatedDate'].split("T")[0], '%Y-%m-%d')
    #completeDate=datetime.strptime(sprint['completeDate'].split("T")[0], '%Y-%m-%d')
  
    #print(sprint['activatedDate'])
    #print(sprint['completeDate'])
    activatedDate=sprint['activatedDate'] + timedelta(days=-1)
    completeDate=sprint['completeDate']+timedelta(days=1)
    
    #print(activatedDate)
    #print(completeDate)
    
    issues=j.BoardIssues(boardid,f'updated >= {activatedDate.strftime("%Y-%m-%d")} and updated <= {completeDate.strftime("%Y-%m-%d")}')
    for issue in issues:
        print(issue["key"])
        prev_sprint='Backlog'
        current_sprint='Backlog'
        for transaction in issue["transactions"]["sprint"]:
            if transaction['date'] >= sprint['activatedDate'] and transaction['date'] <= sprint['completeDate']:
                #print(sprint['activatedDate'],transaction['date'],sprint['completeDate'],transaction['fromString'],"--->",transaction['toString'])
                prev_sprint=int(transaction['from'])
                current_sprint=int(transaction['to'])
                
        #print(sprint_id,"+"+prev_sprint,current_sprint)
        if prev_sprint == sprint_id:
            if current_sprint != sprint_id:
                if current_sprint in sprints:
                    print(issue["key"],"Removed and moved to ",sprints[current_sprint]["name"])
                else:
                    print(issue["key"],"Removed and moved to ",current_sprint)
            
            #print(datetime.strptime(transaction['date'], '%Y-%m-%d %H:%M:%S'))
if  sprint["state"] == 'active':
    issues=j.Search(f'sprint in ("{sprint_name}")',fields=["key"])
    for issue in issues:
        #print(issue)
        print(issue['key'])
        
    activatedDate=sprint['activatedDate'] + timedelta(days=-1)
    issues=j.BoardIssues(boardid,f'updated >= {activatedDate.strftime("%Y-%m-%d")}')
    for issue in issues:
        print(issue["key"])
        prev_sprint='Backlog'
        current_sprint='Backlog'
        for transaction in issue["transactions"]["sprint"]:
            if transaction['date'] >= sprint['activatedDate']:
                print(sprint['activatedDate'],transaction['date'],transaction['fromString'],"--->",transaction['toString'])
                prev_sprint=int(transaction['from'])
                current_sprint=int(transaction['to'])
                
        
        #print(sprint_id,"+"+prev_sprint,current_sprint)
        if prev_sprint == sprint_id:
            if current_sprint  != sprint_id:
                if current_sprint in sprints:
                    print(issue["key"],"Removed and moved to ",sprints[current_sprint]["name"])
                else:
                    print(issue["key"],"Removed and moved to ",current_sprint)
      
        




