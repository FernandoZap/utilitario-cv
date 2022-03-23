# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Secretaria,Vinculo,Funcao,Evento,Folha,Servidor,Setor,Folhames,Folhaevento,Planilha
from . import listagens



def importarServidores(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nrow):

    lote = str(datetime.datetime.now().today())[0:19]

    idop = current_user


    wb = openpyxl.load_workbook(planilha)
    sheets = wb.sheetnames

    sheet0 = sheets[0]

    sheet = wb.get_sheet_by_name(sheet0)


    retorno = True

    row=2
    erro=0
    objetos=[]
    lista=[]
    lista_servidores=listagens.listagemServidores(id_municipio)

    lista_incluidos=[]
    lista_cpf=[]
    while row<sheet.max_row+1 and row<nrow:
        

        cod_servidor = sheet['A' + str(row)].value # DC 
        nome_servidor = sheet['I' + str(row)].value # DC 
        data_admissao = sheet['M' + str(row)].value # DC 
        cpf = sheet['O' + str(row)].value # DC 
        valor = sheet['AL' + str(row)].value # DC 
        data_referencia = sheet['B' + str(row)].value # Código da pasta
        municipio_ref = sheet['AH' + str(row)].value # Código da pasta
        mes_referencia = sheet['D' + str(row)].value # Código da pasta


        if row==2:
            municipio_ref=municipio_ref.strip()
            data_ref=str(data_referencia)
            if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
                #print ('anomes 1: '+str(anomes))
                #print ('data_ref: '+data_ref[0:4]+data_ref[5:7])
                #print ('Erro: ano e mes não confere com a planilha informada.')
                return 'Erro: ano e mes não confere com a planilha informada.'
            if municipio_ref.upper()!=municipio.upper():
                #print ('municipio: '+municipio)
                #print ('Erro: nome da prefeitura não confere com planilha informada.')
                return 'Erro: nome da prefeitura não confere com planilha informada.'

        if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
            row+=1
            continue

        if mes_referencia is None:
            row+=1
            continue
        if municipio_ref is None:
            row+=1
            continue           
        if cod_servidor is None:
            row+=1
            continue

        row+=1

        nome_servidor=nome_servidor.strip()

        cpf=cpf.strip()

        if len(nome_servidor)==0 and len(str(cpf))==0 and len(str(valor))==0:
            break 
        if cod_servidor is None:
            break            

        if str(cod_servidor) not in lista_servidores:
            if str(cod_servidor) not in lista_incluidos:
                objeto = Servidor(
                    id_municipio=id_municipio,
                    cod_servidor=cod_servidor,
                    nome = nome_servidor,
                    cpf = cpf,
                    data_admissao = data_admissao
                    )
                objetos.append(objeto)
                lista_incluidos.append(str(cod_servidor))
        
    Servidor.objects.bulk_create(objetos)
    return ''


def importarSecretarias(planilha,id_municipio,anomes,current_user,mes_ref,nrow):

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
    lista=[]
    lista_secretarias=listagens.listagemSecretarias(id_municipio)
    while row<sheet.max_row+1 and row<8000:

        secretaria = sheet['A' + str(row)].value # DC 
        row+=1

        if secretaria is not None:
            if len(secretaria)>2:
                if secretaria not in lista_secretarias:
                    if secretaria not in lista:
                        objeto = Secretaria(
                            id_municipio=id_municipio,
                            secretaria=secretaria
                            )
                        lista.append(secretaria)
                        objetos.append(objeto)
        else:
            break                    
        
    Secretaria.objects.bulk_create(objetos)
    return None


'''
def importarSetores(planilha,id_municipio,anomes,current_user):

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
    lista=[]
    lista_setores=listagens.listagemSetores(id_municipio)
    while row<sheet.max_row+1 and row<8000:

        setor = sheet['B' + str(row)].value # DC 

        row+=1

        if setor is not None:
            setor = setor.strip()
            if len(setor)>2:
                if setor not in lista_setores:
                    if setor not in lista:
                        objeto = Setor(
                            id_municipio=id_municipio,
                            setor=setor
                            )
                        lista.append(setor)
                        objetos.append(objeto)
        else:
            break                    
        
    Setor.objects.bulk_create(objetos)
    return None
'''

'''

def importarVinculos(planilha,id_municipio,anomes,current_user,mes_ref):

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
    lista=[]
    lista_vinculos=listagens.listagemVinculos(id_municipio)
    while row<sheet.max_row+1 and row<8000:

        vinculo = sheet['C' + str(row)].value # DC 

        row+=1

        if vinculo is not None:
            vinculo = vinculo.strip()
            if len(vinculo)>2:
                if vinculo not in lista_vinculos:
                    if vinculo not in lista:
                        objeto = Vinculo(
                            id_municipio=id_municipio,
                            vinculo=vinculo
                            )
                        lista.append(vinculo)
                        objetos.append(objeto)
        else:
            break                    
        
    Vinculo.objects.bulk_create(objetos)
    return None
'''

'''
def importarFuncoes(planilha,id_municipio,anomes,current_user):

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
    lista=[]
    lista_funcoes=listagens.listagemFuncoes(id_municipio)
    while row<sheet.max_row+1 and row<8000:

        funcao = sheet['D' + str(row)].value # DC 

        row+=1

        if funcao is not None:
            funcao = funcao.strip()
            if len(funcao)>2:
                if funcao not in lista_funcoes:
                    if funcao not in lista:
                        objeto = Funcao(
                            id_municipio=id_municipio,
                            funcao=funcao
                            )
                        lista.append(funcao)
                        objetos.append(objeto)
        else:
            break                    
        
    Funcao.objects.bulk_create(objetos)
    return None

'''

'''
def importarEventos(planilha,id_municipio,anomes,current_user,municipio,mes_ref):

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
    lista=[]
    lista_eventos=listagens.listagemEventos(id_municipio)
    while row<sheet.max_row+1 and row<5500:

        evento = sheet['E' + str(row)].value # DC 

        mes_referencia = sheet['D' + str(row)].value # Código da pasta
        municipio_ref = sheet['AH' + str(row)].value # Código da pasta
        data_referencia = sheet['B' + str(row)].value # Código da pasta
        cod_evento = sheet['AV' + str(row)].value # Código da pasta


        if mes_referencia is None:
            row+=1
            continue
        if municipio_ref is None:
            row+=1
            continue

        if mes_referencia=='' or municipio_ref=='':
            row+=1
            continue

        data_ref=str(data_referencia)            

        if row==2:
            if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
                #print ('anomes 1: '+str(anomes))
                #print ('data_ref: '+data_ref[0:4]+data_ref[5:7])
                #print ('Erro: ano e mes não confere com a planilha informada.')
                return 'Erro: ano e mes não confere com a planilha informada.'
            if municipio_ref.upper()!=municipio.upper():
                #print ('municipio: '+municipio)
                #print ('Erro: nome da prefeitura não confere com planilha informada.')
                return 'Erro: nome da prefeitura não confere com planilha informada.'

        if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
            row+=1    
            continue




        row+=1

        if evento is not None:
            evento = evento.strip()
            if len(evento)>2:
                if evento not in lista_eventos:
                    if evento not in lista:
                        objeto = Evento(
                            id_municipio=id_municipio,
                            evento=evento,
                            codigo=cod_evento,
                            tipo='V'
                            )
                        lista.append(evento)
                        objetos.append(objeto)
        else:
            break                    
        
    Evento.objects.bulk_create(objetos)
    return None

'''

def importarSecFuncVincEventos(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nrow):


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
    carga_secretaria=[]
    carga_funcao=[]
    carga_vinculo=[]
    carga_evento=[]


    ls_secretaria=[]
    ls_funcao=[]
    ls_vinculo=[]
    ls_evento=[]


    lista_secretarias=listagens.listagemSecretarias(id_municipio)
    lista_funcoes=listagens.listagemFuncoes(id_municipio)
    lista_vinculos=listagens.listagemVinculos(id_municipio)
    lista_eventos=listagens.listagemEventos(id_municipio)


    while row<sheet.max_row+1 and row<6000:

        secretaria = sheet['W' + str(row)].value # DC 
        setor = sheet['X' + str(row)].value # DC 
        funcao = sheet['AB' + str(row)].value # DC 
        vinculo = sheet['Y' + str(row)].value # DC 
        evento = sheet['AJ' + str(row)].value # DC 
        nome_servidor = sheet['I' + str(row)].value # DC 
        data_referencia = sheet['B' + str(row)].value # Código da pasta
        municipio_ref = sheet['AH' + str(row)].value # Código da pasta
        cod_evento = sheet['AV' + str(row)].value # Código da pasta
        tipo = sheet['AI' + str(row)].value # Código da pasta

        mes_referencia = sheet['D' + str(row)].value # Código da pasta

        if mes_referencia is None:
            row+=1
            continue
        if municipio_ref is None:
            row+=1
            continue
        if nome_servidor is None:
            row+=1
            continue

        if mes_referencia=='' or municipio_ref=='' or nome_servidor=='':
            row+=1
            continue


        municipio_ref=municipio_ref.strip()

        data_ref=str(data_referencia)


        if row==2:
            if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
                #print ('anomes 1: '+str(anomes))
                #print ('data_ref: '+data_ref[0:4]+data_ref[5:7])
                #print ('Erro: ano e mes não confere com a planilha informada.')
                return 'Erro: ano e mes não confere com a planilha informada.'
            if municipio_ref.upper()!=municipio.upper():
                #print ('municipio: '+municipio)
                #print ('Erro: nome da prefeitura não confere com planilha informada.')
                return 'Erro: nome da prefeitura não confere com planilha informada.'

        if str(anomes)!=data_ref[0:4]+data_ref[5:7] and mes_ref!=mes_referencia.strip():
            row+=1    
            continue
        row+=1


        if nome_servidor is None:
            break
        if len(nome_servidor.strip())==0:
            break

        if tipo=='4':
            tipo_evento='D'
        elif tipo in ['1','2','3']:
            tipo_evento='V'
        else:
            tipo_evento='V'            


        if secretaria is not None:
            secretaria=secretaria.strip()
            if len(secretaria)>2:
                if secretaria not in lista_secretarias:
                    if secretaria not in ls_secretaria:
                        obj_secretaria = Secretaria(
                            id_municipio=id_municipio,
                            secretaria=secretaria
                            )
                        ls_secretaria.append(secretaria)
                        carga_secretaria.append(obj_secretaria)


        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                if funcao not in lista_funcoes:
                    if funcao not in ls_funcao:
                        obj_funcao = Funcao(
                            id_municipio=id_municipio,
                            funcao=funcao
                            )
                        ls_funcao.append(funcao)
                        carga_funcao.append(obj_funcao)

        if vinculo is not None:
            vinculo=vinculo.strip()
            if len(vinculo)>2:
                if vinculo not in lista_vinculos:
                    if vinculo not in ls_vinculo:
                        obj_vinculo = Vinculo(
                            id_municipio=id_municipio,
                            vinculo=vinculo
                            )
                        ls_vinculo.append(vinculo)
                        carga_vinculo.append(obj_vinculo)

        if evento is not None:
            evento=evento.strip()
            if len(evento)>2:
                if evento not in lista_eventos:
                    if evento not in ls_evento:
                        obj_evento = Evento(
                            id_municipio=id_municipio,
                            evento=evento,
                            codigo=cod_evento,
                            tipo = tipo_evento
                            )
                        ls_evento.append(evento)
                        carga_evento.append(obj_evento)
    
    Secretaria.objects.bulk_create(carga_secretaria)
    Funcao.objects.bulk_create(carga_funcao)
    Vinculo.objects.bulk_create(carga_vinculo)
    Evento.objects.bulk_create(carga_evento)

    return None



def importarSetores(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nrow):

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
    lista=[]
    lista_setores=listagens.listagemSetores(id_municipio)

    dict_secretarias=listagens.criarDictSecretarias(id_municipio)
    lista_secretarias = listagens.listagemSecretarias(id_municipio)

    while row<sheet.max_row+1 and row<700:

        secretaria = sheet['W' + str(row)].value # DC 
        setor = sheet['X' + str(row)].value # DC
        data_referencia = sheet['B' + str(row)].value # Código da pasta
        municipio_ref = sheet['AH' + str(row)].value # Código da pasta

        nome_servidor = sheet['I' + str(row)].value # DC 
        mes_referencia = sheet['D' + str(row)].value # Código da pasta


        if row==2:
            municipio_ref=municipio_ref.strip()

            data_ref=str(data_referencia)

            if str(anomes)!=data_ref[0:4]+data_ref[5:7]:
                #print ('anomes 1: '+str(anomes))
                #print ('data_ref: '+data_ref[0:4]+data_ref[5:7])
                #print ('Erro: ano e mes não confere com a planilha informada.')
                return 'Erro: ano e mes não confere com a planilha informada.'
            if municipio_ref.upper()!=municipio.upper():
                #print ('municipio: '+municipio)
                #print ('Erro: nome da prefeitura não confere com planilha informada.')
                return 'Erro: nome da prefeitura não confere com planilha informada.'


        if mes_referencia is None:
            row+=1
            continue
        if municipio_ref is None:
            row+=1
            continue
        if nome_servidor is None:
            row+=1
            continue

        if mes_referencia=='' or municipio_ref=='' or nome_servidor=='':
            row+=1
            continue


        row+=1

        if setor is not None:
            setor = setor.strip()
            secretaria = secretaria.strip()

            if secretaria in lista_secretarias:
                id_secretaria = dict_secretarias[secretaria]
                obj_sec = Secretaria.objects.get(pk=id_secretaria)


                if len(setor)>2:
                    if secretaria+setor not in lista_setores:
                        if secretaria+setor not in lista:
                            objeto = Setor(
                                id_municipio=id_municipio,
                                secretaria=obj_sec,
                                setor=setor
                                )
                            lista.append(secretaria+setor)
                            objetos.append(objeto)
        else:
            break                    
        
    Setor.objects.bulk_create(objetos)
    return None




def importarFolha(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nrow):

    wb = openpyxl.load_workbook(planilha)
    sheets = wb.sheetnames

    sheet0 = sheets[0]

    sheet = wb.get_sheet_by_name(sheet0)


    row=2
    erro=0
    qtde_itens=0
    retorno = True

    #dict_secretarias=listagens.dictSecretarias(id_municipio)
    dict_secretarias=listagens.criarDictSecretarias(id_municipio)
    lista_secretarias = listagens.listagemSecretarias(id_municipio)

    #dict_setores=listagens.dictSetores(id_municipio)
    dict_setores=listagens.criarDictSetores(id_municipio)
    lista_setores = listagens.listagemSetores(id_municipio)

    #dict_funcoes=listagens.dictFuncoes(id_municipio)
    dict_funcoes=listagens.criarDictFuncoes(id_municipio)
    lista_funcoes = listagens.listagemFuncoes(id_municipio)


    #dict_vinculos=listagens.dictVinculos(id_municipio)
    dict_vinculos=listagens.criarDictVinculos(id_municipio)
    lista_vinculos = listagens.listagemVinculos(id_municipio)

    #dict_eventos=listagens.dictEventos(id_municipio)
    dict_eventos=listagens.criarDictEventos(id_municipio)
    lista_eventos = listagens.listagemEventos(id_municipio)

    #dict_tipos_eventos=listagens.dictTiposEventos(id_municipio)
    dict_tipos_eventos=listagens.criarDictTiposDeEventos(id_municipio)


    listagem_folhames=listagens.listagemFolhames(id_municipio,anomes)


    lista=[]
    lista_eventosMes=[]

    row=2
    erro=0
    objetos=[]
    feventos=[]
    lista_incluidos=[]
    while row<sheet.max_row+1 and row<=nrow:
        
        cod_servidor = sheet['A' + str(row)].value # DC 
        cpf = sheet['O' + str(row)].value # DC 
        secretaria =  sheet['W' + str(row)].value # Código da pasta
        setor = sheet['X' + str(row)].value # Código da pasta
        funcao =  sheet['AB' + str(row)].value # Código da pasta
        vinculo = sheet['Y' + str(row)].value # Código da pasta
        previdencia = sheet['Z' + str(row)].value # Código da pasta
        cl_orcamentaria = sheet['AM' + str(row)].value # Código da pasta
        dias = sheet['AK' + str(row)].value # Código da pasta
        evento = sheet['AJ' + str(row)].value # Código da pasta
        cod_evento = sheet['AV' + str(row)].value # Código da pasta
        valor = sheet['AL' + str(row)].value # Código da pasta
        carga_horaria = sheet['L' + str(row)].value # Código da pasta
        nome_servidor = sheet['I' + str(row)].value # Código da pasta

        data_referencia = sheet['B' + str(row)].value # Código da pasta
        mes_referencia = sheet['D' + str(row)].value # Código da pasta
        municipio_ref = sheet['AH' + str(row)].value # Código da pasta

        


        
        if mes_referencia is None or municipio_ref is None or data_referencia is None or cod_servidor is None:
            row+=1
            continue

        data_ref=str(data_referencia)


        if row==2:
            if str(anomes)!=data_ref[0:4]+data_ref[5:7] or mes_ref!=mes_referencia.strip():
                #print ('anomes 1: '+str(anomes))
                #print ('data_ref: '+data_ref[0:4]+data_ref[5:7])
                #print ('Erro: ano e mes não confere com a planilha informada.')
                return 'Erro: ano e mes não confere com a planilha informada.'
            if municipio_ref.upper()!=municipio.upper():
                #print ('municipio: '+municipio)
                #print ('Erro: nome da prefeitura não confere com planilha informada.')
                return 'Erro: nome da prefeitura não confere com planilha informada.'

        if str(anomes)!=data_ref[0:4]+data_ref[5:7] or mes_ref!=mes_referencia.strip():
            row+=1
            continue

        row+=1

        if secretaria is None:
            secretaria=''
        secretaria=secretaria.strip()
        if secretaria=='':
            break

        setor=setor.strip()    

    
        if secretaria in lista_secretarias:
            id_secretaria = dict_secretarias[secretaria]
        else:
            id_secretaria=0            

        if secretaria+setor in lista_setores:
            id_setor = dict_setores[secretaria+setor]
        else:
            id_setor=0            

        if funcao in lista_funcoes:
            id_funcao = dict_funcoes[funcao]
        else:
            id_funcao=0            

        if vinculo in lista_vinculos:
            id_vinculo = dict_vinculos[vinculo]
        else:
            id_vinculo=0            

        if evento in lista_eventos:
            id_evento = dict_eventos[evento]
            tipo = dict_tipos_eventos[id_evento]
        else:
            id_evento=0
            tipo=''


        if cod_servidor is None:
            cod_servidor=''

        if nome_servidor is None:
            nome_servidor=''

        if cpf is None:
            cpf=''

        if valor is None:
            valor=''

        if len(str(cod_servidor))==0 and len(nome_servidor)==0 and len(str(cpf))==0 and len(str(valor))==0:
            break


        if id_secretaria==0 or id_setor==0 or id_funcao==0 or id_vinculo==0 or id_evento==0:
            erro=funcoes_gerais.gravarErro_01(id_municipio,anomes,row)


        if previdencia=='PREVIDÊNCIA MUNICIPAL':
            previdencia='M'
        elif previdencia=='INSS':
            previdencia='I'
        elif previdencia=='NÃO PAGA':
            previdencia='N'
        else:
            previndencia=''

        if str(cod_servidor)+'-'+str(cod_evento) not in lista_eventosMes:
            obj_feventos = Folhaevento(
                    id_municipio = id_municipio,
                    anomes = anomes,
                    cod_servidor = cod_servidor,
                    previdencia = previdencia,
                    cl_orcamentaria = cl_orcamentaria,
                    id_evento = id_evento,
                    tipo = tipo,
                    valor = valor
                )

            feventos.append(obj_feventos)
            lista_eventosMes.append(str(cod_servidor)+'-'+str(cod_evento))


        if cod_servidor not in lista_incluidos:
            if str(cod_servidor)+'-'+str(anomes) not in listagem_folhames:
                objeto = Folhames(
                    anomes=anomes,
                    id_municipio=id_municipio,
                    cod_servidor=cod_servidor,
                    cpf=cpf,
                    id_secretaria=id_secretaria,
                    id_setor=id_setor,
                    id_funcao=id_funcao,
                    id_vinculo=id_vinculo,
                    previdencia=previdencia,
                    dias = dias,
                    carga_horaria=carga_horaria
                    )

                objetos.append(objeto)
                lista_incluidos.append(cod_servidor)
        
    Folhames.objects.bulk_create(objetos)
    Folhaevento.objects.bulk_create(feventos)
    return ''



def importarSecFuncVincEventos2(id_municipio,anomes,municipio):

    row=2
    erro=0
    qtde_itens=0
    retorno = True

    row=2
    erro=0
    carga_secretaria=[]
    carga_funcao=[]
    carga_vinculo=[]
    carga_evento=[]


    ls_secretaria=[]
    ls_funcao=[]
    ls_vinculo=[]
    ls_evento=[]

    codigo_folha=int(str(anomes)[4:6])


    lista_secretarias=listagens.listagemSecretarias(id_municipio)
    lista_funcoes=listagens.listagemFuncoes(id_municipio)
    lista_vinculos=listagens.listagemVinculos(id_municipio)
    lista_eventos=listagens.listagemEventos(id_municipio)



    queryP = Planilha.objects.values(
        'codigo',
        'secretaria',
        'setor',
        'funcao',
        'evento',
        'cod_evento',
        'tipo',
        'tipo_admissao'
        ).filter(entidade=municipio,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        print (queryP[qp]['secretaria'])
        print (queryP[qp]['setor'])
        print (queryP[qp]['funcao'])
        print (queryP[qp]['tipo_admissao'])
        print (queryP[qp]['evento'])
        print ('--------------------')


        if queryP[qp]['tipo']=='4':
            tipo_evento='D'
        elif queryP[qp]['tipo'] in ['1','2','3']:
            tipo_evento='V'
        else:
            tipo_evento='V'            


        cod_evento=queryP[qp]['cod_evento']
        evento=queryP[qp]['evento']
        secretaria=queryP[qp]['secretaria']
        funcao=queryP[qp]['funcao']
        vinculo=queryP[qp]['tipo_admissao']
        
        if secretaria is not None:
            secretaria=secretaria.strip()
            if len(secretaria)>2:
                if secretaria not in lista_secretarias:
                    if secretaria not in ls_secretaria:
                        obj_secretaria = Secretaria(
                            id_municipio=id_municipio,
                            secretaria=secretaria
                            )
                        ls_secretaria.append(secretaria)
                        carga_secretaria.append(obj_secretaria)

        
        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                if funcao not in lista_funcoes:
                    if funcao not in ls_funcao:
                        obj_funcao = Funcao(
                            id_municipio=id_municipio,
                            funcao=funcao
                            )
                        ls_funcao.append(funcao)
                        carga_funcao.append(obj_funcao)

        
        if vinculo is not None:
            vinculo=vinculo.strip()
            if len(vinculo)>2:
                if vinculo not in lista_vinculos:
                    if vinculo not in ls_vinculo:
                        obj_vinculo = Vinculo(
                            id_municipio=id_municipio,
                            vinculo=vinculo
                            )
                        ls_vinculo.append(vinculo)
                        carga_vinculo.append(obj_vinculo)

        if evento is not None:
            evento=evento.strip()
            if len(evento)>2:
                if evento not in lista_eventos:
                    if evento not in ls_evento:
                        obj_evento = Evento(
                            id_municipio=id_municipio,
                            evento=evento,
                            codigo=cod_evento,
                            tipo = tipo_evento
                            )
                        ls_evento.append(evento)
                        carga_evento.append(obj_evento)

    '''
    Secretaria.objects.bulk_create(carga_secretaria)
    Funcao.objects.bulk_create(carga_funcao)
    Vinculo.objects.bulk_create(carga_vinculo)
    Evento.objects.bulk_create(carga_evento)
    '''

    return None

