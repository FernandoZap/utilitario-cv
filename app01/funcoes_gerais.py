# -*- coding: utf-8 -*-
import os
import sys
import re
from .models import LogErro,Municipio,Funcao,Evento
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

    lista_eventos = [ob.evento for ob in Evento.objects.filter(id_municipio=id_municipio,cancelado='N',tipo='V',exibe_excel=1)]


    for kk in range(len(lista_eventos)):
        lista.append(lista_eventos[kk])
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
    cursor.execute("select ev.id_evento, ev.evento,coalesce(fm.valor,0) as valor \
    from eventos ev inner join folhaeventos fm on fm.id_evento=ev.id_evento and \
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



