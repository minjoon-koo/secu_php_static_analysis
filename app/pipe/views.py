from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Tiket
from .Tool import git_clone
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
    #git_clone.test()
    #tiket.thred_set.create( create_date=timezone.now(), content=git_clone())
    git_clone("minjoon-koo","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","main","github.com/sldt-co-ltd/ats_test_template.git","3","3")
    return redirect('pipe:detail', tiket_id=tiket.id)

