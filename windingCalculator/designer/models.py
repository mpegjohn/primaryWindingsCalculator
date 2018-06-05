# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_comma_separated_integer_list
import math

# Create your models here.

class Wire(models.Model):
    diameter = models.FloatField()
    grade_1_dia_max = models.FloatField()
    grade_2_dia_max = models.FloatField()

    def calc_resistance_per_m(self):
        return 0.017241/self.calc_area()
        
    def calc_resistance(self, length):
        return  self.calc_resistance_per_m() * length

    def calc_mass_per_m(self):
        return self.calc_area() * 8.89

    def calc_mass(self, length):
        return self.calc_mass_per_m() * length

    def calc_current_capacity(self, current_density):
        return self.calc_area() * current_density

    def calc_cost(self, length, price_per_kg):
        return self.calc_mass(length) * price_per_kg/1000

    def calc_area(self):
        return math.pi * ((self.diameter/2.0) ** 2)

    def __str__(self):
        return str(self.diameter)

class Winding(models.Model):
    turns = models.IntegerField()
    taps = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    winding_number = models.IntegerField()
    layers = models.IntegerField()
    turns_per_layer = models.IntegerField()
    wire = models.ForeignKey(Wire)
    wire_grade = models.IntegerField()

    def calc_winding_height(self):
        if self.wire_grade == 1:
            wire_diameter = self.wire.grade_1_dia_max
        else:
            wire_diameter = self.wire.grade_2_dia_max

        return (self.layers * wire_diameter)

    def calc_mean_length_turn(self, toungue_width, stack_depth, distance_from_core):
        mlt = 2 * (toungue_width + stack_depth) + math.pi * ((2 * distance_from_core) + self.calc_winding_height())
        self.mlt = mlt

        return mlt

    def calc_length_m(self):
        mlt = self.mlt
        length_m = mlt * self.turns/1000.0

        return length_m

    def calc_resistance(self):
        resistance = self.wire.calc_resistance(self.calc_length_m())

        return  resistance

    def calc_mass(self):
        mass_kg = self.calc_length_m() * self.wire.calc_mass_per_m()/1000.0
        mass_kg = self.wire.calc_mass(self.calc_length_m())
        return  mass_kg

    def calc_vold_drop(self, current):
        volts = self.calc_resistance() * current
        return volts

    def calc_watts(self, current):
        wats = (current ** 2) * self.calc_resistance()
        return wats

    def calc_cost(self, cost_per_kg):
        cost = self.calc_weight() * cost_per_kg
        return cost


class Steel(models.Model):
    name = models.CharField(max_length=100, default='M6 x 0.35')
    supplier = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, default='M6')
    thickness = models.FloatField(default=0.35)
    gapped_permeability = models.FloatField(default=1000.0)

    def __str__(self):
        return self.name

class general_properties(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()

class Lamination(models.Model):
    name = models.CharField(max_length=20)

    tongue_width = models.FloatField()

    def calc_path_length(self):
        return self.tongue_width * 5.6

    def calc_width(self):
        return self.tongue_width *3.0

    def calc_height(self):
        return  self.tongue_width * 2.5

    def calc_window_height(self):
        return self.tongue_width * 1.5

    def calc_window_width(self):
        return  self.tongue_width * 0.5

    def calc_window_area(self):
        return self.calc_window_height() * self.calc_window_width()

    def __str__(self):
        return self.name

class Core(models.Model):
    name = models.CharField(max_length=100, default="")
    laminations = models.ForeignKey(Lamination)
    stack = models.FloatField()
    stack_factor = models.FloatField(default=0.92)

    def calc_area(self):
        return self.laminations.tongue_width * self.stack

    def calc_cubic_cm(self):
       return (6 * ((self.laminations.tongue_width/10.0) ) ** 2) * self.stack/10.0

    def calc_mass(self):
        return self.calc_cubic_cm() * .0078 * self.stack_factor

    def __str__(self):
        return self.name

class Bobbin(models.Model):
    TYPES = (
        ('SS', 'SS'),
        ('DS', 'DS'),
        ('SDS', 'SDS'),
    )

    name = models.CharField(max_length=100)
    core = models.ForeignKey(Core)
    type = models.CharField(max_length=100, choices=TYPES)
    section_winding_length = models.FloatField()
    section_winding_depth  = models.FloatField()
    meterial_thickness = models.FloatField()
    number_terminals = models.IntegerField(default=18)

    def __str__(self):
        return self.name

class Inductor(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100)

    windings = models.ManyToManyField(Winding)
    bobbin = models.ForeignKey(Bobbin)
    steel = models.ForeignKey(Steel)
    total_gap = models.FloatField()

    target_inductance = models.FloatField()
    current_density = models.FloatField()

    dc_current = models.FloatField()
    ac_voltage = models.FloatField()


    def calc_turns(self):
        mag_path_length = self.bobbin.core.laminations.calc_path_length()

        area = self.bobbin.core.calc_area()

        permeability = self.steel.gapped_permeability

        mu_0 = 4 * math.pi * 1e-10  # mu_0 in mm

        turns = math.sqrt((self.target_inductance * (self.total_gap + mag_path_length / permeability)) / (mu_0 * area))

        return turns

