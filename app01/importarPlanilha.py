# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Pagamento



def importarExcel(planilha,id_municipio,anomes,current_user):

    lote = str(datetime.datetime.now().today())[0:19]

    idop = current_user


    wb = openpyxl.load_workbook(planilha)
    sheets = wb.sheetnames

    sheet0 = sheets[0]

    sheet = wb.get_sheet_by_name(sheet0)


    row=2
    erro=0
    qtde_itens=0
    retorno = True

    row=2
    erro=0
    objetos=[]
    while row<sheet.max_row+1:
        ccA = sheet['A' + str(row)].value # DC 
        ccB = sheet['B' + str(row)].value # Código da pasta
        ccC = sheet['C' + str(row)].value # Id do tipo da decisao

        ccA = ccA.strip()
        ccA = ccA.upper()
        row+=1

        objeto = Pagamento(
            anomes=anomes,
            id_municipio=id_municipio,
            codigo=ccA,
            nome=ccB,
            valor=ccC)

        objetos.append(objeto)
        
    Pagamento.objects.bulk_create(objetos)
    return None




