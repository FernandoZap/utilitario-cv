# Generated by Django 4.0.1 on 2022-06-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_provento_grupamento'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Folha',
        ),
        migrations.DeleteModel(
            name='Planilha',
        ),
        migrations.AddField(
            model_name='provento',
            name='lixo',
            field=models.IntegerField(default=0, null=True),
        ),
    ]