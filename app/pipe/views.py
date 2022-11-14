from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tiket
from .Tool import git_clone, psalm

import time
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
    request.POST.get('branch')
    request.POST.get('thred')
    request.POST.get('repoURL')
    #tiket.thred_set.create( create_date=timezone.now(), content=tmp)
    #git_clone("minjoon-koo","1111","main","github.com/sldt-co-ltd/ats_test_template.git","3","3")
    #tmp= psalm("3","4")

    #tiket.thred_set.create( create_date=timezone.now(), content=tmp)
    ajax_test(request)
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
    return render(request, 'pipe/thred_list.html')