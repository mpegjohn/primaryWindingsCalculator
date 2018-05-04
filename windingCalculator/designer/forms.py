from django import forms

class WireSizeForm(forms.Form):
    currentDensity = forms.FloatField(label="Current density in A/m^2", help_text="Enter the desired current density")
    length = forms.FloatField(label="Length in m", help_text="Enter the length in metres")

class LamForm(forms.Form):
    size = forms.CharField(max_length=20, label="Lamination size", help_text="The name or pattern number")
    tongue_width = forms.FloatField(label="Toungue width in mm", help_text="Tongue width in mm")
