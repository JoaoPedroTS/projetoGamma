from django.db import models
from farm.models import Farm
from season.models import Season

# Create your models here.
class Supplier(models.Model):
    def __str__(self):
        return self.supplier_acronym

    supplier_name = models.CharField(max_length=100)
    supplier_acronym = models.CharField(max_length=4)

    def save(self, *args, **kwargs):
        if self.supplier_acronym:
            self.supplier_acronym = self.supplier_acronym.upper()
        super().save(*args, **kwargs)

class Protocol(models.Model):
    def __str__(self):
        return self.protocol_acronym
    
    class BinaryChoice(models.TextChoices):
        SIM = "S", "Sim"
        NAO = "N", "Não"
    
    protocol_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="protocols")
    protocol_duration = models.IntegerField()
    gnrh = models.CharField(
        max_length=1,
        choices=BinaryChoice.choices,
        default=BinaryChoice.NAO,
    )
    presync = models.CharField(
        max_length=1,
        choices=BinaryChoice.choices,
        default=BinaryChoice.NAO,
    )
    protocol_acronym = models.CharField(max_length=50, default="", blank=True)

    def save(self, *args, **kwargs):
        self.protocol_acronym = f"{self.protocol_supplier} - {self.protocol_duration} - G{self.gnrh} - PS{self.presync}"
        super().save(*args, **kwargs)
    

class Shaping(models.Model):
    def __str__(self):
        return self.shaping_acronym
    
    shaping_name = models.CharField(max_length=100)
    shaping_acronym = models.CharField(max_length=4)

    def save(self, *args, **kwargs):
        # Transforma o farm_acronym em letras maiúsculas antes de salvar
        if self.shaping_acronym:
            self.shaping_acronym = self.shaping_acronym.upper()
        super().save(*args, **kwargs)

class Batch(models.Model):
    def __str__(self):
        return self.batch_name
    
    class Choices(models.TextChoices):
        SIM = "M", "Macho"
        NAO = "F", "Fêmea"
        MIX = "H", "Heterogêneo"
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="batches")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="batches")
    batch_name = models.CharField(max_length=200)
    prior_batch = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='derivative')
    batch_shaping = models.ForeignKey(Shaping, on_delete=models.CASCADE, related_name="batches", default=None)
    batch_maternity = models.CharField(
        max_length=1,
        choices=Choices.choices
    )
    batch_size = models.IntegerField()
    negative_quant = models.IntegerField(default=0)
    positive_quant = models.IntegerField(default=0)
    uncertainty_quant = models.IntegerField(default=0)
    batch_acronym = models.CharField(max_length=50, default="", blank=True)

    def save(self, *args, **kwargs):
        self.batch_acronym = f"{self.batch_name} - {self.batch_shaping} - {self.batch_maternity}"
        super().save(*args, **kwargs)