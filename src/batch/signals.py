from django.db.models.signals import post_save
from .models import Batch
from django.dispatch import receiver

@receiver(post_save, sender=Batch)
def create_negative_derived_batch(sender, instance, created, **kwargs):
    if not created and getattr(instance, "work_day", False) and instance.negative_quant is not None:
        
        name_parts = instance.batch_name.split("/")
        if len(name_parts) > 1:
            sufix = int(name_parts[1])+1
            child_name = f"{name_parts[0]}/{sufix}"
        else:
            child_name = f"{name_parts[0]}/1"
        
        Batch.objects.create(
            season = instance.season,
            farm = instance.farm,
            batch_name = child_name,
            prior_batch = instance,
            batch_maternity = instance.batch_maternity,
            protocol = instance.protocol,
            d0_date = instance.dg_date,
            batch_size = instance.negative_quant
        )