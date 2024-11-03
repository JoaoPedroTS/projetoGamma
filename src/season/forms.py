from django import forms
from .models import Season

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = [
            "season_name",
            "begin_date",
            "end_date",
            "farms"
        ]

        labels = {
            "season_name": "Nome",
            "begin_date": "Data de início",
            "end_date": "Data final",
            "farms": "Fazendas nessa estação"
        }

        widgets = {
            "season_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "begin_date": forms.DateInput(attrs={
                "class": "form-control",
                "placeholder": "dd/mm/AAAA"
            }, format="%d/%m/%Y"),

            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "placeholder": "dd/mm/AAAA"
            }, format="%d/%m/%Y"),

            "farms": forms.CheckboxSelectMultiple(attrs={
                "class": "checkbox-select-multiple"
            })
        }

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.fields["begin_date"].input_formats = ["%d/%m/%Y"]
            self.fields["end_date"].input_formats = ["%d/%m/%Y"]

            for checkbox in self.fields["farms"].widget.choices:
                checkbox[1].widget.attrs.update({"class": "form-check-input"})

class AppendFarmForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = [
            "farms"
        ]

        labels = {
            "farms": "Fazendas nessa estação"
        }

        widgets = {
            "farms": forms.CheckboxSelectMultiple(attrs={
                "class": "checkbox-select-multiple"
            })
        }