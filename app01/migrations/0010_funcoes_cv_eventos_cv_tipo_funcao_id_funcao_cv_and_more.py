# Generated by Django 4.0.1 on 2022-04-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_eventos_cv_evento_exibe_excel_evento_ordenacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funcoes_cv',
            fields=[
                ('id_funcao_cv', models.AutoField(primary_key=True, serialize=False)),
                ('funcao', models.CharField(max_length=100)),
                ('cancelado', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'funcoes_cv',
            },
        ),
        migrations.AddField(
            model_name='eventos_cv',
            name='tipo',
            field=models.CharField(default='V', max_length=1),
        ),
        migrations.AddField(
            model_name='funcao',
            name='id_funcao_cv',
            field=models.IntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name='funcoes_cv',
            constraint=models.UniqueConstraint(fields=('funcao',), name='unique_funcoes_cv'),
        ),
    ]
