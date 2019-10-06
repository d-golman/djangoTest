from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='form-home'),    
    url(r'^external', views.external)
]