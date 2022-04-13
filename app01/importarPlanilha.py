# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Secretaria,Vinculo,Evento,Setor,Planilha,Servidor,Folhames,Folhaevento,Refeventos,Funcao,Funcoes_cv,LogErro,Eventos_cv

from . import listagens,funcoes_gerais,funcoes_banco


def importarServidores(i_id_municipio,i_anomes,entidade,empresa):

    erro=0
    objetos=[]
    lista=[]
    lista_servidores=listagens.listagemServidores(i_id_municipio)
    lista_servidores_verificados=[]

    id_municipio=i_id_municipio
    anomes=i_anomes

    lista_incluidos=[]
    lista_cpf=[]
    codigo_folha=int(str(i_anomes)[4:6])

    queryP = Planilha.objects.values(
        'codigo',
        'nome_servidor',
        'data_admissao',
        'cpf'
        ).filter(entidade=entidade,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):


        codigo = queryP[qp]['codigo']
        nome_servidor = queryP[qp]['nome_servidor']
        cpf = queryP[qp]['cpf']
        data_admissao = queryP[qp]['data_admissao']


        nome_servidor=nome_servidor.strip()
        nome_servidor=funcoes_gerais.remove_combining_fluent(nome_servidor)
        cpf=cpf.strip()

        #srv = Servidor.objects.filter(id_municipio=id_municipio,cod_servidor=codigo).first()


        if codigo not in lista_servidores_verificados:
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
        lista_servidores_verificados.append(codigo)                

        
    Servidor.objects.bulk_create(objetos)
    return 1

def importarSetores(i_id_municipio,i_anomes,entidade,empresa):

    objetos=[]
    lista=[]
    carga_erro=[]
    ls_setores_verificados=[]

    lista_erro_secretaria=[]
    lista_setores=listagens.listagemSetores(i_id_municipio)

    dict_secretarias=listagens.criarDictSecretarias(i_id_municipio)
    lista_secretarias = listagens.listagemSecretarias(i_id_municipio)
    codigo_folha=int(str(i_anomes)[4:6])


    id_municipio=i_id_municipio
    anomes=i_anomes

    queryP = Planilha.objects.values(
        'codigo',
        'secretaria',
        'setor',
        'funcao'
        ).filter(entidade=entidade,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        setor = queryP[qp]['setor']
        secretaria = queryP[qp]['secretaria']

        if setor is not None and secretaria is not None:
            setor = setor.strip()
            secretaria = secretaria.strip()

            setor=funcoes_gerais.remove_combining_fluent(setor)
            secretaria=funcoes_gerais.remove_combining_fluent(secretaria)

            if setor+secretaria not in ls_setores_verificados:

                if secretaria in lista_secretarias:
                    id_secretaria = dict_secretarias[secretaria]
                    obj_sec = Secretaria.objects.get(pk=id_secretaria)
                else:
                    obj_sec=None
                    if secretaria not in lista_erro_secretaria:
                        lista_erro_secretaria.append(secretaria)


                    if len(setor)>2 and obj_sec is not None:
                        if secretaria+setor not in lista_setores:
                            if secretaria+setor not in lista:
                                objeto = Setor(
                                    id_municipio=i_id_municipio,
                                    secretaria=obj_sec,
                                    setor=setor
                                    )
                                lista.append(secretaria+setor)
                                objetos.append(objeto)
            ls_setores_verificados.append(setor+secretaria)
        
    if len(lista)>0:
        Setor.objects.bulk_create(objetos)

    if len(lista_erro_secretaria)>0:
        for kk in range(len(lista_erro_secretaria)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='secretaria',
                observacao=lista_erro_secretaria[kk]
                )
            carga_erro.append(obj)

    if len(lista_erro_secretaria)>0:
        LogErro.objects.bulk_create(carga_erro)

    return 1



def importarFolha(i_id_municipio,i_anomes,entidade,empresa):

    lista_erro_setor=[]
    lista_erro_secretaria=[]

    id_municipio=i_id_municipio
    anomes=i_anomes


    dict_secretarias=listagens.criarDictSecretarias(i_id_municipio)
    lista_secretarias = listagens.listagemSecretarias(i_id_municipio)

    dict_setores=listagens.criarDictSetores(i_id_municipio)
    lista_setores = listagens.listagemSetores(i_id_municipio)

    
    lista_funcoes = listagens.listagemFuncoes(empresa)
    dict_funcoes=listagens.criarDictFuncoes(empresa)

    lista_funcoes_cv = listagens.listagemFuncoes_cv()
    dict_funcoes_cv=listagens.criarDictFuncoes_cv()


    dict_vinculos=listagens.criarDictVinculos(i_id_municipio)
    lista_vinculos = listagens.listagemVinculos(i_id_municipio)

    listagem_folhames=listagens.listagemFolhames(i_id_municipio,i_anomes)

    lista_eventos = listagens.listagemEventos(empresa)
    dict_eventos=listagens.criarDictEventos(empresa)

    lista_eventos_cv = listagens.listagemEventos_cv()
    dict_eventos_cv=listagens.criarDictEventos_cv()



    dict_tipos_eventos=listagens.criarDictTiposDeEventos(empresa)
    dict_tipos_eventos_cv=listagens.criarDictTiposDeEventos_cv()

    lista=[]
    lista_eventosMes=[]

    objetos=[]
    feventos=[]
    lista_incluidos=[]

    lista_ref_eventos=[]
    obj_ref_ev=[]
    carga_erro=[]
    carga_folhaeventos=[]
    carga_folhames=[]
    carga_refeventos=[]


    codigo_folha=int(str(i_anomes)[4:6])

    #erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,'gravando log 2')
    #erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,entidade)
    #erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,str(codigo_folha))

    #erro=funcoes_gerais.gravarErro_01(i_id_municipio,i_anomes,entidade)


    
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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)


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

        secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
        setor=funcoes_gerais.remove_combining_fluent(setor)
        funcao=funcoes_gerais.remove_combining_fluent(funcao)
        vinculo=funcoes_gerais.remove_combining_fluent(vinculo)
        evento=funcoes_gerais.remove_combining_fluent(evento)


    
        if secretaria in lista_secretarias:
            id_secretaria = dict_secretarias[secretaria]
        else:
            id_secretaria=0            

        if id_secretaria==0:
            if secretaria is not None:
                if secretaria not in lista_erro_secretaria:
                    lista_erro_secretaria.append(secretaria)

        if secretaria+setor in lista_setores:
            id_setor = dict_setores[secretaria+setor]
        else:
            id_setor=0

        if id_setor==0:
            if setor is not None:
                if setor not in lista_erro_setor:
                    lista_erro_setor.append(str(cod_servidor)+': '+setor)

        if funcao in lista_funcoes:
            id_funcao = dict_funcoes[funcao]
        elif funcao in lista_funcoes_cv:
            id_funcao = dict_funcoes_cv[funcao]
        else:
            id_funcao=0

        if vinculo in lista_vinculos:
            id_vinculo = dict_vinculos[vinculo]
        else:
            id_vinculo=0            

        if evento in lista_eventos:
            id_evento = dict_eventos[evento]
            tipo = dict_tipos_eventos[id_evento]
        elif evento in lista_eventos_cv:
            id_evento = dict_eventos_cv[evento]
            tipo = dict_tipos_eventos_cv[id_evento]
        else:
            id_evento=0
            tipo=''

        if cpf is None:
            cpf=''

        if valor is None:
            valor=0

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

            carga_folhaeventos.append(obj_feventos)
            lista_eventosMes.append(str(cod_servidor)+'-'+str(cod_evento))
        
        if cod_servidor not in lista_incluidos:
            if str(cod_servidor)+'-'+str(i_anomes) not in listagem_folhames:
                objeto_folhames = Folhames(
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

                carga_folhames.append(objeto_folhames)
                lista_incluidos.append(cod_servidor)
        if evento=='VENCIMENTO BASE':
            if cod_servidor not in lista_ref_eventos:
                ref_ev = Refeventos(
                    anomes=anomes,
                    id_municipio=id_municipio,
                    cod_servidor=cod_servidor,
                    ref_eventos = dias
                    )

                carga_refeventos.append(ref_ev)
                lista_ref_eventos.append(cod_servidor)

    if len(lista_erro_secretaria)>0:
        for kk in range(len(lista_erro_secretaria)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='secretaria',
                observacao=lista_erro_secretaria[kk]
                )
            carga_erro.append(obj)

    if len(lista_erro_setor)>0:
        for kk in range(len(lista_erro_setor)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='setor',
                observacao=lista_erro_setor[kk]
                )
            carga_erro.append(obj)

    if len(lista_erro_setor)>0:                
        LogErro.objects.bulk_create(carga_erro)

    Folhames.objects.bulk_create(carga_folhames)
    Folhaevento.objects.bulk_create(carga_folhaeventos)
    Refeventos.objects.bulk_create(carga_refeventos)
    return 1




def importarSecFuncVincEventos(i_id_municipio,i_anomes,entidade,empresa):


    carga_secretaria=[]
    carga_funcao=[]
    carga_vinculo=[]
    carga_evento=[]
    carga_evento2=[]
    carga_funcao=[]

    ls_evento_verificado=[]
    ls_funcao_verificada=[]
    ls_vinculo_verificado=[]
    ls_secretaria_verificada=[]


    id_municipio=i_id_municipio
    anomes=i_anomes


    ls_secretaria=[]
    ls_funcao=[]
    ls_vinculo=[]
    ls_evento=[]
    ls_eventos_campos=[]
    ls_funcoes_campos=[]

    codigo_folha=int(str(i_anomes)[4:6])


    lista_secretarias=listagens.listagemSecretarias(i_id_municipio)

    lista_funcoes=listagens.listagemFuncoes(empresa)
    lista_funcoes_cv=listagens.listagemFuncoes_cv()

    lista_vinculos=listagens.listagemVinculos(i_id_municipio)

    lista_eventos=listagens.listagemEventos(empresa)
    lista_eventos_cv=listagens.listagemEventos_cv()


    arquivo_ok=0

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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)



    for qp in range(len(queryP)):
        arquivo_ok=1

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
            secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
            if secretaria not in ls_secretaria_verificada:
                if len(secretaria)>2:
                    if secretaria not in lista_secretarias:
                        if secretaria not in ls_secretaria:
                            obj_secretaria = Secretaria(
                                id_municipio=i_id_municipio,
                                secretaria=secretaria
                                )
                            ls_secretaria.append(secretaria)
                            carga_secretaria.append(obj_secretaria)
        ls_secretaria_verificada.append(secretaria)                        

        if vinculo is not None:
            vinculo=vinculo.strip()
            if len(vinculo)>2:

                vinculo=funcoes_gerais.remove_combining_fluent(vinculo)
                if vinculo not in ls_vinculo_verificado:
                    if vinculo not in lista_vinculos:
                        if vinculo not in ls_vinculo:
                            obj_vinculo = Vinculo(
                                id_municipio=i_id_municipio,
                                vinculo=vinculo
                                )
                            ls_vinculo.append(vinculo)
                            carga_vinculo.append(obj_vinculo)
        ls_vinculo_verificado.append(vinculo)                        

        if evento is not None:
            evento=evento.strip()
            if len(evento)>2:
                evento=funcoes_gerais.remove_combining_fluent(evento)
                if evento not in ls_evento_verificado:
                    ev1=Evento.objects.filter(empresa=empresa,evento=evento).first()
                    if ev1 is None:
                        ev2=Eventos_cv.objects.filter(evento=evento).first()
                        if ev2 is None:
                            evento_new=Eventos_cv(
                                evento=evento,
                                tipo=tipo_evento,
                                cancelado='N'
                                )
                            evento_new.save()
                            ev2=Eventos_cv.objects.filter(evento=evento).first()
                            id_evento_cv=ev2.id_evento_cv
                        else:
                            id_evento_cv=ev2.id_evento_cv
                        evento_new=Evento(
                            empresa=empresa,
                            tipo=tipo_evento,
                            evento=evento,
                            cancelado='N',
                            exibe_excel=1,
                            ordenacao=0,
                            cl_orcamentaria='O',
                            id_evento_cv=id_evento_cv
                            )
                        evento_new.save()
        ls_evento_verificado.append(evento)

        '''
        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                funcao=funcoes_gerais.remove_combining_fluent(funcao)
                if funcao not in ls_funcao_verificada:
                    ev1=Funcao.objects.filter(empresa=empresa,funcao=funcao).first()
                    if ev1 is None:
                        ev2=Funcoes_cv.objects.filter(funcao=funcao).first()
                        if ev2 is None:
                            funcao_new=Funcoes_cv(
                                funcao=funcao,
                                cancelado='N'
                                )
                            funcao_new.save()
                            ev2=Funcoes_cv.objects.filter(funcao=funcao).first()
                            id_funcao_cv=ev2.id_funcao_cv
                        else:
                            id_funcao_cv=ev2.id_funcao_cv
                        funcao_new=Funcao(
                            empresa=empresa,
                            funcao=funcao,
                            id_funcao_cv=id_funcao_cv
                            )
                        funcao_new.save()


        ls_funcao_verificada.append(funcao)                            .
        '''


    if len(ls_secretaria)>0:
        Secretaria.objects.bulk_create(carga_secretaria)
    if len(ls_vinculo)>0:        
        Vinculo.objects.bulk_create(carga_vinculo)        

    obj=LogErro(
        id_municipio=id_municipio,
        anomes=anomes,
        numero_linha=0,
        codigo='secretaria',
        observacao='teste'
        )
    obj.save()

    if len(ls_evento)>0:
        for kk in range(len(ls_evento)):
            obje=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='evento',
                observacao=ls_evento[kk]
                )
            carga_evento2.append(obje)
    LogErro.objects.bulk_create(carga_evento2)
    return 1


def importarSecFuncVincEventos2(i_id_municipio,i_anomes,entidade,empresa):


    carga_secretaria=[]
    carga_funcao=[]
    carga_vinculo=[]
    carga_evento=[]


    ls_secretaria=[]
    ls_funcao=[]
    ls_vinculo=[]
    ls_evento=[]
    ls_eventos_campos=[]
    ls_funcoes_campos=[]

    codigo_folha=int(str(i_anomes)[4:6])


    lista_secretarias=listagens.listagemSecretarias(i_id_municipio)

    lista_funcoes=listagens.listagemFuncoes(empresa)
    lista_funcoes_cv=listagens.listagemFuncoes_cv()

    lista_vinculos=listagens.listagemVinculos(i_id_municipio)

    lista_eventos=listagens.listagemEventos(empresa)
    lista_eventos_cv=listagens.listagemEventos_cv()


    arquivo_ok=0

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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)



    for qp in range(len(queryP)):
        arquivo_ok=1

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
            secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
            if len(secretaria)>2:
                if secretaria not in lista_secretarias:
                    if secretaria not in ls_secretaria:
                        obj_secretaria = Secretaria(
                            id_municipio=i_id_municipio,
                            secretaria=secretaria
                            )
                        ls_secretaria.append(secretaria)
                        carga_secretaria.append(obj_secretaria)

        
        if vinculo is not None:
            vinculo=vinculo.strip()
            if len(vinculo)>2:
                vinculo=funcoes_gerais.remove_combining_fluent(vinculo)
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
                evento=funcoes_gerais.remove_combining_fluent(evento)
                if pesquisaEvento(evento,lista_eventos,lista_eventos_cv):
                    if evento not in ls_evento:
                        obj_new = Eventos_cv(
                            evento=evento,
                            tipo=tipo_evento,
                            cancelado='N'
                            )
                        carga_evento.append(obj_new)
                        ls_evento.append(evento)

        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                funcao=funcoes_gerais.remove_combining_fluent(funcao)
                if pesquisaFuncao(funcao,lista_funcoes,lista_funcoes_cv):
                    if funcao not in ls_funcao:
                        obj_new = Funcoes_cv(
                            funcao=funcao,
                            cancelado='N'
                            )
                        carga_funcao.append(obj_new)
                        ls_funcao.append(funcao)

    if arquivo_ok==0:
        return 0
    Secretaria.objects.bulk_create(carga_secretaria)
    Funcoes_cv.objects.bulk_create(carga_funcao)
    Vinculo.objects.bulk_create(carga_vinculo)
    Eventos_cv.objects.bulk_create(carga_evento)
    return 1


def pesquisaFuncao(funcao,lista1,lista2):
    if funcao not in lista1:
        if funcao not in lista2:
            return True
    return False


def pesquisaEvento(evento,lista1,lista2):
    if evento not in lista1:
        if evento not in lista2:
            return True
    return False




