from django.urls import path, include, re_path
from django.views.generic import TemplateView
from apps.web import views as webviews
from apps.api.views import *

urlpatterns = [
#    path('', webviews.index, name='home'),
    path('', webviews.home, name='home'),
    path('hackathon', webviews.hackathon, name='hackathon'),
    path('id', webviews.home_id, name='home_id'),
]