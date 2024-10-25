from django.utils import timezone
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

    def get_duration(self):
        delta = self.end_date - self.begin_date
        return delta.days + 1
    
    def get_remaining_days(self):
        today = timezone.now().date()

        if self.end_date >= today:
            remaining_days = self.end_date - today
            return remaining_days.days
        
        return 0