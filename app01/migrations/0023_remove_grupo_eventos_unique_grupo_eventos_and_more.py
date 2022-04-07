# Generated by Django 4.0.1 on 2022-04-05 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0022_grupo_funcoes_id_user_grupo_funcoes_updated_at'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='grupo_eventos',
            name='unique_grupo_eventos',
        ),
        migrations.RenameField(
            model_name='grupo_eventos',
            old_name='id_municipio',
            new_name='empresa',
        ),
        migrations.AddField(
            model_name='evento',
            name='empresa',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddConstraint(
            model_name='grupo_eventos',
            constraint=models.UniqueConstraint(fields=('empresa', 'desc_evento'), name='unique_grupo_eventos'),
        ),
    ]
