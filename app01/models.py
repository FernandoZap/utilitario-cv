from __future__ import unicode_literals
from django.db import connection
from django.db import models
from . import choices


#SET FOREIGN_KEY_CHECKS = 0;
#heroku run python manage.py shell --app civitas-plataforma

# TUTORIAL How to Reset Migrations
#https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

    #Restaurar o auto-increment no pgadmin
#http://blog.abraseucodigo.com.br/problemas-com-postgres-django-sequences.html
'''
neste exemplo estamos corrigindo o problema na tabela eventos_cv
SELECT c.relname FROM pg_class c WHERE c.relkind = 'S';
select * from eventos_cv_id_evento_cv_seq
select count(*) from eventos_cv
SELECT setval('eventos_cv_id_evento_cv_seq', 137);

observacao: o valor 137 é o resultado do select  count(*).
'''



#sudo /opt/pentaho/client-tools/data-integration/spoon.sh


# lista = [f.name for f in User._meta.get_fields()]

#https://www.sankalpjonna.com/learn-django/running-a-bulk-update-with-django



#-----------------------deletando varios objetos -------------------------------------------------------
'''
from django.db import connection 
from app.account.models import Store 
from app.recommendations.models import Recommendation

store = Store.objects.get(name=‘amazon’) 
recommendations = Recommendation.objects.filter(store=store) 
if recommendations.exists(): 
    cursor = connection.cursor()
    cursor.execute(“DELETE FROM app_recommendation WHERE store_id = %s”, [store.id])

'''
#2022-04-19
#git push heroku master

#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
#---------------------------------------------------------------------------

class Municipio(models.Model):  
    id_municipio = models.AutoField(primary_key=True)
    municipio = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100,default='')
    entidade = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.municipio

    class Meta:
            db_table = "municipios"        

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        

class Vinculo(models.Model):  
    id_vinculo = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    vinculo = models.CharField(max_length=100)

    def __str__(self):
        return self.vinculo

    class Meta:
        db_table = 'vinculos'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'vinculo'], name='unique_vinculo')
        ]


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        

class LogErro(models.Model):  
    id_logerro = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    anomes = models.IntegerField(default=0)
    numero_linha = models.IntegerField(null=True)
    codigo = models.CharField(max_length=100, null=True)
    observacao = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.codigo

    class Meta:
        db_table = 'logerro'


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Funcao(models.Model):  
    id_funcao = models.AutoField(primary_key=True)
    id_municipio =  models.IntegerField()
    empresa = models.CharField(max_length=50,default='')
    funcao = models.CharField(max_length=100)
    id_funcao_cv = models.IntegerField(default=0)
    cancelado = models.CharField(max_length=1,default='N')

    def __str__(self):
        return self.funcao

    class Meta:
        db_table = 'funcoes'

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Servidor(models.Model):  
    id_servidor = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    nome = models.CharField(max_length=100)
    cod_servidor = models.IntegerField()
    cpf = models.CharField(max_length=20,default='')
    data_admissao = models.DateField(null=True)
    ativo = models.IntegerField(default=1)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'servidores'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'cod_servidor'], name='servidor_unique')
        ]
        indexes = [
            models.Index(fields=['id_municipio'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Secretaria(models.Model):  
    id_secretaria = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    secretaria = models.CharField(max_length=100)

    def __str__(self):
        return self.secretaria

    class Meta:
        db_table = "secretarias"  
        constraints = [
            models.UniqueConstraint(fields=['id_municipio','secretaria'], name='unique_secretaria')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Evento(models.Model):  
    PROVDESC_CHOICES = [
        ('',''),
        ('V','VANTAGEM'),
        ('D','DESCONTO'),
    ]

    id_evento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    empresa = models.CharField(max_length=50,default='')
    tipo = models.CharField(max_length=9,choices=PROVDESC_CHOICES,default='V')
    evento = models.CharField(max_length=50)
    cancelado = models.CharField(max_length=1,default='N')
    exibe_excel = models.IntegerField(default=1)
    ordenacao = models.IntegerField(default=0)
    cl_orcamentaria = models.CharField(max_length=6, null=True)
    id_evento_cv = models.IntegerField(default=0)

    def __str__(self):
        return self.evento

    class Meta:
        db_table = 'eventos'

        

class Setor(models.Model):  
    id_setor = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    secretaria = models.ForeignKey(Secretaria,on_delete=models.CASCADE)
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.setor


    class Meta:
        db_table = 'setores'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio','secretaria', 'setor' ], name='unique_setor')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        




class Folhames(models.Model):
    id_folha = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField()
    cod_servidor = models.IntegerField()
    cpf = models.CharField(max_length=11, null=True)
    id_secretaria = models.IntegerField(null=True)
    id_setor = models.IntegerField(null=True)
    id_funcao = models.IntegerField(null=True)
    id_vinculo = models.IntegerField(null=True)
    previdencia = models.CharField(max_length=6, null=True)
    carga_horaria = models.IntegerField(null=True)
    dias = models.CharField(max_length=30, null=True)
    data_criacao = models.DateTimeField(null=True)

    def __str__(self):
        return self.cod_servidor

    class Meta:
        db_table = 'folhames'
        indexes = [
            models.Index(fields=['id_municipio','anomes'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        




class Folhaevento(models.Model):
    id_folhaevento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField()
    cod_servidor = models.IntegerField()
    previdencia = models.CharField(max_length=6, null=True)
    cl_orcamentaria = models.CharField(max_length=6, null=True)
    id_evento = models.IntegerField(null=True)
    tipo = models.CharField(max_length=1, null=True)
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.cod_servidor

    class Meta:
        db_table = 'folhaeventos'
        indexes = [
            models.Index(fields=['id_municipio','anomes'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        


class Refeventos(models.Model):  
    id_ref = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField()
    cod_servidor = models.IntegerField()
    ref_eventos = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.ref_eventos


    class Meta:
        db_table = 'refeventos'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio','anomes', 'cod_servidor' ], name='unique_refeventos')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField(null=True)
    codigo = models.IntegerField(null=True)
    nome_servidor = models.CharField(max_length=100, null=True)
    carga_horaria = models.IntegerField(null=True)
    secretaria = models.CharField(max_length=100,null=True)
    setor = models.CharField(max_length=100,null=True)
    tipo_admissao = models.CharField(max_length=100,null=True)
    data_admissao = models.CharField(max_length=10,null=True)
    previdencia = models.CharField(max_length=100, null=True)
    funcao = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.nome_servidor

    class Meta:
        db_table = 'funcionarios'
        indexes = [
            models.Index(fields=['id_municipio','anomes','codigo'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))                 

class Provento(models.Model):
    id_provento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField(null=True)
    codigo = models.IntegerField(null=True)
    previdencia = models.CharField(max_length=100, null=True,default='')
    tipo = models.IntegerField(null=True)
    evento = models.CharField(max_length=100,null=True)
    valor_evento = models.DecimalField(max_digits=9, decimal_places=2,null=True)
    classificacao = models.CharField(max_length=15, null=True)
    grupamento = models.CharField(max_length=1, null=True,default='N')
    lixo = models.IntegerField(null=True,default=0)


    def __str__(self):
        return self.codigo

    class Meta:
        db_table = 'proventos'
        indexes = [
            models.Index(fields=['id_municipio','anomes','codigo'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))                             


class Complemento(models.Model):
    id_complemento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField(null=True)
    codigo = models.IntegerField(null=True)
    ref_evento = models.CharField(max_length=20,null=True,default='')

    def __str__(self):
        return self.codigo

    class Meta:
        db_table = 'complementos'
        indexes = [
            models.Index(fields=['id_municipio','anomes','codigo'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))                             

class Temp_evento(models.Model):
    id_seq = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    evento = models.CharField(max_length=150,null=True,default='')
    tipo = models.CharField(max_length=1,null=True,default='V')

    def __str__(self):
        return self.evento

    class Meta:
        db_table = 'temp_eventos'
        indexes = [
            models.Index(fields=['id_municipio','evento'])
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))                             
