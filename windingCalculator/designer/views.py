# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. You're at the designer index.")

from .models import Wire

def index(request):
    wire_list = Wire.objects.all()
    context = {'wire_list': wire_list}
    return render(request, 'designer/index.html', context)
