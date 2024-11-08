from django.db import models
from farm.models import Farm
from season.models import Season
from django.contrib.auth.models import User
import datetime

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

class BirthMonth(models.Model):
    def __str__(self):
        return self.month
    
    month = models.CharField(max_length=3, choices=[(str(i), str(i)) for i in range(1, 13)] + [("N/A", "N/A")], unique=True)

class Batch(models.Model):
    def __str__(self):
        return self.batch_name
    
    class Choices(models.TextChoices):
        SIM = "M", "Macho"
        NAO = "F", "Fêmea"
        MIX = "H", "Heterogêneo"
        NA = "N/A", "N/A"

    class ShappingChoices(models.TextChoices):
        VS = "VS", "Vaca Solteira"
        VL = "VL", "Vaca leiteira"
        VP = "VP", "Vaca Parida"
        NN = "NN", "Novilha Normal"
        NP = "NP", "Novilha Precoce"

    RATING_CHOICES = [
        (round(i * 0.25, 2), str(round(i * 0.25, 2)))
        for i in range(8, 21)  # gera valores de 1.0 até 5.0 com passo 0.25
    ]

    BIRTH_MONTH_CHOICES = [(str(i), str(i)) for i in range(1, 13)]  # Gera valores de 1 a 12

    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="batches")
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="batches")
    batch_name = models.CharField(max_length=200)
    prior_batch = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='derivative')
    batch_maternity = models.CharField(
        max_length=3,
        choices=Choices.choices
    )
    batch_shapping = models.CharField(
        max_length=2,
        choices=ShappingChoices.choices,
        null=True,
        blank=True
    )
    birth_month = models.ManyToManyField(
        "BirthMonth",
        blank=True
    )
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name="batches", default=None)
    vet_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    batch_size = models.IntegerField()
    d0_date = models.DateField(blank=True, null=True, default=None)
    dg_date = models.DateField(blank=True, null=True, default=None)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rating"
    )
    negative_quant = models.IntegerField(default=0)
    recurrence_negative_quant = models.IntegerField(default=0)
    positive_quant = models.IntegerField(default=0)
    recurrence_positive_quant = models.IntegerField(default=0)
    recurrence_quant = models.IntegerField(default=0)
    uncertainty_quant = models.IntegerField(default=0)
    batch_acronym = models.CharField(max_length=50, default="", blank=True)

    def next_batch_number(self, *args, **kwargs):
        latest_batch = Batch.objects.filter(farm=self.farm, season=self.season).order_by("-id").first()
        if latest_batch and latest_batch.batch_name:
            try:
                latest_batch = int(latest_batch.batch_name.split()[-1])
            except ValueError:
                latest_batch = 0
            return latest_batch +1 
        return 1
    
    def save(self, *args, **kwargs):
    # Configura o nome do lote, se ainda não estiver definido
        if not self.batch_name:
            next_number = self.next_batch_number()
            self.batch_name = f"Lote {next_number}"
        
        super().save(*args, **kwargs)
        
        selected_birth_months = list(self.birth_month.all().values_list('month', flat=True))
        
        if self.batch_shapping in ["VS", "NN", "NP"]:
            self.batch_maternity = "N/A"
            self.batch_acronym = f"{self.batch_name} - {self.batch_shapping} - {self.rating} - N/A"
        else:
            if selected_birth_months:
                if len(selected_birth_months) == 1:
                    self.batch_acronym = f"{self.batch_name} - {self.batch_shapping} - {self.rating} - {self.batch_maternity} - {selected_birth_months[0]}"
                else:
                    birth_months_display = "; ".join(selected_birth_months)
                    self.batch_acronym = f"{self.batch_name} - {self.batch_shapping} - {self.rating} - {self.batch_maternity} - {birth_months_display}"
            else:
                self.batch_acronym = f"{self.batch_name} - {self.batch_shapping} - {self.rating} - {self.batch_maternity} - N/A"
        
        print(f"Batch acronym after update: {self.batch_acronym}")

        super().save(*args, **kwargs)