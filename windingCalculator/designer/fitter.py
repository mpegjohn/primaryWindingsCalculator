from .models import Wire
from .models import Bobbin
import math


class Fitter(object):

    def __init__(self, bobbin, wire, grade, turns, fit_factor=0.97, max_fill=0.85):
        self.bobbin = bobbin
        self.wire = wire
        self.grade = grade
        self.turns = turns
        self.fit_factor = fit_factor
        self.max_fill = max_fill

    def calc_fit(self):
        winding_width = self.bobbin.section_winding_length * self.fit_factor
        winding_height = self.bobbin.section_winding_depth * self.max_fill

        diameter = self.wire.grade_2_dia_max
        if self.grade == 1:
            diameter = self.wire.grade_1_dia_max

        self.turns_per_layer = int(winding_width / diameter)
        self.layers = math.ceil(self.turns/self.turns_per_layer)

        self.height = self.layers * diameter

        if self.height > self.winding_height:
            return False
        return True




