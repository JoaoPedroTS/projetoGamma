import django_tables2 as tables
from .models import Batch

class BatchTable(tables.Table):
    class Meta:
        model = Batch
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'batch_name',
            'animal_type',
            'batch_size',
            'positive_quant',
            'negative_quant'
        )