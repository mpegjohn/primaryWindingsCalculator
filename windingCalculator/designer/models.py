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

class Winding(models.Model):
    turns = models.IntegerField()
    layers = models.IntegerField()
    turns_per_layer = models.IntegerField()
    wire = models.ForeignKey(Wire)

class steel(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    thickness =models.FloatField()

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

class Core(models.Model):
    laminations = models.ForeignKey(Lamination)
    steel = models.ForeignKey(steel)
    stack = models.FloatField()

class Inductor(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100)

    winding = models.ForeignKey(Winding)
    core = models.ForeignKey(Core)

    target_inductance = models.FloatField()
    current_density = models.FloatField()

    dc_current = models.FloatField()
    ac_voltage = models.FloatField()




    def resistance(self):
        return self.wire.resistance(self.mean_length_turns * self.turns)
