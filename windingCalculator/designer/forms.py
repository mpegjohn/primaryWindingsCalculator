from django import forms
from .models import Lamination

class WireSizeForm(forms.Form):
    currentDensity = forms.FloatField(label="Current density in A/m^2", help_text="Enter the desired current density")
    length = forms.FloatField(label="Length in m", help_text="Enter the length in metres")

class LamForm(forms.ModelForm):
    class Meta:
        model = Lamination
        fields = ('lam_size', 'tongue_width')
