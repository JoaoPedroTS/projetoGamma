# Generated by Django 5.1.1 on 2024-10-25 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0023_batch_d0_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='recurrence_negative_quant',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='batch',
            name='recurrence_positive_quant',
            field=models.IntegerField(default=0),
        ),
    ]