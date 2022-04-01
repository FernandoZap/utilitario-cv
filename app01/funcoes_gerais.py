# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Evento,LogErro,Municipio
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

    lista.append('Secretaria')
    lista.append('Setor')
    lista.append('Matricula')
    lista.append('Nome')
    lista.append('Funcao')
    lista.append('Vinculo')
    lista.append('DataAdmissao')
    lista.append('CargaHoraria')
    lista.append('Dias')

    objs=Evento.objects.filter(id_municipio=id_municipio,tipo='V',exibe_excel=1).order_by('evento')
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
    ('92', 'PREFEITURA MUNICIPAL DE ITATIRA'),
    ('134', 'PREFEITURA MUNICIPAL DE GRAÇA'),
    ('42', 'PREFEITURA MUNICIPAL DE MOMBAÇA'),
    ('109', 'PREFEITURA MUNICIPAL DE SOLONÓPOLE'),
    ('44', 'PREFEITURA MUNICIPAL DE PEDRA BRANCA'),
    ('38', 'PREFEITURA MUNICIPAL DE SÃO GONÇALO DO AMARANTE'),
    ('125', 'PREFEITURA MUNICIPAL DE ALTO SANTO'),
    ('152', 'PREFEITURA MUNICIPAL DE ARATUBA'),
    ('162', 'PREFEITURA MUNICIPAL DE IRAPUAN PINHEIRO'),
    ('76', 'PREFEITURA MUNICIPAL DE INDEPENDÊNCIA'),
    ('57', 'PREFEITURA MUNICIPAL DE JAGUARIBE'),
    ('177', 'PREFEITURA MUNICIPAL DE PACUJÁ'),
    ('119', 'PREFEITURA MUNICIPAL DE PIQUET CARNEIRO'),
    ('174', 'PREFEITURA MUNICIPAL DE SÃO JOÃO DO JAGUARIBE'),
    ('107', 'PREFEITURA MUNICIPAL DE VARJOTA')
    ] 


    lista1=[]
    lista2=[]
    secs = Municipio.objects.all()
    for sec in secs:
        lista1.append(
            sec.id_municipio
            )
        lista2.append(
            sec.municipio
            )

    dicionario = dict(zip(lista1,lista2))
    return dicionario[string_id_municipio]



def eventosMes(id_municipio,anomes,cod_servidor):
    cursor = connection.cursor()
    cursor.execute("select ev.id_evento,ev.evento,coalesce(fm.valor,0) as valor \
    from eventos ev left join folhaeventos fm on fm.id_evento=ev.id_evento and \
    fm.anomes=%s and fm.id_municipio=%s and fm.cod_servidor=%s \
    where ev.tipo='V' and ev.id_municipio=%s and ev.exibe_excel=1 order by ev.evento",[anomes,id_municipio,cod_servidor,id_municipio])

    query = dictfetchall(cursor)
    return query


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def gravarErro_01(id_municipio,anomes,observacao):
    log=LogErro(id_municipio=id_municipio,anomes=anomes,observacao=observacao)
    log.save()
    return 'ok'
