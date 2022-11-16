import os, subprocess, sys  
from datetime import datetime
import json, xmltodict

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
def git_clone(userName, accessToken, branch, repoUrl, Tiket, Thred):
    clone = f"https://{userName}:{accessToken}@{repoUrl}"
    dir = f"../Storage/{Tiket}/{Thred}"
    result = subprocess.run(['git','clone','-b',branch,'--single-branch',clone,dir],capture_output=True, text=True)
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
        <directory name="simple-php-website"/>
        <ignoreFiles>
            <directory name="vendor"/>
        </ignoreFiles>
    </projectFiles>
<plugins><pluginClass class="Psalm\LaravelPlugin\Plugin"/></plugins></psalm>'''
def psalm(Tiket, Thred):
    execbin = f'../Storage/vendor/bin/psalm'
    configFile = f'../Storage/{Tiket}.{Thred}.xml'
    execoption = f"--config={configFile}"
    output = f"--output-format=json"

    #1. create config file
    confDict = xmltodict.parse(confxml)
    confDict['psalm']['projectFiles']['directory']['@name'] = f"{Tiket}/{Thred}/"
    Newconf = xmltodict.unparse(confDict, pretty=True)
    with open(configFile,'w') as f:
        f.write(Newconf)

    #2. psaml analysis 
    result = subprocess.run([execbin,execoption,'--taint-analysis',output],capture_output=True, text=True)
    #3. return json 
    json_res = result.stdout
    print(result.stdout)
    #print(result.stderr)
    return result.stdout
    