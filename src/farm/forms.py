from django import forms
from .models import Farm

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = [
            "farm_name",
            "farm_acronym",
            # "farm_brand",
            "farm_owner",
            "farm_location",
        ]

        labels = {
            "farm_name": "Nome",
            "farm_acronym": "Sigla",
            # "farm_brand": "Logomarca",
            "farm_owner": "Proprietário",
            "farm_location": "Localidade",
        }

        widgets = {
            "farm_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "farm_acronym": forms.TextInput(attrs={
                "class": "form-control"
            }),
            # "farm_brand",
            "farm_owner": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "farm_location": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }