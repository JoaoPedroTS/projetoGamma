# Generated by Django 5.1.1 on 2024-10-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0022_batch_recurrence_quant'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='d0_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
