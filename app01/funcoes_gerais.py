# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import Evento,LogErro,Municipio,Eventos_cv
import zipfile
import re
from django.db import connection
from django.db.models import Count,Sum
import unidecode
import unicodedata


def mesPorExtenso(mes,modelo):

    lista_mes=['','JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    if modelo==1:
        return lista_mes[int(mes)]
    elif modelo==2:
        return (lista_mes[int(mes)])[0:3]


def mesReferencia(mes):
    lista_mes=['','JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
    return lista_mes[int(mes)]


def cabecalhoFolha(empresa):
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

    lista_ids = [ob.id_evento_cv for ob in Evento.objects.filter(empresa='SS',cancelado='N')]

    lista_set = set(lista_ids)

    ev_cv = Eventos_cv.objects.filter(tipo='V',id_evento_cv__in=lista_set).order_by('evento')

    for ob in ev_cv:
        lista.append(ob.evento)
    lista.append('soma')        


    '''
    objs=Evento_cv..objects.filter(empresa=empresa,tipo='V',exibe_excel=1).order_by('evento')
    for obj in objs:
        if obj.cl_orcamentaria is None:
            cl_orcamentaria=''
        else:
            cl_orcamentaria=obj.cl_orcamentaria
        lista.append(obj.evento+' ('+cl_orcamentaria+')')
    lista.append('Soma')
    '''
    return lista



def modelos(string_id_municipio):
    modelos_lista = [('86', 2), ('76', 1)]
    modelos = dict(modelos_lista)    
    return modelos[string_id_municipio]


def strings_pesquisa(id_municipio):

    lista1=[]
    lista2=[]
    secs = Municipio.objects.all()
    for sec in secs:
        lista1.append(
            str(sec.id_municipio)
            )
        lista2.append(
            'PREFEITURA MUNICIPAL DE '+(sec.municipio).upper()
            )

    dicionario = dict(zip(lista1,lista2))
    return dicionario[str(id_municipio)]

def entidade(id_municipio):
    munic = Municipio.objects.get(id_municipio=id_municipio)
    lista=[]
    if munic is not None:
        lista.append(munic.municipio)
        lista.append(munic.empresa)
    return lista        



def nome_do_municipio(id_municipio):

    lista1=[]
    lista2=[]
    secs = Municipio.objects.all()
    for sec in secs:
        lista1.append(
            sec.id_municipio
            )
        lista2.append(
            (sec.municipio).upper()
            )

    dicionario = dict(zip(lista1,lista2))
    return dicionario[id_municipio]

def eventosMes(id_municipio,anomes,cod_servidor):
    cursor = connection.cursor()
    cursor.execute("select ev.id_evento_cv,ev.evento,coalesce(fm.valor,0) as valor \
    from eventos_cv ev inner join folhaeventos fm on fm.id_evento=ev.id_evento_cv and \
    fm.anomes=%s and fm.id_municipio=%s and fm.cod_servidor=%s \
    where ev.tipo='V'order by ev.evento",[anomes,id_municipio,cod_servidor])

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




def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def to_ascii(ls):
    for i in range(len(ls)):
        ls[i] = unidecode.unidecode(ls[i])
    return ls

def to_ascii_string(string):
    return unidecode.unidecode(string)



def remove_combining_fluent(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return ''.join(
        [l for l in normalized if not unicodedata.combining(l)]
    )



