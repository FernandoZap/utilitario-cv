# -*- coding: utf-8 -*-
import os
import sys
from django.db import connection
from .models import Folhaevento,Evento,Eventos_cv


def delete_lista_de_eventos(lista,empresa,lista_id,descricao_p,current_user):
	pass
	'''

	#cursor = connection.cursor()
	#cursor.execute("DELETE FROM eventos \
		#WHERE id_municipio = %s AND evento in %s", [id_municipio,lista])

	objs=Evento.objects.filter(empresa=empresa,evento__in=descricao_p)
	lista1=[]
	lista_ids_principal=[]
	if objs.exsts():
		for obj in objs:
			lista1.append(obj.id_municipio)
			lista_ids_principal.append(obj.id_evento)
		dicionario1=dict(zip(lista1,lista_ids_principal))


	objs = Evento.objects.filter(empresa=empresa,evento__in=lista)
	if objs.exists()
		for kk in range(len(objs)):
			id_municipio=objs[kk].id_municipio
			id_titular=dicionario1(id_municipio)
			obj[kk].id_titular=id_titular
			obj[kk].exibe_excel=0
		Evento.objects.bulk_update(objs,[id_titular,exibe_excel])			

	if id_evento==0:
		ev1=Evento(id_municipio=id_municipio,evento=descricao_p,tipo='V',codigo=0,exibe_excel=1,cl_orcamentaria='O',ordenacao=0)
		ev1.save()
		obj = Evento.objects.filter(id_municipio=id_municipio,evento=descricao_p).first()
		if obj is not None:
			id_evento =  obj.id_evento


			query = Folhaevento.objects.filter(id_municipio=id_municipio,id_evento__in=lista_id)
			query.update(id_evento=id_evento)

			cursor.execute("UPDATE folhaeventos SET id_evento=%s \
				WHERE id_municipio = %s AND id_evento in %s", [id_evento,id_municipio,lista_id])

			query = Evento.objects.filter(id_municipio=id_municipio,id_evento__in=lista_id)
			query.update(exibe_excel=0)


	cursor.execute("UPDATE eventos SET exibe_excel=0 \
		WHERE id_municipio = %s AND id_evento in %s", [id_municipio,lista_id])

	cursor.close()
	del cursor
	'''
'''

def delete_lista_de_funcoes(lista,id_municipio,lista_id,id_funcao,current_user):

	cursor = connection.cursor()


	cursor.execute("UPDATE folhaeventos SET id_funcao=%s \
		WHERE id_municipio = %s AND id_funcao in %s", [id_funcao,id_municipio,lista_id])

	cursor.close()
	del cursor

'''

'''
def incluirEventos(empresa,lista_municipios,descricao_p):
	lista=[]
	carga=[]
	for kk in range(len(lista_municipios)):
		if lista_municipios[kk] not in lista:
		    obj_evento = Evento(
		        id_municipio=lista_municipios[kk],
		        evento=descricao_p,
		        empresa=empresa,
		        codigo=0,
		        tipo = 'V',
		        exibe_excel = 1,
		        cl_orcamentaria = 'O'
		        )
		    lista.append(lista_municipios[kk])
		    carga.append(obj_evento)

	if len(carga)>0:		    
		Evento.objects.bulk_create(carga)
	return 1    

'''

def incluirEventos(empresa,evento,id_evento_cv,tipo,cl_orcamentaria):
	pass

def incluirListaDeEventos(lst):
	'''
	 esta funcao esta sendo chamdas por importarPlanilha.py
	'''
	carga_evento=[]
	lista=[]
	for kk in range(len(lst)):
		obj = Eventos_cv.objects.filter(evento=lst[kk]['evento']).first()
		if obj is not None:

			if obj.evento not in lista:
				id_evento=obj.id_evento_cv

				obj_new = Evento(
					empresa=lst[kk]['empresa'],
					evento=lst[kk]['eventp'],
					tipo = lst[kk]['tipo'],
					exibe_excel = 1,
					cancelado='N',
					ordenacao=0,
					cl_orcamentaria = lst[kk]['cl_orcamentaria'],
					id_evento_cv=id_evento_cv
					)
				carga_evento.append(obj_new)
				lista.appen(obj.evento)
	if len(lista)>0:
		Evento.objects.bulk_create(carga_evento)


def incluirListaDeFuncoes(lst):
	'''
	 esta funcao esta sendo chamdas por importarPlanilha.py
	'''
	carga_funcao=[]
	lista=[]
	for kk in range(len(lst)):
		obj = Funcoes_cv.objects.filter(funcao=lst[kk]['funcao']).first()
		if obj is not None:

			if obj.funcao not in lista:
				id_funcao_cv=obj.id_funcao_cv

				obj_new = Funcao(
					empresa=lst[kk]['empresa'],
					funcao=lst[kk]['funcao'],
					id_funcao_cv = id_funcao_cv
					)
				carga_funcao.append(obj_new)
				lista.append(obj.funcao)
	if len(lista)>0:
		Funcao.objects.bulk_create(carga_funcao)














