# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Secretaria,Vinculo,Funcao,Evento,Setor,Planilha,Servidor,Folhames,Folhaevento,Refeventos
from . import listagens,funcoes_gerais



def importarServidores(i_id_municipio,i_anomes,i_municipio):

    erro=0
    objetos=[]
    lista=[]
    lista_servidores=listagens.listagemServidores(i_id_municipio)

    lista_incluidos=[]
    lista_cpf=[]
    codigo_folha=int(str(i_anomes)[4:6])



    queryP = Planilha.objects.values(
        'codigo',
        'nome_servidor',
        'data_admissao',
        'cpf'
        ).filter(entidade=i_municipio,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        codigo = queryP[qp]['codigo']
        nome_servidor = queryP[qp]['nome_servidor']
        cpf = queryP[qp]['cpf']
        data_admissao = queryP[qp]['data_admissao']


        nome_servidor=nome_servidor.strip()
        cpf=cpf.strip()


        if str(codigo) not in lista_servidores:
            if str(codigo) not in lista_incluidos:
                objeto = Servidor(
                    id_municipio=i_id_municipio,
                    cod_servidor=codigo,
                    nome = nome_servidor,
                    cpf = cpf,
                    data_admissao = data_admissao
                    )
                objetos.append(objeto)
                lista_incluidos.append(str(codigo))
        
    Servidor.objects.bulk_create(objetos)
    return ''


def importarSetores(i_id_municipio,i_anomes,i_municipio):

    objetos=[]
    lista=[]
    lista_setores=listagens.listagemSetores(i_id_municipio)

    dict_secretarias=listagens.criarDictSecretarias(i_id_municipio)
    lista_secretarias = listagens.listagemSecretarias(i_id_municipio)
    codigo_folha=int(str(i_anomes)[4:6])



    queryP = Planilha.objects.values(
        'codigo',
        'secretaria',
        'setor',
        'funcao'
        ).filter(entidade=i_municipio,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        setor = queryP[qp]['setor']
        secretaria = queryP[qp]['secretaria']

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
                                id_municipio=i_id_municipio,
                                secretaria=obj_sec,
                                setor=setor
                                )
                            lista.append(secretaria+setor)
                            objetos.append(objeto)
        
    Setor.objects.bulk_create(objetos)
    return None




def importarFolha(i_id_municipio,i_anomes,i_municipio):


    #dict_secretarias=listagens.dictSecretarias(id_municipio)
    dict_secretarias=listagens.criarDictSecretarias(i_id_municipio)
    lista_secretarias = listagens.listagemSecretarias(i_id_municipio)

    #dict_setores=listagens.dictSetores(id_municipio)
    dict_setores=listagens.criarDictSetores(i_id_municipio)
    lista_setores = listagens.listagemSetores(i_id_municipio)

    #dict_funcoes=listagens.dictFuncoes(id_municipio)
    dict_funcoes=listagens.criarDictFuncoes(i_id_municipio)
    lista_funcoes = listagens.listagemFuncoes(i_id_municipio)


    #dict_vinculos=listagens.dictVinculos(id_municipio)
    dict_vinculos=listagens.criarDictVinculos(i_id_municipio)
    lista_vinculos = listagens.listagemVinculos(i_id_municipio)

    #dict_eventos=listagens.dictEventos(id_municipio)
    dict_eventos=listagens.criarDictEventos(i_id_municipio)
    lista_eventos = listagens.listagemEventos(i_id_municipio)

    #dict_tipos_eventos=listagens.dictTiposEventos(id_municipio)
    dict_tipos_eventos=listagens.criarDictTiposDeEventos(i_id_municipio)


    listagem_folhames=listagens.listagemFolhames(i_id_municipio,i_anomes)

    lista_grupo_eventos=listagens.listagemGrupoEventos(i_id_municipio)
    dict_grupo_eventos=listagens.criarDictGrupoEventos(i_id_municipio)



    lista=[]
    lista_eventosMes=[]

    objetos=[]
    feventos=[]
    lista_incluidos=[]

    lista_ref_eventos=[]
    obj_ref_ev=[]


    codigo_folha=int(str(i_anomes)[4:6])
    
    queryP = Planilha.objects.values(
        'codigo',
        'cpf',
        'secretaria',
        'setor',
        'funcao',
        'tipo_admissao',
        'previdencia',
        'carga_horaria',
        'ref_evento',
        'classificacao',
        'evento',
        'cod_evento',
        'tipo',
        'valor_evento'
        ).filter(entidade=i_municipio,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        cod_servidor = queryP[qp]['codigo']
        cpf = queryP[qp]['cpf']
        secretaria = queryP[qp]['secretaria']
        setor = queryP[qp]['setor']
        funcao = queryP[qp]['funcao']
        vinculo = queryP[qp]['tipo_admissao']
        previdencia = queryP[qp]['previdencia']
        cl_orcamentaria = queryP[qp]['classificacao']
        evento = queryP[qp]['evento']
        cod_evento = queryP[qp]['cod_evento']
        tipo = queryP[qp]['tipo']
        valor = queryP[qp]['valor_evento']
        carga_horaria = queryP[qp]['carga_horaria']
        dias = queryP[qp]['ref_evento']

        
        secretaria=secretaria.strip()
        setor=setor.strip()    
        funcao=funcao.strip()    
        vinculo=vinculo.strip()    
        previdencia=previdencia.strip()
        evento=evento.strip()

        if evento in lista_grupo_eventos:
            evento1 = dict_grupo_eventos[evento]
        else:
            evento1 = evento

        evento = evento1

    
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
        

        if cpf is None:
            cpf=''

        if valor is None:
            valor=0

        if id_secretaria==0:
            observacao='cod_servidor: '+str(cod_servidor)+' - secretaria'
            erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,observacao)
        if id_setor==0:
            observacao='cod_servidor: '+str(cod_servidor)+' - setor'
            erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,observacao)
        if id_vinculo==0:
            observacao='cod_servidor: '+str(cod_servidor)+' - vinculo'
            erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,observacao)
        if id_funcao==0:
            observacao='cod_servidor: '+str(cod_servidor)+' - funcao'
            erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,observacao)
        if id_evento==0:
            observacao='cod_servidor: '+str(cod_servidor)+' - evento'
            erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,observacao)

        
        if previdencia=='PREVIDÊNCIA MUNICIPAL':
            previdencia='M'
        elif previdencia=='INSS':
            previdencia='I'
        elif previdencia=='NÃO PAGA':
            previdencia='N'
        else:
            previndencia=''

        '''            
        
        if str(cod_servidor)+'-'+str(cod_evento) not in lista_eventosMes:
            obj_feventos = Folhaevento(
                    id_municipio = i_id_municipio,
                    anomes = i_anomes,
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
            if str(cod_servidor)+'-'+str(i_anomes) not in listagem_folhames:
                objeto = Folhames(
                    anomes=i_anomes,
                    id_municipio=i_id_municipio,
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
        if evento=='VENCIMENTO BASE':
            if cod_servidor not in lista_ref_eventos:
                ref_ev = Refeventos(
                    anomes=i_anomes,
                    id_municipio=i_id_municipio,
                    cod_servidor=cod_servidor,
                    ref_eventos = dias
                    )

                obj_ref_ev.append(ref_ev)
                lista_ref_eventos.append(cod_servidor)

        '''
    #Folhames.objects.bulk_create(objetos)
    #Folhaevento.objects.bulk_create(feventos)
    #Refeventos.objects.bulk_create(obj_ref_ev)
    return ''


def importarSecFuncVincEventos2(i_id_municipio,i_anomes,i_municipio):


    carga_secretaria=[]
    carga_funcao=[]
    carga_vinculo=[]
    carga_evento=[]


    ls_secretaria=[]
    ls_funcao=[]
    ls_vinculo=[]
    ls_evento=[]

    codigo_folha=int(str(i_anomes)[4:6])


    lista_secretarias=listagens.listagemSecretarias(i_id_municipio)
    lista_funcoes=listagens.listagemFuncoes(i_id_municipio)
    lista_vinculos=listagens.listagemVinculos(i_id_municipio)
    lista_eventos=listagens.listagemEventos(i_id_municipio)



    queryP = Planilha.objects.values(
        'codigo',
        'secretaria',
        'setor',
        'funcao',
        'evento',
        'cod_evento',
        'tipo',
        'tipo_admissao',
        'classificacao'
        ).filter(entidade=i_municipio,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):
        '''
        print (queryP[qp]['secretaria'])
        print (queryP[qp]['setor'])
        print (queryP[qp]['funcao'])
        print (queryP[qp]['tipo_admissao'])
        print (queryP[qp]['evento'])
        print ('--------------------')
        '''


        if queryP[qp]['tipo']==4:
            tipo_evento='D'
        elif queryP[qp]['tipo'] in [1,2,3]:
            tipo_evento='V'
        else:
            tipo_evento='V'            


        cod_evento=queryP[qp]['cod_evento']
        evento=queryP[qp]['evento']
        classificacao=queryP[qp]['classificacao']

        secretaria=queryP[qp]['secretaria']
        funcao=queryP[qp]['funcao']
        vinculo=queryP[qp]['tipo_admissao']

        
        if secretaria is not None:
            secretaria=secretaria.strip()
            if len(secretaria)>2:
                if secretaria not in lista_secretarias:
                    if secretaria not in ls_secretaria:
                        obj_secretaria = Secretaria(
                            id_municipio=i_id_municipio,
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
                            id_municipio=i_id_municipio,
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
                            id_municipio=i_id_municipio,
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
                            id_municipio=i_id_municipio,
                            evento=evento,
                            codigo=cod_evento,
                            tipo = tipo_evento,
                            cl_orcamentaria = classificacao
                            )
                        ls_evento.append(evento)
                        carga_evento.append(obj_evento)

    Secretaria.objects.bulk_create(carga_secretaria)
    Funcao.objects.bulk_create(carga_funcao)
    Vinculo.objects.bulk_create(carga_vinculo)
    Evento.objects.bulk_create(carga_evento)

    return None

