from django import forms
from .models import PunktacjaJury, PunktacjaWidzowie, Kraj, Polfinal

class PunktacjaJuryForm(forms.ModelForm):
    class Meta:
        model = PunktacjaJury
        fields = ['kraj', 'przyznajacy_kraj', 'punkty']

class PunktacjaWidzowieForm(forms.ModelForm):
    class Meta:
        model = PunktacjaWidzowie
        fields = ['kraj', 'punkty']
class ListaForm(forms.ModelForm):

    class Meta:
        model = Kraj
        fields = ['nazwa','zdjecie']


class PolfinalForm(forms.ModelForm):

    class Meta:
        model = Polfinal
        fields = ['kraj']