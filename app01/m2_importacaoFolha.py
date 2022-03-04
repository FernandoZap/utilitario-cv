# -*- coding: utf-8 -*-
import zipfile
import re
from . import funcoes_banco
import PyPDF2 as p2




def importacaoFolha(file_zip,id_municipio,anomes):


    lista_departamento=[]
    lista_setor=[]
    lista_funcionario=[]
    lista_matricula=[]
    lista_funcao=[]
    lista_vinculo=[]
    lista_lotacao=[]
    lista_final=[]
    lista_provdesc=[]

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
            lista_provdesc=[]
            for i in range(0,n-2):
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
                    if re.search(r'RESUMO DA SECRETARIA',linha[ll]):
                        continue
                    if re.search(r'RESUMO GERAL',linha[ll]):
                        continue
                    inicio_de_pagina+=1
                    lista_provdesc=[]
                    


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
                                depto=fcod_departamentoSetor(linha[ll],id_municipio,'departamento')
                                cod_depto=depto[0:3]

                                setor=fcod_departamentoSetor(linha[ll],id_municipio,'setor')
                                cod_setor=setor[3:9]
                                continue


                    else:                        
                        if ll>0:
                            cod_matricula=fcod_matricula(linha[ll])
                            funcionario=fcod_funcionario((linha[ll])[0:90])
                            cod_funcionario=funcionario[0:5]
                            #if cod_funcionario=='02799' or cod_funcionario=='02804' or cod_funcionario=='00584':
                                #print ('cod_matricula: '+cod_matricula)
                            nome_funcionario=funcionario[5:]
                            proventos=fproventos(linha[ll],cod_matricula)


                            for k in range(len(proventos)):
                                if k>0:
                                    lista_provdesc.append(f_montaProventos(proventos[k]))

                            funcao=fcod_funcaoVinculoLotacao(linha[ll][5:150])
                            if len(funcao)==3:
                                cod_funcao=funcao[0]
                                cod_vinculo=funcao[1]
                                cod_lotacao=funcao[2]
                            else:
                                cod_funcao='0000'
                                cod_vinculo='0000'
                                cod_lotacao='0000'
                            lista_final.append(
                                    {
                                        'cod_depto':cod_depto,
                                        'cod_setor':cod_setor,
                                        'cod_matricula':cod_matricula,
                                        'cod_funcionario':cod_funcionario,
                                        'cod_funcao':cod_funcao,
                                        'cod_vinculo':cod_vinculo,
                                        'cod_lotacao':cod_lotacao,
                                        'proventos':lista_provdesc,
                                        'id_municipio':id_municipio,
                                        'anomes':anomes
                                    }
                                )

        retorno = funcoes_banco.gravar_folhaMensal(lista_final)
        file.close()
    return None



'''
def importacaoFolha(file_zip,id_municipio,anomes):


    lista_departamento=[]
    lista_setor=[]
    lista_funcionario=[]
    lista_matricula=[]
    lista_funcao=[]
    lista_vinculo=[]
    lista_lotacao=[]
    lista_final=[]
    lista_provdesc=[]

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
            for i in range(0,n-2):
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
                    if re.search(r'RESUMO DA SECRETARIA',linha[ll]):
                        continue
                    if re.search(r'RESUMO GERAL',linha[ll]):
                        continue
                    inicio_de_pagina+=1
                    lista_provdesc=[]


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
                                depto=fcod_departamentoSetor(linha[ll],id_municipio,'departamento')
                                cod_depto=depto[0:3]

                                setor=fcod_departamentoSetor(linha[ll],id_municipio,'setor')
                                cod_setor=setor[3:9]
                                continue


                    else:                        
                        if ll>0:
                            cod_matricula=fcod_matricula(linha[ll])
                            funcionario=fcod_funcionario((linha[ll])[0:90])
                            cod_funcionario=funcionario[0:5]
                            #if cod_funcionario=='02799' or cod_funcionario=='02804' or cod_funcionario=='00584':
                                #print ('cod_matricula: '+cod_matricula)
                            nome_funcionario=funcionario[5:]
                            proventos=fproventos(linha[ll],cod_matricula)


                            for k in range(len(proventos)):
                                if k>0:
                                    lista_provdesc.append(f_montaProventos(proventos[k]))

                            funcao=fcod_funcaoVinculoLotacao(linha[ll][5:150])
                            if len(funcao)==3:
                                cod_funcao=funcao[0]
                                cod_vinculo=funcao[1]
                                cod_lotacao=funcao[2]
                            else:
                                cod_funcao='0000'
                                cod_vinculo='0000'
                                cod_lotacao='0000'
                            lista_final.append(
                                    {
                                        'cod_depto':cod_depto,
                                        'cod_setor':cod_setor,
                                        'cod_matricula':cod_matricula,
                                        'cod_funcionario':cod_funcionario,
                                        'cod_funcao':cod_funcao,
                                        'cod_vinculo':cod_vinculo,
                                        'cod_lotacao':cod_lotacao
                                    }
                                )

                    for k in lista_final:   
                        retorno=funcoes_banco.gravar_folhaMensal(
                            id_municipio,
                            anomes,
                            k['cod_depto'],
                            k['cod_setor'],
                            k['cod_funcionario'],
                            k['cod_matricula'],
                            k['cod_funcao'],
                            k['cod_lotacao'],
                            k['cod_vinculo'],
                            lista_provdesc
                            )
                    lista_provdesc=[]
                    lista_final=[]
            break
        #print (lista_provdesc)
        #print ('----------------------')
        file.close()
        return None
'''


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
            lista.append(s_funcao.group(0)[0:4])
        else:
            lista.append('')
        if s_vinculo is not None:
            lista.append(s_vinculo.group(0)[0:4])
        else:
            lista.append('')
        if s_lotacao is not None:
            lista.append(s_lotacao.group(0)[0:4])
        else:
            lista.append('')
        return lista            
    return lista


def fcod_funcionario(l_detalhe):

    result = re.search(r'[\d]{5}[A-Z\s\.]{3,45}',l_detalhe)
    if result is not None:
        string =result.group(0)
        return string

    return 'DESCONHECIDO'


def fcod_matricula(l_detalhe):
    string=l_detalhe[50:160]
    result = re.search(r'[\d]{2,12}[-]{1}[A-Z]?[\d]{4}',string)
    if result is not None:
        string=result.group(0)
        return string[0:len(string)-4]
    return ''


def fcod_provdesc(string):
    string1 = re.sub(r'[A-Z]{1}[\d]{4}[\s]{0,10}[\d]{0,3}[\.]{0,1}[\d]{0,3}[,]{1}[\d]{2}TOTAL DE SERVIDORES:','$$',string)
    string2=string1.split('$$')
    string3=string2[0]
    string4=re.sub(r'[A-Z]{1}[\d]{4}[\s]{0,10}[\d]{0,3}[\.]{0,1}[\d]{0,3}[\.]{0,1}[\d]{0,3}[\,]{0,1}[\d]{2}', '$$', string3)
    lista=string4.split('$$')
    return lista


def fproventos(l_linha,matricula):
    string1 = re.sub(matricula,'$$',l_linha)
    string2 = re.sub('VANTAGENS','$$', string1)
    string3 = string2.split('$$') 
    string4 = string3[1]

    

    lista = re.findall( r'[\d]{4}[A-Z]{1,2}', string4)
    for k in range(len(lista)):
        s1='$$'+lista[k]
        string4 = re.sub(lista[k],s1,string4)
    string5 = string4.split('$$')        
    return string5




def f_montaProventos(proventos):
    codigo = proventos[0:4]
    proventos = re.sub(r'30/30','',proventos)
    res = re.search(r'[\d]{0,4}[\.]?[\d]{1,3}[,]{1}[\d]{2}$', proventos)
    valor = res.group(0)
    return {'codigo':codigo,'valor':valor}













