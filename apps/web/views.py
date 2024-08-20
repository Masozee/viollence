from django.shortcuts import render, get_object_or_404
from .models import *
# Create your views here.


def index(request):
    regions = Regions.objects.all()
    return render(request, 'index.html', {'regions': regions})


def home(request):
    return render(request, "old/map.html", )


def hackathon(request):
    return render(request, "old/hackathon.html", )


def home_id(request):
    return render(request, "old/index_id.html", )

