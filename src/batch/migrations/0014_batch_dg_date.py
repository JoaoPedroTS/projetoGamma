# Generated by Django 5.1.1 on 2024-10-23 22:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0013_batch_vet_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='dg_date',
            field=models.DateField(default=datetime.date(1500, 1, 1)),
        ),
    ]
