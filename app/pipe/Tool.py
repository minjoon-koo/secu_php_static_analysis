import os, subprocess, sys  
from datetime import datetime
import json

os.chdir(os.path.dirname(os.path.realpath(__file__)))

'''
git clone parameter 샘플
{
    
}
'''

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
    return result.stdout