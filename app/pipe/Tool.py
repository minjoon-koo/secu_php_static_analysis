import os, subprocess, sys  
from datetime import datetime
import json, xmltodict
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth

os.chdir(os.path.dirname(os.path.realpath(__file__)))


'''소스코드 점검 대상 github code 
git clone -b [branch name] --single-branch https://\
        [id]:[acc-token]@\
        github.com/sldt-co-ltd/\
        [repo-name].git
[branch name] -> clone 대상 branch
[id] -> github name (메일주소 아님)
[acc-token] -> 엑세스 토큰 (https://github.com/settings/tokens 발급)
[repo-name] -> 대상 repo
ex)
git clone -b test --single-branch https://minjoon-koo:[git-acc-token]@github.com/test/test.git
'''
def git_clone(userName, accessToken, branch, repoUrl, Tiket, Thred, No):
    clone = f"https://{userName}:{accessToken}@{repoUrl}.git"
    dir = f"../Storage/{Tiket}/{Thred}/{No}"
    subprocess.run(['rm','-rf',dir])
    result = subprocess.run(['git','clone','-b',branch,'--single-branch',clone,dir],capture_output=True, text=True)
    print(result.stderr)
    return result.stderr


confxml = '''<?xml version="1.0"?>
<psalm
    errorLevel="1"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
>
    <projectFiles>
        <file name="test.php"/>
        <ignoreFiles>
            <directory name="vendor"/>
        </ignoreFiles>
    </projectFiles>
<plugins><pluginClass class="Psalm\LaravelPlugin\Plugin"/></plugins></psalm>'''
def psalm(Tiket, Thred,file_list):
    execbin = f'../Storage/vendor/bin/psalm'
    configFile = f'../Storage/{Tiket}.{Thred}.xml'
    execoption = f"--config={configFile}"
    output = f"--output-format=json"

    #1. create config file
    confDict = xmltodict.parse(confxml)
    dump = []
    for i in file_list:
        rf = f"{Tiket}/{Thred}/{i}"
        path = {"@name":rf}
        dump.append(path)
    confDict['psalm']['projectFiles']['file'] = dump    

            
    #confDict['psalm']['projectFiles']['directory']['@name'] = f"{Tiket}/{Thred}/"
    Newconf = xmltodict.unparse(confDict, pretty=True)
    with open(configFile,'w') as f:
        f.write(Newconf)
    #2. psaml analysis 
    result = subprocess.run([execbin,execoption,'--taint-analysis',output],capture_output=True, text=True)
    #3. return json 
    json_res = result.stdout

    print(result.stdout)
    print(result.stderr)
    return result.stdout


'''
jira 이슈 관리 방법 또는
배포 방식이 어떻게 변동되느냐에 따라 변수를 받느냐 고정 값으로 서칭하느냐 등
변경이 필요 할 것으로 보입니다.

현재 DEMO버전에서는 아래의 고정 값을 기준으로 이슈, 브랜치 서칭하도록 구현 함


#파이선 모듈
>>> from jira import JIRA
>>> import requests
>>> from requests.auth import HTTPBasicAuth

#배포 이슈 생성되는 jira 정보
url = 'https://xxxxxxx.atlassian.net'
options = {"server":url}
project = 'XXXXXX'
status = '배포대기'
JQL = f"project ={project} AND status = {status}" 
REST_git_branch = f"""{url}/rest/dev-status/latest/issue/detail?issueId={issue_id}&applicationType=GitHub&dataType=branch"""

'''

def jira(URL, userName, accessToken, projectKey,statusValue):
    #함수 최종 리턴 값 
    #repoName
    #repoURL
    #branch
    #jira issue_Key
    '''
    {
         Issue_key : { 
            repoName : 'Name', 
            repoURL : 'url',
            branch : 'branch',
            id : 'id',
            file_list : [str,str,str],
            }, 
    }'''
    '''리턴 타입변경 --> 멀티 브런치
     {
         Issue_key : [
            { 
                repoName : 'Name', repoURL : 'url', branch : 'branch', id : 'id',file_list : [str,str,str]
            },
            { 
                repoName : 'Name', repoURL : 'url', branch : 'branch', id : 'id',file_list : [str,str,str]
            }
        ]
    }   
    '''
    tiket_dict = {}

    #jira objects 에서 issue id 추출
    options = {"server":URL}
    JQL = f"project = {projectKey} AND status = {statusValue}"
    auth = HTTPBasicAuth(userName,accessToken)

    jira = JIRA(options, basic_auth =(userName, accessToken))
    ###jira_issue : return SELECT LIST 
    #[<JIRA Issue: key='SEC-95', id='27006'>, <JIRA Issue: key='SEC-89', id='26698'>,]
    jira_issue = jira.search_issues(JQL)

    kim = 0
    for i in jira_issue:
        REST_git_branch = requests.request(
            "GET", 
            f"{URL}/rest/dev-status/latest/issue/detail?issueId={i.id}&applicationType=GitHub&dataType=branch", 
            headers= {'Accept': 'application/json'}, 
            auth= HTTPBasicAuth(userName,accessToken)
            )
        REST_JSON = json.loads(REST_git_branch.text)

        REST_git_commit = requests.request(
            "GET", 
            f"{URL}/rest/dev-status/latest/issue/detail?issueId={i.id}&applicationType=GitHub&dataType=repository", 
            headers= {'Accept': 'application/json'}, 
            auth= HTTPBasicAuth(userName,accessToken)
            )
        REST_ADD = json.loads(REST_git_commit.text)
        #print(REST_JSON['detail'][0]['branches'][0]['name'])
        #print(json.dumps(REST_ADD))
        try:
            '''
            file_dump = []
            for k in REST_ADD['detail'][0]['repositories'][0]['commits']:
                for h in k['files']:
                    file_dump.append(h['path'])
            file_list_set = set(file_dump)
            file_list = list(file_list_set)
            '''
            info_list = []
            for detail in REST_JSON['detail'][0]['branches']:
              bN = detail['name']
              rN = detail['repository']['name']
              rU = detail['repository']['url']

              file_dump = []
              for k in REST_ADD['detail'][0]['repositories']:
                if(k['url'] == rU):
                  for h in k['commits']:
                    for l in h['files']:
                      file_dump.append(l['path'])
              file_list_set = set(file_dump)
              file_list = list(file_list_set)

              info_dict={
                "repoName" : rN ,
                "repoURL" : rU,
                "branch" : bN,
                "id" : i.id,
                "file_list" : file_list 
              }
              info_list.append(info_dict)
            
              tiket_dict[i.key]= info_list

        except:
            print(f"{i.key} : not found GITHUB BRANCH")
    
    return tiket_dict

def comment(URL, userName, accessToken, statusValue, jira_tiket, psalmResult, pipe_url):
    text =f'[SEC_CODE]점검 결과 : {psalmResult}개 취약패턴이 검출되었습니다.\n > 상세 내용 확인 : {pipe_url}'
    if(psalmResult == '0') : text = f'[SEC_CODE]점검 완료 되었습니다\n > 상세 내용 확인 : {pipe_url}'
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

    data=json.dumps({
            "body": {
                "type": "doc", 
                "version": 1, 
                "content": [{
                        "type": "paragraph", 
                        "content": [{
                                "text": text, 
                                "type": "text"
                                }]
                            }]
                    }
        })

    push_result=requests.post(
        f"{URL}/rest/api/3/issue/{jira_tiket}/comment",
        headers= headers, 
        data=data,
        auth=HTTPBasicAuth(userName,accessToken)
        )