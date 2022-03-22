# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Evento,LogErro
import zipfile
import re
from django.db import connection
from django.db.models import Count,Sum


def mesPorExtenso(mes,modelo):

    lista_mes=['','JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    if modelo==1:
        return lista_mes[int(mes)]
    elif modelo==2:
        return (lista_mes[int(mes)])[0:3]


def mesReferencia(mes):
    lista_mes=['','JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    return lista_mes[int(mes)]


def cabecalhoFolha(id_municipio):
    lista=[]
    lista.append('Matricula')
    lista.append('Nome')
    lista.append('DataAdmissao')
    lista.append('Secretaria')
    lista.append('Setor')
    lista.append('Funcao')
    lista.append('Vinculo')
    lista.append('CargaHoraria')
    lista.append('Dias')

    objs=Evento.objects.filter(id_municipio=id_municipio,tipo='V').order_by('evento')
    for obj in objs:
        if obj.cl_orcamentaria is None:
            cl_orcamentaria=''
        else:
            cl_orcamentaria=obj.cl_orcamentaria
        lista.append(obj.evento+' ('+cl_orcamentaria+')')
    lista.append('Soma')
    return lista



def modelos(string_id_municipio):
    modelos_lista = [('86', 2), ('76', 1)]
    modelos = dict(modelos_lista)    
    return modelos[string_id_municipio]


def strings_pesquisa(string_id_municipio):
    modelos_lista = [
    ('86', 'PREFEITURA MUNICIPAL DE CARIDADE'), 
    ('15', 'PREFEITURA MUNICIPAL DE CANINDE'),
    ('124', 'PREFEITURA MUNICIPAL DE QUIXELO'),
    ('92', 'PREFEITURA MUNICIPAL DE ITATIRA')
    ]    

    modelos = dict(modelos_lista)    
    return modelos[string_id_municipio]



def eventosMes(id_municipio,anomes,cod_servidor):
    cursor = connection.cursor()
    cursor.execute("select ev.id_evento,ev.evento,coalesce(fm.valor,0) as valor \
    from eventos ev left join folhaeventos fm on fm.id_evento=ev.id_evento and \
    fm.anomes=%s and fm.id_municipio=%s and fm.cod_servidor=%s \
    where ev.tipo='V' and ev.id_municipio=%s order by ev.evento",[anomes,id_municipio,str(cod_servidor),id_municipio])

    query = dictfetchall(cursor)
    return query


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def gravarErro_01(id_municipio,anomes,row):
    log=LogErro(id_municipio=id_municipio,anomes=anomes,numero_linha=row)
    log.save()
    return 'ok'





