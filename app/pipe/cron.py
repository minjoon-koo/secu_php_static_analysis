import os, subprocess, sys  
from datetime import datetime
import json, xmltodict
from jira import JIRA
from requests.auth import HTTPBasicAuth
import time
import os,dotenv, json,subprocess
from django.utils import timezone
from .models import Tiket,Thred, Result, Info
from .Tool import git_clone, psalm, jira,comment
from pathlib import Path
import requests

dotenv.load_dotenv()

os.chdir(os.path.dirname(os.path.realpath(__file__)))
ERROR_FATAL = 'fatal'

def slack_push(msg,url):
    payload = { "text" : msg }
    requests.post(url, json=payload)

def jira_sync():
    print("jira Sync")
    URL = os.environ.get("JIRA_URL")
    userName=os.environ.get("JIRA_USER_EMAIL")
    accessToken = os.environ.get("JIRA_ACCESS_TOKEN")
    projectKey = os.environ.get("JIRA_PROJECT_KEY")
    statusValue = os.environ.get("JIRA_STATUS_VALUE")
    slack_webhook_url = os.environ("SLACK_WEBHOOK_URL")
    jira_tiket = jira(URL, userName, accessToken, projectKey,statusValue)
    pipe_tiket = Tiket.objects.order_by('-create_date')
    issue_list = []
    for i in pipe_tiket:
        issue_list.append(i.jira_tiket)

    #tiket 생성
    for j in jira_tiket.keys():
        if j not in issue_list:
            print(f"create tiket - jira issue_num : {j}")
            create_msg = "[Sec]Code 점검 - 신규 이슈가 등록되었습니다."
            create_msg = create_msg + f" : {j}"
            slack_push(create_msg,slack_webhook_url)
            try:
                newTiket = Tiket(jira_tiket= j, status= statusValue, create_date= timezone.now())
            except Exception as e:
                print(e)
            newTiket.save()
            for k in jira_tiket[j]:
                newTiket.info_set.create(branch=k['branch'], repoURL=k['repoURL'].replace("https://",""), content=k['file_list'])
        else:
            print(f"already created tiket : {j}")
            #print(jira_tiket[j]['file_list'])
    

def pr_sync(jira_tiket):
    URL = os.environ.get("JIRA_URL")
    userName=os.environ.get("JIRA_USER_EMAIL")
    accessToken = os.environ.get("JIRA_ACCESS_TOKEN")
    projectKey = os.environ.get("JIRA_PROJECT_KEY")
    statusValue = os.environ.get("JIRA_STATUS_VALUE")

    options = {"server":URL}
    JQL = f"project = {projectKey} AND key={jira_tiket}"
    auth = HTTPBasicAuth(userName,accessToken)
    jira = JIRA(options, basic_auth = (userName, accessToken))
    jira_issue = jira.search_issues(JQL)
    jira_id = jira_issue[0].id

    REST_git_pr = requests.request(
        "GET",
        f"{URL}/rest/dev-status/latest/issue/detail?issueId={jira_id}&applicationType=GitHub&dataType=pullrequest",
        headers= {'Accept': 'application/json'}, 
        auth= HTTPBasicAuth(userName,accessToken)
    )
    res = json.loads(REST_git_pr.text)
    try :
        last_pr_num =  json.loads(REST_git_pr.text)['detail'][0]['pullRequests'][len(res['detail'][0]['pullRequests'])-1]['id'].replace('#','')
        print(f"{jira_tiket} pr num : {last_pr_num}")

        tiket_Obj = Tiket.objects.filter(jira_tiket = jira_tiket)
        tiket = tiket_Obj[0]

        if(tiket.pr_exec == 'executed' and tiket.pr_num != last_pr_num):
            tiket.pr_num = last_pr_num
            tiket.pr_exec = 'renew'
            print(f"pr num : {last_pr_num} renewal")
            tiket.save()
        elif(tiket.pr_num == last_pr_num):
            print(f"{last_pr_num} stay")
        else:
            tiket.pr_num = last_pr_num
            tiket.pr_exec = 'None'
            tiket.save()
            print(f"{last_pr_num} create")

    except:
        print(f"{jira_tiket} : not found pr num")



def pr_update(tiket):
    tiket_id = tiket.id
    print(f"tiket id = {tiket_id}")
    jira_tiket = tiket.jira_tiket
    print(f"jira tiket = {jira_tiket}")
    info = Info.objects.filter(tiket_id = tiket_id)
    accessToken = os.environ.get("GIT_ACCESS_TOKEN")
    userName = os.environ.get("GIT_USER_NAME")
    thred_cnt = Thred.objects.filter(tiket_id = tiket_id)
    thred = str(len(thred_cnt))
    print(f"{jira_tiket} (id={tiket_id}) : {thred}")
    checkResult = 'safety'
    file_list = []

    try:
        temp = requests.post(
            f"http://localhost:8000/pipe/thred/create/{tiket_id}/",
            data={'thred':thred, 'jira_tiket':jira_tiket}
        )
    except Exception as e:
        print(e)     
    


def pr_batch():
    print("f============================")
    tikets = Tiket.objects.order_by('-create_date')
    for tiket in tikets:
        #if(tiket.pr_num == '') : print(tiket.jira_tiket)
        if(tiket.pr_num != '' and tiket.pr_exec != 'excuted') : 
            #print(f"{tiket.jira_tiket} : {tiket.pr_num}")
            pr_update(tiket)



def batch():
    jira_sync()
    tikets = Tiket.objects.order_by('-create_date')
    for tiket in tikets:
        pr_sync(tiket.jira_tiket)


