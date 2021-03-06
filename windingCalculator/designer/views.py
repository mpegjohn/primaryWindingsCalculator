# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

import math

from .fitter import Fitter

from .models import Wire
from .forms import WireSizeForm
from .models import Lamination
from .forms import  LamForm
from .models import Core
from .forms import CoreForm
from .models import Bobbin
from .forms import BobbinForm
from .forms import InductorForm
from .forms import SteelForm
from .models import Steel
from .models import Inductor

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
                wire.mass_per_m = wire.calc_mass_per_m()
                wire.mass = wire.calc_mass(length)

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
            wire.mass_per_m = wire.calc_mass_per_m()
            wire.mass = wire.calc_mass(1.0)

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
                core.mass = core.calc_mass()

            context = {'form': form, 'core_list': core_list}

            return render(request, 'designer/core.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = CoreForm()

        for core in core_list:
            core.area = core.calc_area()
            core.mass = core.calc_mass()

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
            number_terminals = form.cleaned_data['number_terminals']

            bobbin = Bobbin(name=name, core=core, type=type,
                            section_winding_length=section_winding_length,
                            section_winding_depth=section_winding_depth,
                            meterial_thickness=meterial_thickness,
                            number_terminals=number_terminals
            )

            bobbin.save()

            context = {'form': form, 'bobbin_list': bobbin_list}

            return render(request, 'designer/bobbin.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = BobbinForm()

        context = {'form': form, 'bobbin_list': bobbin_list}

    return render(request, 'designer/bobbin.html', context)

def edit_bobbins(request, id):
    bobbin = Bobbin.objects.get(id=id)

    form = BobbinForm(initial={'name':bobbin.name, 'core':bobbin.core, 'type':bobbin.type,
                               'section_winding_length':bobbin.section_winding_length,
                      'section_winding_depth':bobbin.section_winding_depth,
                      'meterial_thickness':bobbin.meterial_thickness,
                      'number_terminals':bobbin.number_terminals}
                      )

    context = {'form': form, 'bobbin': bobbin}
    return render(request, 'designer/edit_bobbin.html', context)

def update_bobbins(request, id):
    form = BobbinForm(request.POST)

    if form.is_valid():
        bobbin = Bobbin.objects.get(id=id)
        bobbin.name = form.cleaned_data['name']
        bobbin.core = form.cleaned_data['core']
        bobbin.type = form.cleaned_data['type']
        bobbin.section_winding_length = form.cleaned_data['section_winding_length']
        bobbin.section_winding_depth = form.cleaned_data['section_winding_depth']
        bobbin.meterial_thickness = form.cleaned_data['material_thickness']
        bobbin.number_terminals = form.cleaned_data['number_terminals']
        bobbin.save()
        
    return redirect('bobbins')

def delete_bobbins(request, id):
    bobbin = Bobbin.objects.get(id=id)
    bobbin.delete()
    return redirect('bobbins')

def steel(request):
    steel_list = Steel.objects.all()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SteelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            supplier = form.cleaned_data['supplier']
            grade = form.cleaned_data['grade']
            thickness = form.cleaned_data['thickness']
            gapped_permeability = form.cleaned_data['gapped_permeability']

            steel = Steel(name=name, supplier=supplier, grade=grade, thickness=thickness, gapped_permeability=gapped_permeability)

            steel.save()

            context = {'form': form, 'steel_list': steel_list}

            return render(request, 'designer/steel.html', context)
    else:
        # if a GET (or any other method) we'll create a blank form

        form = SteelForm()

        context = {'form': form, 'steel_list': steel_list}

    return render(request, 'designer/steel.html', context)

def edit_steel(request, id):
    steel = Steel.objects.get(id=id)

    form = SteelForm(initial={'name':steel.name, 'supplier':steel.supplier, 'grade':steel.grade,
                               'thickness':steel.thickness,
                      'gapped_permeability':steel.gapped_permeability}
                      )

    context = {'form': form, 'steel': steel}
    return render(request, 'designer/edit_steel.html', context)


def update_steel(request, id):
    form = SteelForm(request.POST)

    if form.is_valid():
        steel = Steel.objects.get(id=id)
        steel.name = form.cleaned_data['name']
        steel.supplier = form.cleaned_data['supplier']
        steel.grade = form.cleaned_data['grade']
        steel.thickness = form.cleaned_data['thickness']
        steel.gapped_permeability = form.cleaned_data['gapped_permeability']
        steel.save()

    return redirect('steel')

def delete_steel(request, id):
    steel = Steel.objects.get(id=id)
    steel.delete()
    return redirect('steel')

def inductor(request):

    if request.method == 'POST':
        form = InductorForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            bobbin = form.cleaned_data['bobbin']
            inductance = form.cleaned_data['inductance']
            dc_current = form.cleaned_data['dc_current']
            initial_total_gap = form.cleaned_data['initial_total_gap']
            current_density = form.cleaned_data['current_density']
            steel = form.cleaned_data['steel']
            grade = form.cleaned_data['wire_grade']

            # Get the nearest wire size

            wires = Wire.objects.order_by('diameter')

            wire_to_use = None

            for wire in wires:
                # Find the first useable wire for this current density
                if wire.calc_current_capacity(current_density) >= dc_current:
                    wire_to_use = wire
                    break

            inductor = Inductor()

            inductor.bobbin = bobbin
            inductor.name = name
            inductor.target_inductance = inductance
            inductor.total_gap = initial_total_gap
            inductor.steel = steel

            turns = inductor.calc_turns()

            fitter = Fitter(bobbin, wire, grade, turns, 0.97, 0.95)
            fitter.calc_fit()
            


    else:
        form = InductorForm()
        context = {'form': form}

    return render(request, 'designer/inductor.html', context)