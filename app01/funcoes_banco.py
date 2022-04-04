# -*- coding: utf-8 -*-
import os
import sys
from django.db import connection
from .models import Folhaevento,Evento


def delete_lista_de_eventos(lista,id_municipio,lista_id,id_evento,current_user):


	#cursor = connection.cursor()
	#cursor.execute("DELETE FROM eventos \
		#WHERE id_municipio = %s AND evento in %s", [id_municipio,lista])


	query = Folhaevento.objects.filter(id_municipio=id_municipio,id_evento__in=lista_id)
	query.update(id_evento=id_evento)

	'''
	cursor.execute("UPDATE folhaeventos SET id_evento=%s \
		WHERE id_municipio = %s AND id_evento in %s", [id_evento,id_municipio,lista_id])
	'''		

	query = Evento.objects.filter(id_municipio=id_municipio,id_evento__in=lista_id)
	query.update(exibe_excel=0)


	'''
	cursor.execute("UPDATE eventos SET exibe_excel=0 \
		WHERE id_municipio = %s AND id_evento in %s", [id_municipio,lista_id])

	cursor.close()
	del cursor
	'''


def delete_lista_de_funcoes(lista,id_municipio,lista_id,id_funcao,current_user):

	cursor = connection.cursor()


	cursor.execute("UPDATE folhaeventos SET id_funcao=%s \
		WHERE id_municipio = %s AND id_funcao in %s", [id_funcao,id_municipio,lista_id])

	cursor.close()
	del cursor


'''
insert into eventos (codigo,evento,tipo,ordenacao,cl_orcamentaria,exibe_excel,id_municipio)
SELECT 161,'GRATIFICACAO 1,5%','V',0,'O',1,86 UNION
SELECT 191,'GRATIFICACAO DE 25%','V',0,'O',1,86 UNION
SELECT 160,'GRATIFICACAO INCENTIVO 12%','V',0,'O',1,86;

select * from eventos where id_municipio=86 and evento like 'GRAT%';

17,16,5


select * from folhaeventos where id_evento in (17,16,5);


id_folhaevento  | int          | NO   | PRI | NULL    | auto_increment |
| id_municipio    | int          | YES  | MUL | NULL    |                |
| anomes          | int          | NO   |     | NULL    |                |
| cod_servidor    | int          | NO   |     | NULL    |                |
| previdencia     | varchar(6)   | YES  |     | NULL    |                |
| cl_orcamentaria | varchar(6)   | YES  |     | NULL    |                |
| id_evento       | int          | YES  |     | NULL    |                |
| tipo            | varchar(1)   | YES  |     | NULL    |                |
| valor           |


insert into folhaeventos (id_municipio,anomes,cod_servidor,previdencia,cl_orcamentaria,id_evento,tipo,valor,updated_at)
select 86,202111,1011,'I','O',4,'v',100.00,'2022-04-01' UNION
select 86,202111,1012,'I','O',45,'v',200.00,'2022-04-01' UNION
select 86,202111,1013,'I','O',46,'v',300.00,'2022-04-01' UNION
select 86,202111,1014,'I','O',47,'v',400.00,'2022-04-01' UNION
select 86,202111,1014,'I','O',2,'v',500.00,'2022-04-01' UNION
select 86,202111,1014,'I','O',10,'v',600.00,'2022-04-01' UNION
select 86,202111,1033,'I','O',45,'v',1100.00,'2022-04-01' UNION
select 86,202111,1042,'I','O',45,'v',1200.00,'2022-04-01';

select * from folhaeventos;

'''














