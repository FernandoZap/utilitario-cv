# Generated by Django 4.0.1 on 2022-07-09 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_temp_evento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folhaevento',
            name='updated_at',
        ),
    ]
