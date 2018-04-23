from django import forms

class WireSizeForm(forms.Form):
    currentDensity = forms.FloatField(label="Current density in A/m^2", help_text="Enter the desired current density")

