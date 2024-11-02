from django import forms
from .models import Batch, Supplier, Protocol, Shaping

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "batch_name",
            "batch_shaping",
            "protocol",
            "batch_maternity",
            "batch_size",
            "d0_date",
            "rating"
        ]
        
        labels = {
            "batch_name": "Nome do lote",
            "batch_shaping": "Composição do lote",
            "protocol": "Protocolo",
            "batch_maternity": "Sexo",
            "batch_size": "Tamanho do lote",
            "d0_date": "Data D-0",
            "rating": "Escore"
        }

        widgets = {
            "batch_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "batch_shaping": forms.Select(attrs={
                'class': 'form-select'
            }),
            "protocol": forms.Select(attrs={
                'class': 'form-select'
            }),
            "batch_maternity": forms.RadioSelect(attrs={
                "class": "form-check-input form-check-inline"
            }),
            
            "batch_size": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "d0_date": forms.DateInput(attrs={
                "class": "form-control",
                "placeholder": "dd-mm-yyyy"
            }, format='%d-%m-%Y'),

            "rating": forms.RadioSelect(attrs={
                "class": "form-check-input form-check-inline"
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        self.fields['rating'].choices = Batch.RATING_CHOICES
        self.fields['batch_maternity'].choices = Batch.Choices.choices
        # Remover o espaço reservado
        self.fields['rating'].empty_label = None
        self.fields['batch_maternity'].empty_label = None

class EditBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "batch_name",
            "batch_size",
            "positive_quant",
            "negative_quant",
            "recurrence_quant",
            "uncertainty_quant"
        ]

        labels = {
            "batch_name": "Nome do lote",
            "batch_size": "Tamanho do lote",
            "positive_quant": "Positivas",
            "negative_quant": "Negativas",
            "recurrence_quant": "Retorno",
            "uncertainty_quant": "Dúvida"
        }

        widgets = {
            "batch_name": forms.TextInput(attrs={
                "class": "form-control"
            }),            
            "batch_size": forms.NumberInput(attrs={
                "class": "form-control"
            }),            
            "positive_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),            
            "negative_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),            
            "recurrence_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "uncertainty_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

class WorkDayForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "positive_quant",
            "negative_quant",
            "recurrence_quant",
            "uncertainty_quant",
            "dg_date"
        ]

        labels = {
            "positive_quant": "Positivas",
            "negative_quant": "Negatvas",
            "recurrence_quant": "Retorno",
            "uncertainty_quant": "Duvida",
            "dg_date": "Data do serviço"
        }

        widgets = {
            "positive_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            
            "negative_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "recurrence_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "uncertainty_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "dg_date": forms.DateInput(attrs={
                "class": "form-control datepicker",
                "placeholder": "dd-mm-yyyy"
            }, format=['%d-%m-%Y', "%d/%m/%Y"]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dg_date'].input_formats = ['%d-%m-%Y']

    def save(self, commit=True, work_day=False):
        instance = super().save(commit=False)
        instance.work_day = work_day
        if commit:
            instance.save()
        return instance
    
class SupplierForm(forms.ModelForm):
    class Meta: 
        model = Supplier
        
        fields = [
            "supplier_name",
            "supplier_acronym"
        ]

        labels = {
            "supplier_name": "Nome",
            "supplier_acronym": "Sigla"
        }

        widgets = {
            "supplier_name": forms.TextInput(attrs={
                'class': 'form-control'
            }),
            
            "supplier_acronym": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }

class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol

        fields = [
            "protocol_supplier",
            "protocol_duration",
            "gnrh",
            "presync"
        ]

        labels = {
            "protocol_supplier": "Fornecedor",
            "protocol_duration": "Duração",
            "gnrh": "GNRH",
            "presync": "PRÉ-SYNC"
        }

        widgets = {
            "protocol_supplier": forms.Select(attrs={
                'class': 'form-select'
            }),

            "protocol_duration": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "gnrh": forms.Select(attrs={
                "class": "form-select"
            }),
            
            "presync": forms.Select(attrs={
                "class": "form-select"
            }),
        }

class ShapingForm(forms.ModelForm):
    class Meta:
        model = Shaping

        fields = [
            "shaping_name",
            "shaping_acronym"
        ]

        labels = {
            "shaping_name": "Nome",
            "shaping_acronym": "Sigla"
        }

        widgets = {
            "shaping_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            
            "shaping_acronym": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }

class UncertaintyForm(forms.ModelForm):
    class Meta:
        model = Batch

        fields = [
            "positive_quant",
            "negative_quant"
        ]

        labels = {
            "positive_quant": "Positivas",
            "negative_quant": "Negativas"
        }

        widgets = {
            "positive_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "negative_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            positive = cleaned_data.get("positive_quant", 0)
            negative = cleaned_data.get("negative_quant", 0)

            if (positive + negative) > self.instance.uncertainty_quant:
                raise forms.ValidationError("A soma dos valores não pode exceder o total de animais em dúvida.")

            return cleaned_data
        
class RecurrenceForm(forms.ModelForm):
    class Meta:
        model = Batch

        fields = [
            "recurrence_positive_quant",
            "recurrence_negative_quant"
        ]

        labels = {
            "recurrence_positive_quant": "Positivas",
            "recurrence_negative_quant": "Negativas"
        }

        widgets = {
            "recurrence_positive_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "recurrence_negative_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            positive = cleaned_data.get("recurrence_positive_quant", 0)
            negative = cleaned_data.get("recurrence_negative_quant", 0)

            if positive + negative > self.instance.recurrence_quant:
                raise forms.ValidationError("A soma dos valores não pode exceder o total dos animais em retorno")
            
            return cleaned_data
