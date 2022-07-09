# Generated by Django 4.0.1 on 2022-07-08 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_remove_folhames_updated_at_folhames_data_criacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_evento',
            fields=[
                ('id_seq', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField(null=True)),
                ('evento', models.CharField(default='', max_length=150, null=True)),
                ('tipo', models.CharField(default='V', max_length=1, null=True)),
            ],
            options={
                'db_table': 'temp_eventos',
            },
        ),
        migrations.AddIndex(
            model_name='temp_evento',
            index=models.Index(fields=['id_municipio', 'evento'], name='temp_evento_id_muni_0f855e_idx'),
        ),
    ]
