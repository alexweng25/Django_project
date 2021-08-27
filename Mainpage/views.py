from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.


def index(request):
    return render(request, 'Mainpage.html', {'current_time': datetime.now()})
