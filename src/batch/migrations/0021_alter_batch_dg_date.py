# Generated by Django 5.1.1 on 2024-10-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0020_alter_batch_protocol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='dg_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]