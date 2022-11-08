from django.urls import path

from . import views

app_name = 'pipe'

urlpatterns = [
    path('', views.index,name='index'),
    path('<int:tiket_id>/', views.detail,name='detail'),
    path('thred/create/<int:tiket_id>/', views.thred_create, name='thred_create'),
]