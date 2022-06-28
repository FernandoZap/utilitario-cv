# -*- coding: utf-8 -*-
import openpyxl, pprint
import os
import sys
from datetime import datetime
from django.db.models import Count,Sum
from openpyxl.styles import NamedStyle
from .models import Secretaria,Vinculo,Setor,Servidor,Folhames,Folhaevento,Refeventos,LogErro,Funcao,Evento,Funcionario,Provento,Complemento

from . import listagens,funcoes_gerais,funcoes_banco
from django.db import connection


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def importarServidores(id_municipio,anomes,empresa):

    erro=0
    objetos=[]
    lista=[]
    lista_servidores=listagens.listagemServidores(id_municipio)
    lista_servidores_verificados=[]

    lista_incluidos=[]
    lista_cpf=[]


    queryP = Funcionario.objects.values(
        'codigo',
        'nome_servidor',
        'data_admissao').annotate(Count('codigo')).filter(id_municipio=id_municipio,anomes=anomes)

    for qp in range(len(queryP)):



        codigo = queryP[qp]['codigo']
        nome_servidor = queryP[qp]['nome_servidor']
        data_admissao = queryP[qp]['data_admissao']
        dt_admissao = datetime.strptime(data_admissao, '%Y-%m-%d').date()


        nome_servidor=nome_servidor.strip()
        nome_servidor=funcoes_gerais.remove_combining_fluent(nome_servidor)
        nome_servidor=nome_servidor.upper()

        #srv = Servidor.objects.filter(id_municipio=id_municipio,cod_servidor=codigo).first()


        if codigo not in lista_servidores_verificados:
            if str(codigo) not in lista_servidores:
                if codigo not in lista_incluidos:
                    objeto = Servidor(
                        id_municipio=id_municipio,
                        cod_servidor=codigo,
                        nome = nome_servidor,
                        data_admissao = dt_admissao
                        )
                    objetos.append(objeto)
                    lista_incluidos.append(codigo)
            lista_servidores_verificados.append(codigo)                

        
    Servidor.objects.bulk_create(objetos)
    return 1

def importarSetores(id_municipio,anomes,empresa):

    objetos=[]
    lista=[]
    carga_erro=[]
    ls_setores_verificados=[]
    carga_setor=[]

    lista_erro_secretaria=[]
    lista_setores=listagens.listagemSetores2(id_municipio)

    dict_secretarias=listagens.criarDictSecretarias(id_municipio)
    lista_secretarias = listagens.listagemSecretarias(id_municipio)


    codigo_folha=int(str(anomes)[4:6])


    qtd_funcao=0

    queryP=Funcionario.objects.values(
        'secretaria',
        'setor').annotate(Count('secretaria')).filter(id_municipio=id_municipio,anomes=anomes).order_by('secretaria')

    for qp in range(len(queryP)):

        setor = queryP[qp]['setor']
        secretaria = queryP[qp]['secretaria']

        if setor is not None and secretaria is not None:
            setor = setor.strip()
            secretaria = secretaria.strip()
            seto=setor.upper()
            secretaria=secretaria.upper()

            setor=funcoes_gerais.remove_combining_fluent(setor)
            secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
            id_secretaria = dict_secretarias[secretaria]

            if str(id_secretaria)+setor not in ls_setores_verificados:

                if secretaria in lista_secretarias:
                    obj_sec = Secretaria.objects.get(pk=id_secretaria)
                    if obj_sec is not None:
                        if len(setor)>2:
                            if str(id_secretaria)+setor not in lista_setores:
                                if str(id_secretaria)+setor not in lista:
                                    objeto = Setor(
                                        id_municipio=id_municipio,
                                        secretaria=obj_sec,
                                        setor=setor
                                        )
                                    lista.append(str(id_secretaria)+setor)
                                    carga_setor.append(objeto)

                ls_setores_verificados.append(str(id_secretaria)+setor)

    '''        
    if len(lista_setores)>0:
        for k in range(len(lista_setores)):
            print (lista_setores[k])
    print('------------------------------')            
    if len(lista)>0:
        for k in range(len(lista)):
            print (lista[k])

    '''
    
    if len(lista)>0:    
        Setor.objects.bulk_create(carga_setor)

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


def importarSecretaria(id_municipio,anomes,empresa):

    carga_secretaria=[]
 
    ls_secretaria_verificada=[]

    ls_secretaria=[]
 
    codigo_folha=int(str(anomes)[4:6])


    lista_secretarias=listagens.listagemSecretarias(id_municipio)

    arquivo_ok=0

    queryP=Funcionario.objects.values(
        'secretaria').annotate(Count('secretaria')).filter(id_municipio=id_municipio,anomes=anomes).order_by('secretaria')


    for qp in range(len(queryP)):
        arquivo_ok=1

        secretaria=queryP[qp]['secretaria']
        secretaria=secretaria.upper()

    
        if secretaria is not None:
            secretaria=secretaria.strip()
            secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
            if secretaria not in ls_secretaria_verificada:
                if len(secretaria)>2:
                    if secretaria not in lista_secretarias:
                        if secretaria not in ls_secretaria:
                            obj_secretaria = Secretaria(
                                id_municipio=id_municipio,
                                secretaria=secretaria
                                )
                            ls_secretaria.append(secretaria)
                            carga_secretaria.append(obj_secretaria)
            ls_secretaria_verificada.append(secretaria)                        


    if len(ls_secretaria)>0:
        Secretaria.objects.bulk_create(carga_secretaria)

    return 1



def importarFuncao(id_municipio,anomes,empresa):


    carga_funcao=[]

    ls_funcao_verificada=[]

    ls_funcao=[]
    ls_funcoes_campos=[]

    codigo_folha=int(str(anomes)[4:6])

    lista_funcoes=listagens.listagemFuncoes(id_municipio)

    arquivo_ok=0

    queryP=Funcionario.objects.values(
        'funcao').annotate(Count('funcao')).filter(id_municipio=id_municipio,anomes=anomes).order_by('funcao')


    for qp in range(len(queryP)):
        arquivo_ok=1


        funcao=queryP[qp]['funcao']
        funcao=funcao.upper()

        if funcao is not None:
            funcao=funcao.strip()
            if len(funcao)>2:
                funcao=funcoes_gerais.remove_combining_fluent(funcao)
                if funcao not in ls_funcao_verificada:
                    ev1=Funcao.objects.filter(id_municipio=id_municipio,funcao=funcao).first()
                    if ev1 is None:
                        funcao_new=Funcao(
                            id_municipio=id_municipio,
                            empresa=empresa,
                            funcao=funcao,
                            id_funcao_cv=0,
                            cancelado='N'
                            )
                        carga_funcao.append(funcao_new)


            ls_funcao_verificada.append(funcao) 


    if len(carga_funcao)>0:
        Funcao.objects.bulk_create(carga_funcao)        

    return 1





def importarEventos(id_municipio,anomes,empresa):


    carga_evento=[]

    ls_evento_verificado=[]


    ls_evento=[]
    ls_eventos_campos=[]

    codigo_folha=int(str(anomes)[4:6])


    lista_eventos=listagens.listagemEventos(id_municipio)


    arquivo_ok=0

    queryP=Provento.objects.values(
        'evento','tipo').annotate(Count('evento')).filter(id_municipio=id_municipio,anomes=anomes).order_by('evento')


    for qp in range(len(queryP)):
        arquivo_ok=1

        if queryP[qp]['tipo']==4:
            tipo_evento='D'
        elif queryP[qp]['tipo'] in [1,2,3]:
            tipo_evento='V'
        else:
            tipo_evento='V'

        evento=queryP[qp]['evento']
        evento=evento.upper()
        #classificacao=queryP[qp]['classificacao']

        if evento is not None:
            evento=evento.strip()
            if len(evento)>2:
                evento=funcoes_gerais.remove_combining_fluent(evento)
                if evento not in ls_evento_verificado:
                    ev1=Evento.objects.filter(id_municipio=id_municipio,evento=evento).first()
                    if ev1 is None:
                        evento_new=Evento(
                            empresa=empresa,
                            id_municipio=id_municipio,
                            evento=evento,
                            tipo=tipo_evento,
                            exibe_excel=1,
                            ordenacao=0,
                            cl_orcamentaria='O',
                            cancelado='N',
                            id_evento_cv=0
                            )
                        carga_evento.append(evento_new)
                        ls_evento.append(evento)
            ls_evento_verificado.append(evento)


    if len(carga_evento)>0:
        Evento.objects.bulk_create(carga_evento)        

    return 1



def importarVinculos(id_municipio,anomes,empresa):

    carga_vinculo=[]
    ls_vinculo_verificado=[]
    ls_vinculo=[]
    codigo_folha=int(str(anomes)[4:6])
    lista_vinculos=listagens.listagemVinculos(id_municipio)
    arquivo_ok=0
    queryP = Funcionario.objects.values(
        'codigo',
        'tipo_admissao',
        ).filter(id_municipio=id_municipio,anomes=anomes)

    for qp in range(len(queryP)):

        vinculo=queryP[qp]['tipo_admissao']

        if vinculo is not None:
            vinculo=vinculo.upper()
            vinculo=vinculo.strip()
            if len(vinculo)>2:

                vinculo=funcoes_gerais.remove_combining_fluent(vinculo)
                if vinculo not in ls_vinculo_verificado:
                    if vinculo not in lista_vinculos:
                        if vinculo not in ls_vinculo:
                            obj_vinculo = Vinculo(
                                id_municipio=id_municipio,
                                vinculo=vinculo
                                )
                            ls_vinculo.append(vinculo)
                            carga_vinculo.append(obj_vinculo)
            ls_vinculo_verificado.append(vinculo)                        

    if len(ls_vinculo)>0:
        Vinculo.objects.bulk_create(carga_vinculo)        

    return 1


def importarFolhaPasso1(id_municipio,anomes,empresa):

    lista_erro_setor=[]
    lista_erro_secretaria=[]
    lista_erro_funcao=[]


    dict_secretarias=listagens.criarDictSecretarias(id_municipio)
    lista_secretarias = listagens.listagemSecretarias(id_municipio)

    dict_setores=listagens.criarDictSetores(id_municipio)
    lista_setores = listagens.listagemSetores(id_municipio)

    
    lista_funcoes = listagens.listagemFuncoes(id_municipio)
    dict_funcoes=listagens.criarDictFuncoes(id_municipio)


    dict_vinculos=listagens.criarDictVinculos(id_municipio)
    lista_vinculos = listagens.listagemVinculos(id_municipio)

    listagem_folhames=listagens.listagemFolhames(id_municipio,anomes)



    lista=[]

    objetos=[]
    feventos=[]
    lista_incluidos=[]

    lista_ref_eventos=[]
    obj_ref_ev=[]
    carga_erro=[]
    carga_folhaeventos=[]
    carga_folhames=[]
    carga_refeventos=[]

    carga_erro_secretaria=[]
    carga_erro_setor=[]
    carga_erro_funcao=[]


    codigo_folha=int(str(anomes)[4:6])
    '''
    queryP = Funcionario.objects.values(
        'codigo',
        'secretaria',
        'setor',
        'funcao',
        'tipo_admissao',
        'previdencia',
        'carga_horaria'
        ).filter(id_municipio=id_municipio,anomes=anomes)
    '''


    cursor = connection.cursor()
    cursor.execute("select f.*,c.ref_evento from funcionarios f left join complementos c on c.id_municipio=f.id_municipio and \
        c.anomes=f.anomes and c.codigo=f.codigo \
        where f.id_municipio=%s and f.anomes=%s",[id_municipio, anomes])

    queryP = dictfetchall(cursor)


    for qp in queryP:

        cod_servidor = qp['codigo']
        secretaria = qp['secretaria']
        setor = qp['setor']
        funcao = qp['funcao']
        vinculo =qp['tipo_admissao']
        previdencia = qp['previdencia']
        carga_horaria = qp['carga_horaria']
        ref_evento = qp['ref_evento']
        
        secretaria=secretaria.strip()
        setor=setor.strip()    
        funcao=funcao.strip()    
        vinculo=vinculo.strip()    
        previdencia=previdencia.strip()

        secretaria=secretaria.upper()
        setor=setor.upper()
        funcao=funcao.upper()
        vinculo=vinculo.upper()
        previdencia=previdencia.upper()


        secretaria=funcoes_gerais.remove_combining_fluent(secretaria)
        setor=funcoes_gerais.remove_combining_fluent(setor)
        funcao=funcoes_gerais.remove_combining_fluent(funcao)
        vinculo=funcoes_gerais.remove_combining_fluent(vinculo)
    
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
                    lista_erro_setor.append(setor)

        if funcao in lista_funcoes:
            id_funcao = dict_funcoes[funcao]
        else:
            id_funcao=0

        if id_funcao==0:
            if funcao is not None:
                if funcao not in lista_erro_funcao:
                    lista_erro_funcao.append(funcao)


        if vinculo in lista_vinculos:
            id_vinculo = dict_vinculos[vinculo]
        else:
            id_vinculo=0            

        if cod_servidor not in lista_incluidos:
            if str(cod_servidor)+'-'+str(anomes) not in listagem_folhames:
                objeto_folhames = Folhames(
                    anomes=anomes,
                    id_municipio=id_municipio,
                    cod_servidor=cod_servidor,
                    id_secretaria=id_secretaria,
                    id_setor=id_setor,
                    id_funcao=id_funcao,
                    id_vinculo=id_vinculo,
                    previdencia=previdencia,
                    dias = ref_evento,
                    carga_horaria=carga_horaria
                    )

                carga_folhames.append(objeto_folhames)
                lista_incluidos.append(cod_servidor)

                ref_ev = Refeventos(
                    anomes=anomes,
                    id_municipio=id_municipio,
                    cod_servidor=cod_servidor,
                    ref_eventos = ref_evento
                    )

                carga_refeventos.append(ref_ev)
    cursor.close()
    del cursor


    if len(lista_erro_secretaria)>0:
        for kk in range(len(lista_erro_secretaria)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='secretaria',
                observacao=lista_erro_secretaria[kk]
                )
            carga_erro_secretaria.append(obj)

    if len(lista_erro_setor)>0:
        for kk in range(len(lista_erro_setor)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='setor',
                observacao=lista_erro_setor[kk]
                )
            carga_erro_setor.append(obj)

    if len(lista_erro_funcao)>0:
        for kk in range(len(lista_erro_funcao)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='funcao',
                observacao=lista_erro_funcao[kk]
                )
            carga_erro_funcao.append(obj)


    if len(lista_erro_setor)>0:                
        LogErro.objects.bulk_create(carga_erro_setor)

    if len(lista_erro_secretaria)>0:                
        LogErro.objects.bulk_create(carga_erro_secretaria)

    if len(lista_erro_funcao)>0:                
        LogErro.objects.bulk_create(carga_erro_funcao)

    Folhames.objects.bulk_create(carga_folhames)
    Refeventos.objects.bulk_create(carga_refeventos)
    return 1


#-------------------------------------------------------------    

def importarFolhaPasso2(id_municipio,anomes,empresa):

    lista_erro_evento=[]

   
    listagem_folhames=listagens.listagemFolhames(id_municipio,anomes)

    lista_eventos = listagens.listagemEventos(id_municipio)
    dict_eventos=listagens.criarDictEventos(id_municipio)

    dict_tipos_eventos=listagens.criarDictTiposDeEventos(id_municipio)

    lista=[]
    lista_eventosMes=[]

    objetos=[]
    feventos=[]
    lista_incluidos=[]

    carga_erro=[]
    carga_folhaeventos=[]
    carga_folhames=[]

    carga_erro_evento=[]

    queryP = Provento.objects.values(
        'codigo',
        'previdencia',
        'classificacao',
        'evento',
        'tipo',
        'valor_evento'
        ).filter(id_municipio=id_municipio,anomes=anomes,grupamento='N')


    for qp in range(len(queryP)):


        cod_servidor = queryP[qp]['codigo']
        previdencia = queryP[qp]['previdencia']
        cl_orcamentaria = queryP[qp]['classificacao']
        evento = queryP[qp]['evento']
        tipo = queryP[qp]['tipo']
        valor = queryP[qp]['valor_evento']
        
        evento=evento.strip()
        evento=evento.upper()

        evento=funcoes_gerais.remove_combining_fluent(evento)
    
        if evento in lista_eventos:
            id_evento = dict_eventos[evento]
            tipo = dict_tipos_eventos[id_evento]
        else:
            id_evento=0
            tipo=''

        if id_evento==0:
            if evento is not None:
                if evento not in lista_erro_evento:
                    lista_erro_evento.append(evento)


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
        
    if len(lista_erro_evento)>0:
        for kk in range(len(lista_erro_evento)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='evento',
                observacao=lista_erro_evento[kk]
                )
            carga_erro_evento.append(obj)


    if len(lista_erro_evento)>0:                
        LogErro.objects.bulk_create(carga_erro_evento)

    if len(carga_folhaeventos)>0:
        Folhaevento.objects.bulk_create(carga_folhaeventos)



    lista_erro_evento=[]

    lista_incluidos=[]

    carga_erro=[]
    carga_folhaeventos=[]
    carga_folhames=[]

    carga_erro_evento=[]


    queryS = Provento.objects.filter(id_municipio=id_municipio,anomes=anomes,grupamento__in=['S','s']).values('codigo','evento','previdencia','classificacao','tipo').annotate(valor_evento=Sum('valor_evento')).order_by('codigo')            


    for qp in range(len(queryS)):


        cod_servidor = queryS[qp]['codigo']
        previdencia = queryS[qp]['previdencia']
        cl_orcamentaria = queryS[qp]['classificacao']
        evento = queryS[qp]['evento']
        tipo = queryS[qp]['tipo']
        valor = queryS[qp]['valor_evento']
        
        evento=evento.strip()
        evento=evento.upper()

        evento=funcoes_gerais.remove_combining_fluent(evento)
    
        if evento in lista_eventos:
            id_evento = dict_eventos[evento]
            tipo = dict_tipos_eventos[id_evento]
        else:
            id_evento=0
            tipo=''

        if id_evento==0:
            if evento is not None:
                if evento not in lista_erro_evento:
                    lista_erro_evento.append(evento)


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
        
    if len(lista_erro_evento)>0:
        for kk in range(len(lista_erro_evento)):
            obj=LogErro(
                id_municipio=id_municipio,
                anomes=anomes,
                numero_linha=0,
                codigo='evento',
                observacao=lista_erro_evento[kk]
                )
            carga_erro_evento.append(obj)


    if len(lista_erro_evento)>0:                
        LogErro.objects.bulk_create(carga_erro_evento)

    if len(carga_folhaeventos)>0:
        Folhaevento.objects.bulk_create(carga_folhaeventos)

    return 1