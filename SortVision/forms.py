from django import forms
from .models import Kraj, Polfinal

class ListaForm(forms.ModelForm):

    class Meta:
        model = Kraj
        fields = ['nazwa','zdjecie']


class PolfinalForm(forms.ModelForm):

    class Meta:
        model = Polfinal
        fields = ['kraj']


class JuryGlosowanieForm(forms.Form):
    def __init__(self, kraje, current_kraj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(kraj.id, kraj.nazwa) for kraj in kraje if kraj != current_kraj]
        choices.insert(0, ('', '--- Wybierz kraj ---'))

        self.fields['points_1'] = forms.ChoiceField(choices=choices, label="1 pkt")
        self.fields['points_2'] = forms.ChoiceField(choices=choices, label="2 pkt")
        self.fields['points_3'] = forms.ChoiceField(choices=choices, label="3 pkt")
        self.fields['points_4'] = forms.ChoiceField(choices=choices, label="4 pkt")
        self.fields['points_5'] = forms.ChoiceField(choices=choices, label="5 pkt")
        self.fields['points_6'] = forms.ChoiceField(choices=choices, label="6 pkt")
        self.fields['points_7'] = forms.ChoiceField(choices=choices, label="7 pkt")
        self.fields['points_8'] = forms.ChoiceField(choices=choices, label="8 pkt")
        self.fields['points_10'] = forms.ChoiceField(choices=choices, label="10 pkt")
        self.fields['points_12'] = forms.ChoiceField(choices=choices, label="12 pkt")

    def clean(self):
        cleaned_data = super().clean()
        for name, value in cleaned_data.items():
            if not value:
                raise forms.ValidationError("Wybierz kraj dla każdej opcji punktowej.")
        return cleaned_data