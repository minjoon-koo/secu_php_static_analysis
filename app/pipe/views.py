from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tiket,Thred, Result
from .Tool import git_clone, psalm

import time
import os,dotenv, json
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
    branch = request.POST.get('branch')
    thred = int(request.POST.get('thred'))+1
    repoURL = request.POST.get('repoURL')
    accessToken = os.environ.get("GIT_ACCESS_TOKEN")
    userName = os.environ.get("GIT_USER_NAME")
    checkResult = 'safety'

    git_msg = git_clone(userName=userName, accessToken=accessToken, branch=branch, repoUrl = repoURL, Tiket=tiket.id, Thred=thred)
    if(git_msg.find(ERROR_FATAL) != -1) : return redirect('pipe:detail', tiket_id=tiket.id)
    ps_msg = json.loads(psalm(Tiket=tiket_id, Thred=thred))
    if(len(ps_msg)) :  checkResult = 'Warning'
    
    tiket.thred_set.create(content=f"SEC-CODE-{repoURL}-{branch}", create_date=timezone.now(), 
    psalmResult =len(ps_msg),checkResult=checkResult, thred_num=thred)

    for i in ps_msg:
        tiket.result_set.create(thred = thred, Type=i['type'],
        file_name=i['file_name'].replace(f"{tiket_id}/{thred}",""),line_from=i['line_from'],line_to=i['line_to'],
        snippet=i['snippet'],messages=i['message'],link=i['link'],taint_trace=i['taint_trace'])
        
    return redirect('pipe:detail', tiket_id=tiket.id)
    #return JsonResponse(tmp)

@csrf_exempt
def ajax_test(request):
    temp = request.POST.get('msg')
    #time.sleep(5)
    tmp= psalm("3","4")
    context = {"test":temp}
    return JsonResponse(context)
    #return JsonResponse(tmp)

def thred_list(request, tiket_id,thred_num):
    tiket = get_object_or_404(Tiket,pk=tiket_id)
    thred = get_object_or_404(Thred,thred_num = thred_num)
    result = Result.objects.filter(thred=thred_num)
    #result = filter_object_or_404(Result,thred=thred_num)
    context = {'tiket': tiket, 'thred':thred, 'result':result}
    return render(request, 'pipe/thred_list.html',context )