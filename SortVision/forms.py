from django import forms
from .models import PunktacjaJury, PunktacjaWidzowie

class PunktacjaJuryForm(forms.ModelForm):
    class Meta:
        model = PunktacjaJury
        fields = ['przyznajacy_kraj', 'kraj', 'punkty']

class PunktacjaWidzowieForm(forms.ModelForm):
    class Meta:
        model = PunktacjaWidzowie
        fields = ['kraj', 'punkty']
