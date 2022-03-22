# Generated by Django 4.0.1 on 2022-03-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_evento_cl_orcamentaria'),
    ]

    operations = [
        migrations.AddField(
            model_name='logerro',
            name='anomes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logerro',
            name='numero_linha',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logerro',
            name='codigo',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='logerro',
            name='observacao',
            field=models.CharField(max_length=255, null=True),
        ),
    ]