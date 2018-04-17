# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import math

# Create your models here.

class Wire(models.Model):
    diameter = models.FloatField()
    grade_1_dia_max = models.FloatField()
    grade_2_dia_max = models.FloatField()

    def resistance_per_m(self):
        return 0.017241/(math.pi*(self.diameter/2)^2)
        
    def resistance(self, length):
        return  self.resistance_per_m() * length

    def weight_per_m(self):
        return (math.pi*(self.diameter/2)^2) * 8.89

    def weight(self, length):
        return self.weight_per_m() * length

    def cost(self, length, price_per_kg):
	return self.weight(length) * price_per_kg/1000

class Winding(models.Model):
    turns = models.IntegerField()
    layers = models.IntegerField()
    turns_per_layer = models.IntegerField()
    wire = models.ForeignKey(Wire)
    voltage = models.FloatField()
    current = models.FloatField()
    mean_length_turns = models.FloatField()

    def resistance(self):
        return self.wire.resistance(self.mean_length_turns * self.turns)


class Lamination(models.Model):
    lam_size = models.CharField(max_length=20)
    measure_A = models.FloatField()
    measure_B = models.FloatField()
    measure_C = models.FloatField()
    measure_D = models.FloatField()
    measure_E = models.FloatField()
    measure_F = models.FloatField()
    measure_G = models.FloatField()
    path_length = models.FloatField()
    window_area = models.FloatField()


