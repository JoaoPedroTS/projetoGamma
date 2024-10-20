from django import forms
from .models import Batch, Supplier, Protocol, Shaping

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "batch_name",
            "batch_shaping",
            "batch_shaping",
            "batch_maternity",
            "batch_size"
        ]
        
        labels = {
            "batch_name": "Nome do lote",
            "batch_shaping": "Composição do lote",
            "batch_maternity": "Sexo",
            "batch_size": "Tamanho do lote"
        }

        widgets = {
            "batch_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "batch_shaping": forms.Select(attrs={
                'class': 'form-select'
            }),

            "batch_maternity": forms.Select(attrs={
                "class": "form-select"
            }),
            
            "batch_size": forms.NumberInput(attrs={
                "class": "form-control"
            })
        }

class EditBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            "batch_name",
            "batch_size",
            "positive_quant",
            "negative_quant",
            "uncertainty_quant"
        ]

        labels = {
            "batch_name": "Nome do lote",
            "batch_size": "Tamanho do lote",
            "positive_quant": "Positivas",
            "negative_quant": "Negativas",
            "uncertainty_quant": "Retorno"
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
            "uncertainty_quant"
        ]

        labels = {
            "positive_quant": "Positivas",
            "negative_quant": "Negatvas",
            "uncertainty_quant": "Retorno"
        }

        widgets = {
            "positive_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            
            "negative_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "uncertainty_quant": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

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