# Generated by Django 5.1.1 on 2024-10-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='farm_acronym',
            field=models.CharField(default='', max_length=4),
        ),
    ]
