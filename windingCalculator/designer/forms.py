from django import forms
from .models import Lamination
from .models import Core
from .models import Bobbin

class WireSizeForm(forms.Form):
    currentDensity = forms.FloatField(label="Current density in A/m^2", help_text="Enter the desired current density")
    length = forms.FloatField(label="Length in m", help_text="Enter the length in metres")

class LamForm(forms.Form):
    name = forms.CharField(max_length=20, label="Lamination name")
    tongue_width = forms.FloatField(label="Tongue width in mm")

class CoreForm(forms.Form):
    name = forms.CharField(max_length=20, label="Core name")
    stack = forms.FloatField(label="Stack depth in mm")
    stack_factor = forms.FloatField(label="Stacking factor", initial=0.92)
    lamination = forms.ModelChoiceField(queryset=Lamination.objects.all())

class BobbinForm(forms.Form):
    name = forms.CharField(max_length=20, label="Bobbin name")
    core = forms.ModelChoiceField(queryset=Core.objects.all())
    type = forms.ChoiceField(choices=Bobbin.TYPES)
    section_winding_length = forms.FloatField()
    section_winding_depth = forms.FloatField()
    meterial_thickness = forms.FloatField()
    has_terminals = forms.BooleanField(initial=True)
    number_terminals = forms.IntegerField(initial=18)