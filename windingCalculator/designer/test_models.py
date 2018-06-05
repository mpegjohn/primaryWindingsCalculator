# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Wire
from .models import Winding
import math



class WireTestClass(TestCase):

    def setUp(self):
        Wire.objects.create(diameter=1.0, grade_1_dia_max=1, grade_2_dia_max=2)

    def test_calc_resistance_per_m(self):
        wire = Wire.objects.get(id=1)
        self.assertAlmostEqual(wire.calc_resistance_per_m(), 0.02176, 2)

    def test_calc_resistance(self):
        wire = Wire.objects.get(id=1)
        self.assertAlmostEqual(wire.calc_resistance(10), 0.02176*10, 2)

    def test_calc_mass_per_m(self):
        wire = Wire.objects.get(id=1)
        self.assertAlmostEqual(wire.calc_mass_per_m(), 6.982, 2)

    def test_calc_mass(self):
        wire = Wire.objects.get(id=1)
        self.assertAlmostEqual(wire.calc_mass(10), 6.982 * 10, 2)

class WindingTestClass(TestCase):

    def setUp(self):
        Wire.objects.create(diameter=1.0, grade_1_dia_max=1, grade_2_dia_max=2)
        Wire.objects.create(diameter=0.25, grade_1_dia_max=0.27, grade_2_dia_max=0.297)
        wire = Wire.objects.get(diameter=0.25)
        Winding.objects.create(turns=1318, taps= "", wire = wire, wire_grade=2, winding_number=1, layers=25, turns_per_layer=25)
        wire = Wire.objects.get(diameter=1.0)
        Winding.objects.create(turns=1, taps= "", wire = wire, wire_grade=2, winding_number=1, layers=1, turns_per_layer=10)

    def test_winding_height(self):
        winding = Winding.objects.get(id=1)
        self.assertEqual(winding.calc_winding_height(), 7.425)

    def test_mlt_at_the_core(self):
        winding = Winding.objects.get(id=2)
        winding.calc_mean_length_turn(toungue_width=10, stack_depth=10, distance_from_core=0)
        self.assertAlmostEqual(winding.mlt, 40 + (2 * math.pi), delta=0.01)

    def test_mlt_offset(self):
        winding = Winding.objects.get(id=2)
        winding.calc_mean_length_turn(toungue_width=10, stack_depth=10, distance_from_core=2)
        self.assertAlmostEqual(winding.mlt, 40 + (6 * math.pi), delta=0.01)

    def test_mlt_wire_grade(self):
        winding = Winding.objects.get(id=2)
        winding.wire_grade = 1
        winding.calc_mean_length_turn(toungue_width=10, stack_depth=10, distance_from_core=2)
        self.assertAlmostEqual(winding.mlt, 40 + (5 * math.pi), delta=0.01)

    def test_mlt_complex(self):
        winding = Winding.objects.get(id=1)
        mlt = winding.calc_mean_length_turn(toungue_width=25.4, stack_depth=25.4, distance_from_core=1.143)
        self.assertAlmostEqual(winding.mlt, 132.11, delta=0.01)

    def test_calc_length_same_as_mlt(self):
        winding = Winding.objects.get(id=2)
        winding.calc_mean_length_turn(toungue_width=10, stack_depth=10, distance_from_core=2)
        self.assertAlmostEqual(winding.calc_length_m(), (40 + (5 * math.pi))/1000.0, delta=0.01)

    def test_calc_resistance(self):
        winding = Winding.objects.get(id=2)
        winding.turns = 1000
        winding.calc_mean_length_turn(toungue_width=10, stack_depth=10, distance_from_core=2)
        self.assertAlmostEqual(winding.calc_resistance(), winding.calc_length_m() * 0.02176, 1)

