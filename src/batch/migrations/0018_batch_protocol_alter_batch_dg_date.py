# Generated by Django 5.1.1 on 2024-10-23 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0017_alter_batch_dg_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='protocol',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='batch.protocol'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='dg_date',
            field=models.DateField(blank=True, default=None),
        ),
    ]