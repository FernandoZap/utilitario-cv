# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
import datetime
from openpyxl.styles import NamedStyle
from .models import Secretaria,Vinculo,Evento,Setor,Planilha,Servidor,Folhames,Folhaevento,Refeventos,Eventos_cv,Funcao,Funcoes_cv
from . import listagens,funcoes_gerais,funcoes_banco



def importarServidores(i_id_municipio,i_anomes,entidade,empresa):

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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):

        if qp==0:
            print ('programa: importarServidores')



        codigo = queryP[qp]['codigo']
        nome_servidor = queryP[qp]['nome_servidor']
        cpf = queryP[qp]['cpf']
        data_admissao = queryP[qp]['data_admissao']


        nome_servidor=nome_servidor.strip()
        nome_servidor=funcoes_gerais.to_ascii_string(nome_servidor)
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
    return 1


def importarSetores(i_id_municipio,i_anomes,entidade,empresa):

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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)

    for qp in range(len(queryP)):


        if qp==0:
            print ('programa: importarSetores')



        setor = queryP[qp]['setor']
        secretaria = queryP[qp]['secretaria']

        if setor is not None:
            setor = setor.strip()
            setor=funcoes_gerais.to_ascii_string(setor)
            secretaria = secretaria.strip()
            secretaria=funcoes_gerais.to_ascii_string(secretaria)

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
    return 1




def importarFolha(i_id_municipio,i_anomes,entidade,empresa):


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
        ).filter(entidade=entidade,codigo_folha=codigo_folha)

    print ('entidade: '+entidade)
    print ('codigo_folha: '+str(codigo_folha))

    for qp in range(len(queryP)):

        if qp==0:
            print ('programa: importarFolha')


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

        '''
        secretaria=funcoes_gerais.to_ascii_string(secretaria)
        setor=funcoes_gerais.to_ascii_string(setor)
        funcao=funcoes_gerais.to_ascii_string(funcao)
        vinculo=funcoes_gerais.to_ascii_string(vinculo)
        evento=funcoes_gerais.to_ascii_string(evento)
        '''


        # trocar as varições de evento por um único evento para deixar todos
        # com uma única denominação; por exemplo:
        '''
          sempre que houver um desses eventos "GRATIFICACAO 1" , "GRATIFICACAO 2" e "GRATIFICACAO A1"
          trocar por "GRATIFICACAO".

        ''' 
    
        if secretaria in lista_secretarias:
            id_secretaria = dict_secretarias[secretaria]
        else:
            id_secretaria=0            

        if id_secretaria==0:            
            secretaria = funcoes_gerais.to_ascii_string(secretaria)
            if secretaria in lista_secretarias:
                id_secretaria = dict_secretarias[secretaria]
            else:
                id_secretaria=0            


        if secretaria+setor in lista_setores:
            id_setor = dict_setores[secretaria+setor]
        else:
            id_setor=0


        if id_setor==0:
            setor = funcoes_gerais.to_ascii_string(setor)
            if secretaria+setor in lista_setores:
                id_setor = dict_setores[secretaria+setor]



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

        if id_evento==0:
            evento=funcoes_gerais.to_ascii_string(evento)
            if evento in lista_eventos:
                id_evento = dict_eventos[evento]
                tipo = dict_tipos_eventos[id_evento]
            elif evento in lista_eventos_cv:
                id_evento = dict_eventos_cv[evento]
                tipo = dict_tipos_eventos_cv[id_evento]


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

    Folhames.objects.bulk_create(objetos)
    Folhaevento.objects.bulk_create(feventos)
    Refeventos.objects.bulk_create(obj_ref_ev)
    return 1


def importarSecFuncVincEventos(i_id_municipio,i_anomes,entidade,empresa):


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
        '''
        print (queryP[qp]['secretaria'])
        print (queryP[qp]['setor'])
        print (queryP[qp]['funcao'])
        print (queryP[qp]['tipo_admissao'])
        print (queryP[qp]['evento'])
        print ('--------------------')
        '''
        arquivo_ok=1

        if qp==0:
            print ('programa: importarSecFuncVincEventos')


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
                secretaria=funcoes_gerais.to_ascii_string(secretaria)
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
                vinculo=funcoes_gerais.to_ascii_string(vinculo)
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
                if pesquisaEvento(evento,lista_eventos,lista_eventos_cv):
                    if evento not in ls_evento:
                        evento_e=funcoes_gerais.to_ascii_string(evento)
                        obj_new = Eventos_cv(
                            evento=evento_e,
                            tipo=tipo_evento,
                            cancelado='N'
                            )
                        carga_evento.append(obj_new)
                        ls_evento.append(evento)

        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                if pesquisaFuncao(funcao,lista_funcoes,lista_funcoes_cv):
                    if funcao not in ls_funcao:
                        funcao_f=funcoes_gerais.to_ascii_string(funcao)
                        obj_new = Funcoes_cv(
                            funcao=funcao_f,
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
    sf1=funcao
    sf2=funcoes_gerais.to_ascii_string(funcao)
    if sf1 not in lista1:
        if sf2 not in lista1:
            if sf1 not in lista2:
                if sf2 not in lista1:
                    return True
    return False


def pesquisaEvento(evento,lista1,lista2):
    sf1=evento
    sf2=funcoes_gerais.to_ascii_string(evento)
    if sf1 not in lista1:
        if sf2 not in lista1:
            if sf1 not in lista2:
                if sf2 not in lista1:
                    return True
    return False




