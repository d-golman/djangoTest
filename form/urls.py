from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='form-home'),    
    url('search', views.search),
    path('snippet', views.search)
]