from requests.auth import HTTPBasicAuth
from termcolor import colored
from datetime import  datetime, timedelta
import requests
import urllib3
import json
import os
import base64

class Jira:
    def __init__(self,fields=["key"],expand=[],jiraurl=None,jirauser=None,jiratoken=None):
        os.system('color >/dev/null 2>&1')
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
        if jiraurl==None:   
            file_name='settings.json'
            print(colored('Reading settings from '+file_name, 'yellow'))
            with open(file_name) as f:
                
                data = f.read()
                settings = json.loads(data)
                self.url = settings["jiraurl"]
                self.jirauser =  self.Decode(settings["jirauser"])
                self.jiratoken = self.Decode(settings["jiratoken"])
                f.close()
        else:
            self.url = jiraurl
            self.jirauser = self.Decode(jirauser)
            self.jiratoken = self.Decode(jiratoken)
        self.auth = HTTPBasicAuth(self.jirauser, self.jiratoken)
        self.headers = {
              "Accept": "application/json",
              "Content-Type": "application/json",
            }
        self.fields=fields
        self.expand=expand
        
    def Decode(self,base64_message):
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message
                
    def Encode(self,message):
       
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message
        
    def GetSprint(self,boardid,sprintname):
        sprints=self.BoardSprints(boardid)
        for key in sprints:
            sprint=sprints[key]
            if(sprintname.lower()== sprint["name"].lower()):
                return sprint
        
        return None
    
    def SprintReport(self,boardid,sprintid):
        url = self.url+f"/rest/greenhopper/1.0/rapid/charts/sprintreport"
        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params={
                "rapidViewId" : boardid,
                "sprintId": sprintid
            },
            auth=self.auth,
            verify=False,
            
        )
        data=json.loads(response.text)
        return data['contents']
        
    def GetIssuesInSprint(self, sprintid,fields=['key'],expand='name,operations'):
        startAt=0
        maxResults=500
        url = self.url+f"/rest/agile/1.0/sprint/{sprintid}/issue"
        issues=[]
        while(1):
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                params={
                    "startAt": startAt,
                    "maxResults": maxResults,
                    "fields":fields,
                    "expand":expand
                },
                auth=self.auth,
                verify=False,
                
            )
            startAt=startAt+maxResults;
            data=json.loads(response.text)
            
            for d in data["issues"]:
                issues.append(d)
            if len(data["issues"])==0:
                break
        return issues;
    def ParseIssues(self, issues):
        for issue in issues:
            #print(issue['key'])
            issue['transactions']={'sprint':[]}
            for history in issue['changelog']['histories']:
                created=history["created"]
                for item in history['items']:
                    
                    if(item['field']=='Sprint'):
                       #print(item['fromString'])
                       
                       #print(item['fromString'],created,item['toString'])
                       
                       created=created.replace("T"," ")
                       created=created.split(".")[0]
                       item['date']=datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
                       
                       if item['from']==None:
                            item['from']=0
                       if item['to']==None:
                            item['to']=0
                       
                       if item['from']!=0:
                            item['from']=item['from'].split(",").pop().strip()
                            if item['from']==0:
                                item['from']=0
                                
                       if item['to']!=0:
                            item['to']=item['to'].split(",").pop().strip()
                            if( item['to'] == ''):
                                 item['to']=0
                      
                       
                       if item['fromString']==None:
                            item['fromString']=''
                       if item['toString']==None:
                            item['toString']=''
                       
                       if item['fromString']!='':
                            item['fromString']=item['fromString'].split(",").pop().strip()
                       if item['toString']!='':
                            item['toString']=item['toString'].split(",").pop().strip()
                       
                            
                       #print(item['fromString'].split(",")[0])
                       issue['transactions']['sprint'].append(item)
        return issues
        
        
    def BoardIssues(self,boardid,jql,fields=None,expand=None):
        if fields==None:
            fields=self.fields
        if expand==None:
            expand=self.expand 
            
        startAt=0
        maxResults=50
        url = self.url+f"/rest/agile/1.0/board/{boardid}/issue"
        issues=[]
        while(1):
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                params={
                    "startAt": startAt,
                    "maxResults": maxResults,
                    "jql":jql,
                    "fields": fields,
                    "expand":expand,
                    
                },
                auth=self.auth,
                verify=False,
                
            )
            startAt=startAt+maxResults;
            data=json.loads(response.text)
            for d in data["issues"]:
                issues.append(d)
            if len(data["issues"])==0:
                break
        
        return self.ParseIssues(issues)
       

    def BoardSprints(self, boardid,state='closed,active,future'):
        startAt=0
        maxResults=50
        url = self.url+f"/rest/agile/1.0/board/{boardid}/sprint"
        sprints=[]
        while(1):
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                params={
                    "startAt": startAt,
                    "maxResults": maxResults,
                    "state":state
                },
                auth=self.auth,
                verify=False,
                
            )
            startAt=startAt+maxResults;
            data=json.loads(response.text)
            for d in data["values"]:
                sprints.append(d)
            if len(data["values"])==0:
                break
        output={}
        for sprint in sprints:
            output[sprint["id"]]=sprint
            if "activatedDate" in sprint:
                sprint["activatedDate"]=sprint["activatedDate"].replace("T"," ")
                sprint["activatedDate"]=sprint["activatedDate"].split(".")[0]
                sprint["activatedDate"]=datetime.strptime(sprint["activatedDate"], '%Y-%m-%d %H:%M:%S')
            
            if "completeDate" in sprint:
                sprint["completeDate"]=sprint["completeDate"].replace("T"," ")
                sprint["completeDate"]=sprint["completeDate"].split(".")[0]
                sprint["completeDate"]=datetime.strptime(sprint["completeDate"], '%Y-%m-%d %H:%M:%S')
            
        return output
    def GetSprintById(self, sprintId):
        url = self.url+f"/rest/agile/1.0/sprint/{sprintId}"
        response = requests.request(
                "GET",
                url,
                headers=self.headers,
                params={
                    "sprintId":sprintId
                },
                auth=self.auth,
                verify=False,
            )
        data=json.loads(response.text)
        if 'errorMessages' in data:
            return None
        print(data)

    def Search(self,jql,fields=None,expand=[]):

        if fields==None:
            fields=self.fields
        
        startAt=0
        maxResults=500
        url = self.url+"/rest/api/latest/search"
        issues=[]
        while(1):
            payload = json.dumps( 
                {
                    "jql": jql,
                    "startAt": startAt,
                    "maxResults": maxResults,
                    "fields": fields,
                    "expand": expand
                }
            )
            response = requests.request(
                "POST",
                url,
                headers=self.headers,
                data=payload,
                auth=self.auth,
                verify=False
            )
            startAt=startAt+maxResults;
            data=json.loads(response.text)
            #print(data)
            #print(len(data["issues"]))
            for d in data["issues"]:
                if 'changelog' in d:
                    for history in d['changelog']['histories']:
                        print(history["created"])
                        for item in history['items']:
                            if(item['field']=='Sprint'):
                               print(item['fromString'])
                               print(item['toString'])
                       
                issues.append(d)
                
            if len(data["issues"])==0:
                break
                        
        return issues
        