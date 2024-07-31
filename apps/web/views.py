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


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class CustomAdminLoginView(View):
    template_name = 'admin/custom_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin:index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, self.template_name)