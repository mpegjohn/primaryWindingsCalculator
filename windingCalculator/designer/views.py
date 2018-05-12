# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. You're at the designer index.")

from .models import Wire
from .forms import WireSizeForm
from .models import Lamination
from .forms import  LamForm
from .models import Core
from .forms import CoreForm
from .models import Bobbin
from .forms import BobbinForm

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

    form = LamForm()

    if request.method == 'POST':
        form = LamForm(request.POST)

        if form.is_valid():
            lamination = Lamination(name=form.cleaned_data['name'], tongue_width =form.cleaned_data['tongue_width'])
            lamination.save()

    for lamination in laminations:
        lamination.width = lamination.calc_width()
        lamination.height = lamination.calc_height()
        lamination.window_height = lamination.calc_window_height()
        lamination.window_width = lamination.calc_window_width()
        lamination.mag_path = lamination.calc_path_length()
        lamination.window_area = lamination.calc_window_area()

    context = {'laminations':laminations, 'form':form}

    return render(request, 'designer/laminations.html', context)

def edit_lamination(request, id):
    lamination = Lamination.objects.get(id=id)

    form = LamForm(initial={'name':lamination.name, 'tongue_width': lamination.tongue_width})

    context = {'lamination' :lamination, 'form': form}
    return render(request, 'designer/edit_lamination.html', context)

def update_lamination(request, id):
    form = LamForm(request.POST)

    if form.is_valid():
        lamination = Lamination.objects.get(id=id)
        lamination.name = form.cleaned_data['name']
        lamination.tongue_width = form.cleaned_data['tongue_width']
        lamination.save()
    return redirect('laminations')

def delete_lamination(request, id):

    lamination = Lamination.objects.get(id=id)
    lamination.delete()
    return redirect('laminations')

def cores(request):
    core_list = Core.objects.all()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CoreForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            name = form.cleaned_data['name']
            stack = form.cleaned_data['stack']
            stack_factor = form.cleaned_data['stack_factor']
            lamination = form.cleaned_data['lamination']

            core = Core(name=name, stack=stack, stack_factor=stack_factor, laminations=lamination)
            core.save()

            for core in core_list:
                core.area = core.calc_area()
                core.weight = core.calc_weight()

            context = {'form': form, 'core_list': core_list}

            return render(request, 'designer/core.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = CoreForm()

        for core in core_list:
            core.area = core.calc_area()
            core.weight = core.calc_weight()

        context = {'form': form, 'core_list': core_list}

    return render(request, 'designer/core.html', context)

def edit_cores(request, id):
    core = Core.objects.get(id=id)

    form = CoreForm(initial={'name':core.name, 'stack': core.stack, 'stack_factor': core.stack_factor, 'lamination': core.laminations})

    context = {'form': form, 'core': core}
    return render(request, 'designer/edit_cores.html', context)

def update_cores(request, id):
    form = CoreForm(request.POST)

    if form.is_valid():
        core = Core.objects.get(id=id)
        core.name = form.cleaned_data['name']
        core.stack = form.cleaned_data['stack']
        core.stack_factor = form.cleaned_data['stack_factor']
        core.laminations = form.cleaned_data['lamination']
        core.save()

    return redirect('cores')

def delete_cores(request, id):
    core = Core.objects.get(id=id)
    core.delete()
    return redirect('cores')

def inductor(request):
    context = {}

    return render(request, 'designer/inductor.html', context)


def bobbins(request):
    bobbin_list = Bobbin.objects.all()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BobbinForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            core = form.cleaned_data['core']
            type = form.cleaned_data['type']
            section_winding_length = form.cleaned_data['section_winding_length']
            section_winding_depth = form.cleaned_data['section_winding_depth']
            meterial_thickness = form.cleaned_data['meterial_thickness']

            bobbin = Bobbin(name=name, core=core, type=type,
                            section_winding_length=section_winding_length,
                            section_winding_depth=section_winding_depth,
                            meterial_thickness=meterial_thickness)

            bobbin.save()

            context = {'form': form, 'bobbin_list': bobbin_list}

            return render(request, 'designer/bobbin.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = BobbinForm()

        context = {'form': form, 'bobbin_list': bobbin_list}

    return render(request, 'designer/bobbin.html', context)
