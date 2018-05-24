# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import math

# Create your models here.

class Wire(models.Model):
    diameter = models.FloatField()
    grade_1_dia_max = models.FloatField()
    grade_2_dia_max = models.FloatField()

    def calc_resistance_per_m(self):
        return 0.017241/(math.pi*(self.diameter/2) ** 2)
        
    def calc_resistance(self, length):
        return  self.calc_resistance_per_m() * length

    def calc_weight_per_m(self):
        return (math.pi*(self.diameter/2) ** 2) * 8.89

    def calc_weight(self, length):
        return self.calc_weight_per_m() * length

    def calc_current_capacity(self, current_density):
        return self.calc_area() * current_density

    def calc_cost(self, length, price_per_kg):
        return self.weight(length) * price_per_kg/1000

    def calc_area(self):
        return math.pi * ((self.diameter/2.0) ** 2)

    def __str__(self):
        return str(self.diameter)

class Winding(models.Model):
    turns = models.IntegerField()
    layers = models.IntegerField()
    turns_per_layer = models.IntegerField()
    wire = models.ForeignKey(Wire)

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

    def calc_weight(self):
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

    winding = models.ForeignKey(Winding)
    bobbin = models.ForeignKey(Bobbin)

    target_inductance = models.FloatField()
    current_density = models.FloatField()

    dc_current = models.FloatField()
    ac_voltage = models.FloatField()




    def resistance(self):
        return self.wire.resistance(self.mean_length_turns * self.turns)
