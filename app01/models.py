from __future__ import unicode_literals
from django.db import connection
from django.db import models
from . import choices


#SET FOREIGN_KEY_CHECKS = 0;

class Municipio(models.Model):  
    id_municipio = models.AutoField(primary_key=True)
    municipio = models.CharField(max_length=100)
    modelo = models.IntegerField(default=0)
    string_pesquisa = models.CharField(max_length=100,default='')

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
    id_municipio = models.IntegerField()
    funcao = models.CharField(max_length=100)

    def __str__(self):
        return self.funcao

    class Meta:
        db_table = 'funcoes'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'funcao'], name='unique_funcao')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        


class Servidor(models.Model):  
    id_servidor = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField()
    nome = models.CharField(max_length=100)
    cod_servidor = models.CharField(max_length=20)
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
        return self.Secretaria

    class Meta:
        db_table = "secretarias"  
        constraints = [
            models.UniqueConstraint(fields=['id_municipio','secretaria'], name='unique_secretaria')
        ]

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {}'.format(cls._meta.db_table))        



class Folha(models.Model):
    id_folha = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(null=True)
    anomes = models.IntegerField()
    cod_servidor = models.CharField(max_length=6, null=True)
    cpf = models.CharField(max_length=11, null=True)
    id_secretaria = models.IntegerField(null=True)
    id_setor = models.IntegerField(null=True)
    id_funcao = models.IntegerField(null=True)
    id_vinculo = models.IntegerField(null=True)
    previdencia = models.CharField(max_length=6, null=True)
    cl_orcamentaria = models.CharField(max_length=6, null=True)
    carga_horaria = models.IntegerField(null=True)
    dias = models.CharField(max_length=30, null=True)
    id_evento = models.IntegerField(null=True)
    tipo = models.CharField(max_length=1, null=True)
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cod_servidor

    class Meta:
        db_table = 'folhas'
        indexes = [
            models.Index(fields=['id_municipio','anomes'])
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

    ID_MUNICIPIOS_CHOICES = [
        (150,'Abaiara'),
        (129,'Acarape'),
        (24,'Acaraú'),
        (33,'Acopiara'),
        (117,'Aiuaba'),
        (151,'Alcântaras'),
        (173,'Altaneira'),
        (125,'Alto Santo'),
        (41,'Amontada'),
        (175,'Antonina do Norte'),
        (131,'Apuiarés'),
        (13,'Aquiraz'),
        (17,'Aracati'),
        (73,'Aracoiaba'),
        (160,'Ararendá'),
        (93,'Araripe'),
        (152,'Aratuba'),
        (169,'Arneiroz'),
        (84,'Assaré'),
        (82,'Aurora'),
        (179,'Baixio'),
        (110,'Banabuiú'),
        (26,'Barbalha'),
        (89,'Barreira'),
        (87,'Barro'),
        (130,'Barroquinha'),
        (53,'Baturité'),
        (35,'Beberibe'),
        (60,'Bela Cruz'),
        (34,'Boa Viagem'),
        (37,'Brejo Santo'),
        (23,'Camocim'),
        (69,'Campos Sales'),
        (15,'Canindé'),
        (114,'Capistrano'),
        (86,'Caridade'),
        (108,'Cariré'),
        (72,'Caririaçu'),
        (106,'Cariús'),
        (115,'Carnaubal'),
        (20,'Cascavel'),
        (96,'Catarina'),
        (161,'Catunda'),
        (2,'Caucaia'),
        (143,'Chaval'),
        (139,'Choró'),
        (100,'Chorozinho'),
        (85,'Coreaú'),
        (18,'Crateús'),
        (6,'Crato'),
        (112,'Croatá'),
        (79,'Cruz'),
        (176,'Ereré'),
        (32,'Eusébio'),
        (81,'Forquilha'),
        (1,'Fortaleza'),
        (120,'Fortim'),
        (136,'Frecheirinha'),
        (170,'General Sampaio'),
        (134,'Graça'),
        (31,'Granja'),
        (181,'Granjeiro'),
        (156,'Groaíras'),
        (74,'Guaiúba'),
        (48,'Guaraciaba do Norte'),
        (180,'Guaramiranga'),
        (102,'Hidrolândia'),
        (21,'Horizonte'),
        (141,'Ibaretama'),
        (78,'Ibiapina'),
        (145,'Ibicuitinga'),
        (101,'Icapuí'),
        (22,'Icó'),
        (9,'Iguatu'),
        (76,'Independência'),
        (153,'Ipaporanga'),
        (146,'Ipaumirim'),
        (46,'Ipu'),
        (51,'Ipueiras'),
        (135,'Iracema'),
        (162,'Irapuan Pinheiro'),
        (83,'Irauçuba'),
        (168,'Itaiçaba'),
        (50,'Itaitinga'),
        (36,'Itapajé'),
        (7,'Itapipoca'),
        (98,'Itapiúna'),
        (45,'Itarema'),
        (92,'Itatira'),
        (113,'Jaguaretama'),
        (154,'Jaguaribara'),
        (57,'Jaguaribe'),
        (58,'Jaguaruana'),
        (71,'Jardim'),
        (167,'Jati'),
        (99,'Jericoacoara'),
        (3,'Juazeiro do Norte'),
        (80,'Jucás'),
        (28,'Limoeiro do Norte'),
        (103,'Madalena'),
        (64,'Mangabeira'),
        (4,'Maracanaú'),
        (8,'Maranguape'),
        (68,'Marco'),
        (155,'Martinópole'),
        (49,'Massapê.jpg Massapê'),
        (39,'Mauriti'),
        (128,'Meruoca'),
        (70,'Milagres'),
        (142,'Milhã'),
        (138,'Miraíma'),
        (54,'Missão Velha'),
        (42,'Mombaça'),
        (27,'Morada Nova'),
        (165,'Moraújo'),
        (88,'Morrinhos'),
        (133,'Mucambo'),
        (158,'Mulungu'),
        (126,'Nova Olinda'),
        (62,'Nova Russas'),
        (67,'Novo Oriente'),
        (94,'Orós'),
        (19,'Pacajus'),
        (11,'Pacatuba'),
        (148,'Pacoti'),
        (177,'Pacujá'),
        (163,'Palhano'),
        (140,'Palmácia'),
        (55,'Paracuru'),
        (59,'Paraipaba'),
        (65,'Parambu'),
        (149,'Paramoti'),
        (44,'Pedra Branca'),
        (164,'Penaforte'),
        (52,'Pentecoste'),
        (123,'Pereiro'),
        (97,'Pindoretama'),
        (119,'Piquet Caneiro'),
        (159,'Pires Ferreira'),
        (147,'Poranga'),
        (132,'Porteiras'),
        (157,'Potengi'),
        (178,'Potiretama'),
        (95,'Quiterianópolis'),
        (10,'Quixadá'),
        (124,'Quixelô'),
        (12,'Quixeramobim'),
        (90,'Quixeré'),
        (66,'Redenção'),
        (111,'Reriutaba'),
        (14,'Russas'),
        (127,'Saboeiro'),
        (121,'Salitre'),
        (61,'Santana do Acaraú'),
        (116,'Santana do Cariri'),
        (43,'Santa Quitéria'),
        (40,'São Benedito'),
        (38,'São Gonçalo do Amarante'),
        (174,'São João do Jaguaribe'),
        (144,'São Luís do Curu'),
        (77,'Senador Pompeu'),
        (171,'Senador Sá'),
        (5,'Sobral'),
        (109,'Solonópole'),
        (118,'Tabosa'),
        (63,'Tabuleiro do Norte'),
        (75,'Tamboril'),
        (166,'Tarrafas'),
        (29,'Tauá'),
        (105,'Tejuçuoca'),
        (16,'Tianguá'),
        (30,'Trairi'),
        (122,'Tururu'),
        (56,'Ubajara'),
        (172,'Umari'),
        (104,'Umirim'),
        (91,'Uruburetama'),
        (137,'Uruoca'),
        (107,'Varjota'),
        (47,'Várzea Alegre'),
        (25,'Viçosa do Ceará'),
    ]

    id_evento = models.AutoField(primary_key=True)
    id_municipio = models.IntegerField(choices=ID_MUNICIPIOS_CHOICES,default='')
    tipo = models.CharField(max_length=9,choices=PROVDESC_CHOICES,default='V')
    codigo = models.IntegerField(default=0)
    evento = models.CharField(max_length=50)
    cl_orcamentaria = models.CharField(max_length=6, null=True)
    ordenacao = models.IntegerField(default=0)

    def __str__(self):
        return self.evento

    class Meta:
        db_table = 'eventos'
        constraints = [
            models.UniqueConstraint(fields=['id_municipio', 'evento'], name='evento_unique')
        ]


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
    cod_servidor = models.CharField(max_length=6, null=True)
    cpf = models.CharField(max_length=11, null=True)
    id_secretaria = models.IntegerField(null=True)
    id_setor = models.IntegerField(null=True)
    id_funcao = models.IntegerField(null=True)
    id_vinculo = models.IntegerField(null=True)
    previdencia = models.CharField(max_length=6, null=True)
    carga_horaria = models.IntegerField(null=True)
    dias = models.CharField(max_length=30, null=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    cod_servidor = models.CharField(max_length=6, null=True)
    previdencia = models.CharField(max_length=6, null=True)
    cl_orcamentaria = models.CharField(max_length=6, null=True)
    id_evento = models.IntegerField(null=True)
    tipo = models.CharField(max_length=1, null=True)
    valor = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

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
