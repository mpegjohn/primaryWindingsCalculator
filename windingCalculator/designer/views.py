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
from .models import Lamination



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

            cd = form.cleaned_data['currentDensity']
            length = form.cleaned_data['length']

            for wire in wire_list:
                wire.area = wire.calc_area()
                wire.resistance_per_m = wire.calc_resistance_per_m()
                wire.current_capacity = wire.calc_current_capacity(cd)
                wire.resistance = wire.calc_resistance(length)
                wire.weight_per_m = wire.calc_weight_per_m()
                wire.weight = wire.calc_weight(length)

            context = {'form': form, 'wire_list': wire_list, 'density': cd, 'length': length}

            return render(request, 'designer/wire_size.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = WireSizeForm()

        for wire in wire_list:
            wire.area = wire.calc_area()
            wire.resistance_per_m = wire.calc_resistance_per_m()
            wire.current_capacity = wire.calc_current_capacity(3.0)
            wire.resistance = wire.calc_resistance(1.0)
            wire.weight_per_m = wire.calc_weight_per_m()
            wire.weight = wire.calc_weight(1.0)

        context = {'form': form, 'wire_list': wire_list, 'density': 3.0, 'length': 1.0}

        return render(request, 'designer/wire_size.html', context)

def laminations(request):

    laminations = Lamination.objects.all()

    for lamination in laminations:
        lamination.width = lamination.calc_width()
        lamination.height = lamination.calc_height()
        lamination.window_height = lamination.calc_window_height()
        lamination.window_width = lamination.calc_window_width()
        lamination.window_area = lamination.calc_window_area()

    context = {'laminations':laminations}

    return render(request, 'designer/laminations.html', context)

def inductor(request):



    context = {}

    return render(request, 'designer/inductor.html', context)

