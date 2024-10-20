from django.db import models
from farm.models import Farm

# Create your models here.
class Season(models.Model):
    def __str__(self):
        return self.season_name
    
    season_name = models.CharField(max_length=200)
    begin_date = models.DateField()
    end_date = models.DateField()
    farms = models.ManyToManyField(Farm, related_name='seasons')