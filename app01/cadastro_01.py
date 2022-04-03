# -*- coding: utf-8 -*-

import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Grupo_eventos,Evento,Grupo_funcoes,Funcao
from . import funcoes_banco


def grupo_eventos(planilha,id_municipio,current_user):

    wb = openpyxl.load_workbook(planilha)
    sheets = wb.sheetnames

    sheet0 = sheets[0]
    sheet = wb.get_sheet_by_name(sheet0)


    row=2
    colA = sheet['A' + str(row)].value
    colB = sheet['B' + str(row)].value
    

    while row<sheet.max_row+1 and colA=='EVENTO' and colB==id_municipio:
        colD = sheet['D' + str(row)].value
        lista_1=[]
        while row<sheet.max_row+1 and colA=='EVENTO' and colB==id_municipio and colD==sheet['D' + str(row)].value:

            descricao = sheet['C' + str(row)].value # Id do tipo da decisao
            descricao_p = sheet['D' + str(row)].value # Id da decisao

            descricao   = descricao.strip()
            descricao_p = descricao_p.strip()

            
            if descricao != descricao_p:
                if descricao not in lista_1:
                    lista_1.append(descricao)


            colA = sheet['A' + str(row)].value
            colB = sheet['B' + str(row)].value
            colD = sheet['D' + str(row)].value

            row+=1
        if len(lista_1)>0:
            grupo_eventos_2(lista_1,descricao_p,id_municipio,current_user)

    return 1



def grupo_eventos_2(lista_descricoes,descricao_p,id_municipio,current_user):


    lista1=[]
    lista2=[]
    lista_id=[]
    lista_obj=[]

    obj = Evento.objects.filter(id_municipio=id_municipio,evento=descricao_p).first()
    if obj is not None:
        id_evento=obj.id_evento
    else:
        id_evento=0        

    if id_evento==0:
        return        

    objs = Grupo_eventos.objects.filter(desc_evento__in=[lista_descricoes[kk] for kk in range(len(lista_descricoes))])
    if objs.exists():
        for obj in objs:
            lista1.append(obj.desc_evento)
        for kk in range(len(lista_descricoes)):
            if lista_descricoes[kk] not in lista1:
                lista2.append(lista_descricoes[kk])
    else:
        lista2=lista_descricoes


    if len(lista2)>0:
        for kk in range(len(lista2)):
            obj = Grupo_eventos(
                id_municipio = id_municipio,
                desc_evento = lista2[kk],
                desc_evento_principal = descricao_p,
                id_user=current_user
            )
            lista_obj.append(obj)
        Grupo_eventos.objects.bulk_create(lista_obj)

    objs = Evento.objects.filter(id_municipio=id_municipio,evento__in=lista_descricoes)
    if objs.exists():
        for obj in objs:
            lista_id.append(obj.id_evento)


    funcoes_banco.delete_lista_de_eventos(lista_descricoes,id_municipio,lista_id,id_evento,current_user)

    return 1




def grupo_funcoes(planilha,id_municipio,current_user):

    wb = openpyxl.load_workbook(planilha)
    sheets = wb.sheetnames

    sheet0 = sheets[0]
    sheet = wb.get_sheet_by_name(sheet0)


    row=2
    colA = sheet['A' + str(row)].value
    colB = sheet['B' + str(row)].value
    

    while row<sheet.max_row+1 and colA=='FUNCAO' and colB==id_municipio:
        colD = sheet['D' + str(row)].value
        lista_1=[]
        while row<sheet.max_row+1 and colA=='FUNCAO' and colB==id_municipio and colD==sheet['D' + str(row)].value:

            descricao = sheet['C' + str(row)].value # Id do tipo da decisao
            descricao_p = sheet['D' + str(row)].value # Id da decisao

            descricao   = descricao.strip()
            descricao_p = descricao_p.strip()

            
            if descricao != descricao_p:
                if descricao not in lista_1:
                    lista_1.append(descricao)


            colA = sheet['A' + str(row)].value
            colB = sheet['B' + str(row)].value
            colD = sheet['D' + str(row)].value

            row+=1
        if len(lista_1)>0:
            grupo_funcao_2(lista_1,descricao_p,id_municipio,current_user)

    return 1


def grupo_funcoes_2(lista_descricoes,descricao_p,id_municipio,current_user):


    lista1=[]
    lista2=[]
    lista_id=[]
    lista_obj=[]

    obj = Funcao.objects.filter(id_municipio=id_municipio,evento=descricao_p).first()
    if obj is not None:
        id_funcao=obj.id_funcao
    else:
        id_funcao=0        

    if id_funcao==0:
        return        

    objs = Grupo_funcoes.objects.filter(desc_funcao__in=[lista_descricoes[kk] for kk in range(len(lista_descricoes))])
    if objs.exists():
        for obj in objs:
            lista1.append(obj.desc_funcao)
        for kk in range(len(lista_descricoes)):
            if lista_descricoes[kk] not in lista1:
                lista2.append(lista_descricoes[kk])
    else:
        lista2=lista_descricoes


    if len(lista2)>0:
        for kk in range(len(lista2)):
            obj = Grupo_funcoes(
                id_municipio = id_municipio,
                desc_funcao = lista2[kk],
                desc_funcao_principal = descricao_p,
                id_user=current_user
            )
            lista_obj.append(obj)
        Grupo_funcao.objects.bulk_create(lista_obj)

    objs = Funcao.objects.filter(id_municipio=id_municipio,funcao__in=lista_descricoes)
    if objs.exists():
        for obj in objs:
            lista_id.append(obj.id_funcao)


    funcoes_banco.delete_lista_de_funcoes(lista_descricoes,id_municipio,lista_id,id_funcao,current_user)

    return 1

