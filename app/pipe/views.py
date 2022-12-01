from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tiket,Thred, Result, Info
from .Tool import git_clone, psalm, jira,comment

import time
import os,dotenv, json,subprocess
dotenv.load_dotenv()

# 공통 변수
ERROR_FATAL = 'fatal'


# Create your views here.

def index(request):
    tiket_list = Tiket.objects.order_by('-create_date')
    context = {'tiket_list': tiket_list}
    return render(request, 'pipe/tiket_list.html', context)

def detail(request, tiket_id):
    tiket = get_object_or_404(Tiket,pk=tiket_id)
    context = {'tiket': tiket}
    return render(request, 'pipe/Thred.html', context)

def thred_create(request, tiket_id):
    tiket = get_object_or_404(Tiket, pk=tiket_id)
    jira_tiket = request.POST.get('jira_tiket')
    info = Info.objects.filter(tiket_id = tiket_id)
    thred = int(request.POST.get('thred'))+1
    accessToken = os.environ.get("GIT_ACCESS_TOKEN")
    userName = os.environ.get("GIT_USER_NAME")
    checkResult = 'safety'
    #file_list = tiket.content.replace("\'","").replace("[","").replace("]","").replace(" ","").split(",")
    file_list = []

    No = 1
    for i in info:
        git_msg = git_clone(userName=userName, accessToken=accessToken, branch=i.branch, repoUrl = i.repoURL, Tiket=tiket.id, Thred=thred, No=str(No))
        if(git_msg.find(ERROR_FATAL) != -1) : return redirect('pipe:detail', tiket_id=tiket.id)
        commits = i.content.replace("\'","").replace("[","").replace("]","").replace(" ","").split(",")
        for j in commits:
            if(j.find(".lock") == -1):
                file_list.append(f"{No}/{j}")
        No = No +1
    
    print(file_list)
    
    psalm(Tiket=tiket_id, Thred=thred, file_list=file_list)
    ps_msg = json.loads(psalm(Tiket=tiket_id, Thred=thred, file_list=file_list))
    if(len(ps_msg)) :  checkResult = 'Warning'


    tiket.thred_set.create(content=f"{jira_tiket}", create_date=timezone.now(), 
    psalmResult =len(ps_msg),checkResult=checkResult, thred_num=thred)

    for i in ps_msg:
        tiket.result_set.create(thred = thred, Type=i['type'],
        file_name=i['file_name'].replace(f"{tiket_id}/{thred}",""),line_from=i['line_from'],line_to=i['line_to'],
        snippet=i['snippet'],messages=i['message'],link=i['link'],taint_trace=i['taint_trace'])

    if(checkResult == 'safety'):
        T = Tiket.objects.get(id =tiket_id)
        T.status = '점검 완료'
        T.save()

    JIRA_URL = os.environ.get("JIRA_URL")
    JIRA_userName=os.environ.get("JIRA_USER_EMAIL")
    JIRA_accessToken = os.environ.get("JIRA_ACCESS_TOKEN")
    T = Tiket.objects.get(id =tiket_id)
    SV = T.status
    SEC_URL = os.environ.get("SEC_URL")
    pipe_url = f"{SEC_URL}/pipe/{tiket.id}"
    tt = Thred.objects.get(thred_num=thred,tiket_id=tiket_id)
    comment(JIRA_URL,JIRA_userName,JIRA_accessToken, SV, "SEC-95",tt.psalmResult ,pipe_url)
    #subprocess.run(['rm','-rf',dir])

    return redirect('pipe:detail', tiket_id=tiket.id)
    #return JsonResponse(tmp)
   
'''
@csrf_exempt
def thred_create(request, tiket_id):
    print("입장")
    tiket = get_object_or_404(Tiket, pk=tiket_id)
    jira_tiket = request.POST.get('jira_tiket')
    branch = request.POST.get('branch')
    thred = int(request.POST.get('thred'))+1
    repoURL = request.POST.get('repoURL')
    accessToken = os.environ.get("GIT_ACCESS_TOKEN")
    userName = os.environ.get("GIT_USER_NAME")
    checkResult = 'safety'
    file_list = tiket.content.replace("\'","").replace("[","").replace("]","").replace(" ","").split(",")

    git_msg = git_clone(userName=userName, accessToken=accessToken, branch=branch, repoUrl = repoURL, Tiket=tiket.id, Thred=thred)
    if(git_msg.find(ERROR_FATAL) != -1) : return redirect('pipe:detail', tiket_id=tiket.id)
    psalm(Tiket=tiket_id, Thred=thred, file_list=file_list)
    ps_msg = json.loads(psalm(Tiket=tiket_id, Thred=thred, file_list=file_list))
    if(len(ps_msg)) :  checkResult = 'Warning'


    tiket.thred_set.create(content=f"{jira_tiket}-{repoURL}-{branch}", create_date=timezone.now(), 
    psalmResult =len(ps_msg),checkResult=checkResult, thred_num=thred)
  

    for i in ps_msg:
        tiket.result_set.create(thred = thred, Type=i['type'],
        file_name=i['file_name'].replace(f"{tiket_id}/{thred}",""),line_from=i['line_from'],line_to=i['line_to'],
        snippet=i['snippet'],messages=i['message'],link=i['link'],taint_trace=i['taint_trace'])

    if(checkResult == 'safety'):
        T = Tiket.objects.get(id =tiket_id)
        T.status = '점검 완료'
        T.save()

    return redirect('pipe:detail', tiket_id=tiket.id)
    #return JsonResponse(tmp)
'''


@csrf_exempt
def ajax_test(request):
    temp = request.POST.get('msg')
    print(temp)
    URL = os.environ.get("JIRA_URL")
    userName=os.environ.get("JIRA_USER_EMAIL")
    accessToken = os.environ.get("JIRA_ACCESS_TOKEN")
    projectKey = os.environ.get("JIRA_PROJECT_KEY")
    statusValue = os.environ.get("JIRA_STATUS_VALUE")

    jira_tiket = jira(URL, userName, accessToken, projectKey,statusValue)
    pipe_tiket = Tiket.objects.order_by('-create_date')
    issue_list = []
    for i in pipe_tiket:
        issue_list.append(i.jira_tiket)

    #tiket 생성
    for j in jira_tiket.keys():
        if j not in issue_list:
            print(f"create tiket - jira issue_num : {j}")
            newTiket = Tiket(jira_tiket= j, status= statusValue, create_date= timezone.now())
            newTiket.save()
            for k in jira_tiket[j]:
                newTiket.info_set.create(branch=k['branch'], repoURL=k['repoURL'].replace("https://",""), content=k['file_list'])
        else:
            print(f"already created tiket : {j}")
            #print(jira_tiket[j]['file_list'])
    
    context = {"test":temp}
    return JsonResponse(context)
    #return JsonResponse(tmp)


def thred_list(request, tiket_id,thred_num):
    tiket = get_object_or_404(Tiket,pk=tiket_id)
    thred = Thred.objects.filter(thred_num = thred_num)
    result = Result.objects.filter(thred=thred_num)
    #result = filter_object_or_404(Result,thred=thred_num)
    context = {'tiket': tiket, 'thred':thred, 'result':result}
    return render(request, 'pipe/thred_list.html',context )


def tiket_create(request):
    tiket_list = Tiket.objects.order_by('-create_date')
    context = {'tiket_list': tiket_list}
    return JsonResponse(context)

def error(request):
    return render(request, 'pipe/error.html')

def login(request):
    return render(request, 'pipe/login.html')