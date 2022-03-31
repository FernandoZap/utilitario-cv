# Generated by Django 4.0.1 on 2022-03-31 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0017_grupo_funcoes_grupo_funcoes_unique_grupo_funcoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo_eventos',
            fields=[
                ('id_grupo', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField(null=True)),
                ('desc_evento', models.CharField(max_length=100, null=True)),
                ('desc_evento_principal', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'grupo_eventos',
            },
        ),
        migrations.AddConstraint(
            model_name='grupo_eventos',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'desc_evento'), name='unique_grupo_eventos'),
        ),
    ]