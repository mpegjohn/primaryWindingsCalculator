from django import forms
from models import Lamination

class WireSizeForm(forms.Form):
    currentDensity = forms.FloatField(label="Current density in A/m^2", help_text="Enter the desired current density")
    length = forms.FloatField(label="Length in m", help_text="Enter the length in metres")

class LamForm(forms.Form):
    name = forms.CharField(max_length=20, label="Lamination name")
    tongue_width = forms.FloatField(label="Toungue width in mm")

class CoreForm(forms.Form):

    name = forms.CharField(max_length=20, label="Lamination name")

    lamination = forms.ModelChoiceField(queryset=Lamination.objects.all())