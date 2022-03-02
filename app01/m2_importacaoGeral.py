# -*- coding: utf-8 -*-
import os
import sys
import datetime
import zipfile
import re
from .models import Departamento,Setor,Vinculo,ProvDesc
from . import funcoes_banco
import PyPDF2 as p2



def importacaoGeral(file_zip,id_municipio):

    lista_departamento=[]
    lista_setor=[]
    lista_funcionario=[]
    lista_matricula=[]
    lista_funcao=[]
    lista_vinculo=[]
    lista_lotacao=[]


    with zipfile.ZipFile(file_zip) as zip:

        retorno=0
        contador=0
        for filename in zip.namelist():
            file = zip.open(filename)

            pdf_reader = p2.PdfFileReader(file)

            n = pdf_reader.numPages
            text=''
            string='--------------------------------------------------------------'
            string+='----------------------------------------------------------------------'

            lista_1=[]
            lista_2=[]

            lista_final=[]
            for i in range(0,n):
                # creating a page object
                pageObj = pdf_reader.getPage(i)
                # extracting text from page
                text=pageObj.extractText()
                text=re.sub(string,'??',text)
                linha = text.split('??')
                inicio_de_pagina=0
                for ll in range(0,len(linha)):
                    if re.search(r'RESUMO DO SETOR',linha[ll]):
                        continue
                    inicio_de_pagina+=1


                    if not re.search(r'[\d]{4}[A-Z\s]{3,10}',(linha[ll])[0:11]):
                        if not re.search(r'SETOR:',linha[ll]):
                            if not re.search(r'SEC.:',linha[ll]):
                                continue

                    if re.search(r'TOTAL DE SERVIDORES',linha[ll]):
                        continue

                    depsetor=''

                    if ll==0:
                        if re.search(r'SETOR:',linha[ll]):
                            if re.search(r'SEC.:',linha[ll]):
                                lista_departamento.append(fcod_departamentoSetor(linha[ll],id_municipio,'departamento'))
                                lista_setor.append(fcod_departamentoSetor(linha[ll],id_municipio,'setor'))
                                continue
                    else:                        
                        if ll>0 and ll<n-1:
                            #print (linha[ll])
                            #print ('---------------')
                            matricula=fcod_matricula(linha[ll])
                            lista_funcionario.append(fcod_funcionario(matricula,(linha[ll])[0:90]))
                            funcao=fcod_funcaoVinculoLotacao(linha[ll][5:150])
                            #print (lista_funcionario)
                            #print('==============================================')
                            if len(funcao)==3:
                                lista_funcao.append(funcao[0])
                                lista_vinculo.append(funcao[1])
                                lista_lotacao.append(funcao[2])
                if i==n-1:
                    #print (((str(linha)).split("'"))[5])
                    proventos=fcod_provdesc(((str(linha)).split("'"))[5])


            set_depto=set(lista_departamento)                
            set_setor=set(lista_setor)
            funcoes_banco.gravar_departamento(set_depto,id_municipio)
            funcoes_banco.gravar_setor(set_setor,id_municipio)
            #set_funcionario=set(lista_funcionario)
            set_funcao=set(lista_funcao)
            set_vinculo=set(lista_vinculo)
            set_lotacao=set(lista_lotacao)
            funcoes_banco.gravar_funcionario(lista_funcionario,id_municipio)
            funcoes_banco.gravar_funcao(set_funcao,id_municipio)
            funcoes_banco.gravar_vinculo(set_vinculo,id_municipio)
            funcoes_banco.gravar_lotacao(set_lotacao,id_municipio)
            #funcoes_banco.gravar_proventos(proventos,id_municipio)
    zip.close()

def fcod_departamentoSetor(l_departamento,id_municipio,tipo):
    string_1=re.sub(r'SEC.:','$$',l_departamento)
    string_2=re.sub(r'SETOR:','$$',string_1)

    string_3=string_2.split('$$')
    if len(string_3)==3:
        depto=string_3[1]
        setor=(string_3[1])[0:3]+string_3[2]
        if tipo=='departamento':
            return depto
        else:
            return setor
    else:
        return ''

def fcod_funcaoVinculoLotacao(l_detalhe):
    #FUNCAO-VINCULO-LOTACAO
    lista=[]
    string1=re.sub(r'[\d]{1,12}[-]{1}','$$',l_detalhe)
    string2=re.sub(r'[\d]{4}','$$',string1)
    string3=string2.split('$$')
    if len(string3)>=4:
        s_funcao=string3[1]
        s_vinculo=string3[2]
        s_lotacao=string3[3]

        '''
        inputToken = '((('
        df['Title'] = df['Title'].str.replace(re.escape(inputToken), '>>')
        '''

        s_vinculo = re.escape(s_vinculo)

        s_funcao =  re.search(r'[\d]{4}'+s_funcao,l_detalhe)
        s_vinculo = re.search(r'[\d]{4}'+s_vinculo,l_detalhe)
        s_lotacao = re.search(r'[\d]{4}'+s_lotacao,l_detalhe)
        if s_funcao is not None:
            lista.append(s_funcao.group(0))
        else:
            lista.append('')
        if s_vinculo is not None:
            lista.append(s_vinculo.group(0))
        else:
            lista.append('')
        if s_lotacao is not None:
            lista.append(s_lotacao.group(0))
        else:
            lista.append('')
        return lista            
    return lista


def fcod_funcionario(matricula,l_detalhe):

    result = re.search(r'[\d]{5}[A-Z\s\.]{3,45}',l_detalhe)
    if result is not None:
        string =result.group(0)+';'+matricula
        return string

    return 'DESCONHECIDO'


def fcod_matricula(l_detalhe):
    string=l_detalhe[50:160]
    result = re.search(r'[\d]{2,12}[-]{1}[\d]{1,5}',string)
    if result is not None:
        string=result.group(0)
        return string[0:len(string)-4]
    else:
        result = re.search(r'[\d]{2,12}[-]{1}[A-Z]{1}',string)
        if result is not None:
            return result.group(0)
    return ''


'''
def fcod_provdesc(string):
    string1 = re.sub(r'[A-Z]{1}[\d]{4}[\s]{0,10}[\d]{0,3}[\.]{0,1}[\d]{0,3}[,]{1}[\d]{2}TOTAL DE SERVIDORES:','$$',string)
    string2=string1.split('$$')
    string3=string2[0]
    string4=re.sub(r'[A-Z]{1}[\d]{4}[\s]{0,10}[\d]{0,3}[\.]{0,1}[\d]{0,3}[\.]{0,1}[\d]{0,3}[\,]{0,1}[\d]{2}', '$$', string3)
    string5=string4.split('$$')
    return string5

'''
def fcod_provdesc(string):
    string1 = re.sub(r'TOTAL DE SERVIDORES:','$$',string)
    array1  = string1.split('$$')
    string2 = array1[0]
    string3 = re.sub(r'[\d]{0,7}[\.]{0,1}[\d]{0,3}[\.]{0,1}[\d]{1,3}[,]{1}[\d]{2}','$$',string2)
    array2 = string3.split('$$')
    lista=[]
    for kk in range(0,len(array2)):
        string = array2[kk].rstrip()
        ncaract = len(string)
        string=string[0:ncaract-4]
        string = re.sub(r'^[A-Z]{1}','',string)
        if string not in ['0051INSS','0052IRRF', '0053FMSS', '0123FALTAS', '0130PENSAO ALIMENTICIA', '0147FALTASEEO', '0166DESC. PARC. EMPREST.CONS.BRADESC']: 
            string = string[0:len(string)-1]
        lista.append(string)
    return lista




