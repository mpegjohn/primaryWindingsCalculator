# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Wire
from .models import Winding

class WindingTestClass(TestCase):

    def setUp(self):
        Wire.objects.create(diameter=1.0, grade_1_dia_max=1.2, grade_2_dia_max=1.5)
        Wire.objects.create(diameter=0.25, grade_1_dia_max=0.27, grade_2_dia_max=0.297)



    def test_winding(self):

        wire = Wire.objects.get(diameter=0.25)

        winding = Winding()
        winding.wire = wire
        winding.wire_grade = 2
        winding.turns = 1318
        winding.taps = ""
        winding.winding_number = 1
        winding.turns_per_layer = 53

        winding.layers = 25

        self.assertEqual(winding.calc_winding_height(), 7.425)

        mlt = winding.calc_mean_length_turn(toungue_width=25.4, stack_depth=25.4, distance_from_core=1.143)
        self.assertAlmostEqual(mlt, 132.11, delta=0.01)
        self.assertAlmostEqual(winding.mlt, 132.11, delta=0.01)

        winding.save()

        wind = Winding.objects.get(id=1)

        self.assertEqual(wind.calc_winding_height(), 7.425)

