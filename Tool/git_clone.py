import os, subprocess, sys  
from datetime import datetime
import json
#import common  #cloud secret 등을 통해 추출 한 token key load를 위한 커스텀
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class test:
    def test():
        return 3

#Default Set
os.chdir(os.path.dirname(os.path.realpath(__file__)))
#conf = common.common()

'''
parameter 샘플
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

def CodePull(userName, accessToken, branch, repoUrl, Tiket, Thred):
    clone = f"https://{userName}:{accessToken}@{repoUrl}"
    dir = f"../Storage/{Tiket}/{Thred}"
    cmd = f"git -b {branch} --single-branch clone {clone} {dir}"
    #print(cmd)
    result = subprocess.run(['git','clone','-b',branch,'--single-branch',clone,dir],capture_output=True, text=True)


    print("=================")

    print(result.stdout)
    return esult.stdout
    #print(result.stderr)







def main(): #main 구성 1.policy_sentry를 이용한 정책 생성 / 2. boto3(aws lib)을 이용하여 정책 반영
    return CodePull("minjoon-koo","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","mai33n","github.com/sldt-co-ltd/starter-php.git","3","3")
    

if __name__ == '__main__':
    main()