from django.db import models

# Create your models here.
class Farm(models.Model):
    def __str__(self):
        return self.farm_name

    farm_name = models.CharField(max_length=200, unique=True)
    farm_brand = models.ImageField(default="defaultlogo.jpg", upload_to="farm_logos")
    farm_acronym = models.CharField(max_length=4, default="")
    farm_owner = models.CharField(max_length=200)
    farm_location = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        # Transforma o farm_acronym em letras maiúsculas antes de salvar
        if self.farm_acronym:
            self.farm_acronym = self.farm_acronym.upper()
        super().save(*args, **kwargs)