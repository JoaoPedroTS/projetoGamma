# Generated by Django 5.1.1 on 2024-11-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0026_remove_batch_batch_shaping_alter_batch_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='batch_shapping',
            field=models.CharField(blank=True, choices=[('VS', 'Vaca Solteira'), ('VL', 'Vaca leiteira'), ('VP', 'Vaca Parida'), ('NN', 'Novilha Normal'), ('NP', 'Novilha Precoce')], max_length=2, null=True),
        ),
    ]
