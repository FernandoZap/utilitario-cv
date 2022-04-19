# Generated by Django 4.0.1 on 2022-04-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id_evento', models.AutoField(primary_key=True, serialize=False)),
                ('empresa', models.CharField(default='', max_length=50)),
                ('tipo', models.CharField(choices=[('', ''), ('V', 'VANTAGEM'), ('D', 'DESCONTO')], default='V', max_length=9)),
                ('evento', models.CharField(max_length=50)),
                ('cancelado', models.CharField(default='N', max_length=1)),
                ('exibe_excel', models.IntegerField(default=1)),
                ('ordenacao', models.IntegerField(default=0)),
                ('cl_orcamentaria', models.CharField(max_length=6, null=True)),
                ('id_evento_cv', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'eventos',
            },
        ),
        migrations.CreateModel(
            name='Eventos_cv',
            fields=[
                ('id_evento_cv', models.AutoField(primary_key=True, serialize=False)),
                ('evento', models.CharField(max_length=100)),
                ('tipo', models.CharField(default='V', max_length=1)),
                ('cancelado', models.CharField(default='N', max_length=1)),
            ],
            options={
                'db_table': 'eventos_cv',
            },
        ),
        migrations.CreateModel(
            name='Folhaevento',
            fields=[
                ('id_folhaevento', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField(null=True)),
                ('anomes', models.IntegerField()),
                ('cod_servidor', models.IntegerField()),
                ('previdencia', models.CharField(max_length=6, null=True)),
                ('cl_orcamentaria', models.CharField(max_length=6, null=True)),
                ('id_evento', models.IntegerField(null=True)),
                ('tipo', models.CharField(max_length=1, null=True)),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'folhaeventos',
            },
        ),
        migrations.CreateModel(
            name='Folhames',
            fields=[
                ('id_folha', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField(null=True)),
                ('anomes', models.IntegerField()),
                ('cod_servidor', models.IntegerField()),
                ('cpf', models.CharField(max_length=11, null=True)),
                ('id_secretaria', models.IntegerField(null=True)),
                ('id_setor', models.IntegerField(null=True)),
                ('id_funcao', models.IntegerField(null=True)),
                ('id_vinculo', models.IntegerField(null=True)),
                ('previdencia', models.CharField(max_length=6, null=True)),
                ('carga_horaria', models.IntegerField(null=True)),
                ('dias', models.CharField(max_length=30, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'folhames',
            },
        ),
        migrations.CreateModel(
            name='Funcao',
            fields=[
                ('id_funcao', models.AutoField(primary_key=True, serialize=False)),
                ('empresa', models.CharField(default='', max_length=50)),
                ('funcao', models.CharField(max_length=100)),
                ('id_funcao_cv', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'funcoes',
            },
        ),
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
        migrations.CreateModel(
            name='LogErro',
            fields=[
                ('id_logerro', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('anomes', models.IntegerField(default=0)),
                ('numero_linha', models.IntegerField(null=True)),
                ('codigo', models.CharField(max_length=100, null=True)),
                ('observacao', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'logerro',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id_municipio', models.AutoField(primary_key=True, serialize=False)),
                ('municipio', models.CharField(max_length=100)),
                ('empresa', models.CharField(default='', max_length=100)),
                ('entidade', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'municipios',
            },
        ),
        migrations.CreateModel(
            name='Planilha',
            fields=[
                ('id_planilha', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.IntegerField(null=True)),
                ('data_ref', models.DateField(null=True)),
                ('codigo_folha', models.IntegerField(null=True)),
                ('folha', models.CharField(max_length=100, null=True)),
                ('nome_servidor', models.CharField(max_length=100, null=True)),
                ('carga_horaria', models.IntegerField(null=True)),
                ('cpf', models.CharField(max_length=15, null=True)),
                ('secretaria', models.CharField(max_length=100, null=True)),
                ('setor', models.CharField(max_length=100, null=True)),
                ('tipo_admissao', models.CharField(max_length=100, null=True)),
                ('data_admissao', models.DateField(default=None, null=True)),
                ('previdencia', models.CharField(max_length=100, null=True)),
                ('funcao', models.CharField(max_length=100, null=True)),
                ('entidade', models.CharField(max_length=100, null=True)),
                ('tipo', models.IntegerField(null=True)),
                ('evento', models.CharField(max_length=100, null=True)),
                ('ref_evento', models.CharField(max_length=20, null=True)),
                ('valor_evento', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('classificacao', models.CharField(max_length=15, null=True)),
                ('cod_evento', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'planilhas',
            },
        ),
        migrations.CreateModel(
            name='Refeventos',
            fields=[
                ('id_ref', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField(null=True)),
                ('anomes', models.IntegerField()),
                ('cod_servidor', models.IntegerField()),
                ('ref_eventos', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'refeventos',
            },
        ),
        migrations.CreateModel(
            name='Secretaria',
            fields=[
                ('id_secretaria', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('secretaria', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'secretarias',
            },
        ),
        migrations.CreateModel(
            name='Servidor',
            fields=[
                ('id_servidor', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('cod_servidor', models.IntegerField()),
                ('cpf', models.CharField(default='', max_length=20)),
                ('data_admissao', models.DateField(null=True)),
                ('ativo', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'servidores',
            },
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id_setor', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('setor', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'setores',
            },
        ),
        migrations.CreateModel(
            name='Vinculo',
            fields=[
                ('id_vinculo', models.AutoField(primary_key=True, serialize=False)),
                ('id_municipio', models.IntegerField()),
                ('vinculo', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'vinculos',
            },
        ),
        migrations.AddConstraint(
            model_name='vinculo',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'vinculo'), name='unique_vinculo'),
        ),
        migrations.AddField(
            model_name='setor',
            name='secretaria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.secretaria'),
        ),
        migrations.AddIndex(
            model_name='servidor',
            index=models.Index(fields=['id_municipio'], name='servidores_id_muni_9234b3_idx'),
        ),
        migrations.AddConstraint(
            model_name='servidor',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'cod_servidor'), name='servidor_unique'),
        ),
        migrations.AddConstraint(
            model_name='secretaria',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'secretaria'), name='unique_secretaria'),
        ),
        migrations.AddConstraint(
            model_name='refeventos',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'anomes', 'cod_servidor'), name='unique_refeventos'),
        ),
        migrations.AddIndex(
            model_name='planilha',
            index=models.Index(fields=['codigo'], name='planilhas_codigo_72556f_idx'),
        ),
        migrations.AddConstraint(
            model_name='funcoes_cv',
            constraint=models.UniqueConstraint(fields=('funcao',), name='unique_funcoes_cv'),
        ),
        migrations.AddIndex(
            model_name='folhames',
            index=models.Index(fields=['id_municipio', 'anomes'], name='folhames_id_muni_e88aea_idx'),
        ),
        migrations.AddIndex(
            model_name='folhaevento',
            index=models.Index(fields=['id_municipio', 'anomes'], name='folhaevento_id_muni_ef07fe_idx'),
        ),
        migrations.AddConstraint(
            model_name='setor',
            constraint=models.UniqueConstraint(fields=('id_municipio', 'secretaria', 'setor'), name='unique_setor'),
        ),
    ]
