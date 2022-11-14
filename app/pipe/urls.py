from django.urls import path

from . import views

app_name = 'pipe'

urlpatterns = [
    path('', views.index,name='index'),
    path('<int:tiket_id>/', views.detail,name='detail'),
    path('thred/create/<int:tiket_id>/', views.thred_create, name='thred_create'),
    path('ajax_test/', views.ajax_test, name='ajax_test'),
    path('<int:tiket_id>/<int:thred_num>/list', views.thred_list, name ='thred_list')
]