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
    wire_list = Wire.objects.all()

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

    else:
        # if a GET (or any other method) we'll create a blank form

        form = WireSizeForm()

        wire_data=[]

        for wire in wire_list:
            data = {'diameter': wire.diameter,
                 'grade_1_dia_max': wire.grade_1_dia_max,
                 'grade_2_dia_max': wire.grade_2_dia_max,
                 'current_capacity': wire.current_capacity(3.0),}
            wire_data.append(data)


        context = {'form': form, 'wire_list': wire_data, 'density' : 3.0}

        return render(request, 'designer/wire_size.html', context)

