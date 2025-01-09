from django.db.models.signals import post_save
from .models import Batch, BirthMonth
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
        
        new_batch = Batch.objects.create(
            season = instance.season,
            farm = instance.farm,
            batch_name = child_name,
            prior_batch = instance,
            batch_maternity = instance.batch_maternity,
            protocol = instance.protocol, ##Revisar
            d0_date = instance.dg_date,
            batch_size = instance.negative_quant,
            batch_acronym = instance.batch_acronym,
            batch_shapping = instance.batch_shapping,
            order = instance.order,
            rating = instance.rating
        )
        
        birth_months = instance.birth_month.all()

        if birth_months.exists():
            new_batch.birth_month.set(birth_months)
        else:
            # Procura ou cria o objeto "N/A" no modelo BirthMonth
            na_month, created = BirthMonth.objects.get_or_create(month="N/A")
            new_batch.birth_month.set([na_month])