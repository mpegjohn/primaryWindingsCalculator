# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. You're at the designer index.")

from .models import Wire
from .forms import WireSizeForm

def index(request):



    #wire = Wire.objects.get(id=1)
    #return HttpResponse(wire.diameter)

    wire_list = Wire.objects.all()

    context = {'wire_list': wire_list}
    return render(request, 'designer/index.html', context)



def wire_size(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WireSizeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/designer/wire/')

    # if a GET (or any other method) we'll create a blank form
    form = WireSizeForm()
    return render(request, 'designer/wire_size.html', {'form': form})

