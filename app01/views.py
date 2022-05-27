from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import choices,importarPlanilha,listagens,funcoes_gerais,cadastro_01,processamentoFolha
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Planilha,Folhames,Secretaria,Setor,Vinculo,Funcao,Evento,Folhaevento
from accounts.models import User
from django.db.models import Count,Sum
import csv
import datetime
import os
import json
import mysql.connector
import openpyxl
import re
from django.core.files import File
import zipfile
from django.db import connection
import unicodedata


#https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04

#https://docs.djangoproject.com/en/4.0/topics/db/sql/




# git remote set-url origin git@github.com:FernandoZap/utilitario-cv.git



# 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

#curl -H 'Authorization: token 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' https://api.github.com/FernandoZap/utilitario-cv


colunas_eventos=['BV','BW','BX']


def get(self, request, *args, **kwargs):
    self.request.session['funcao'] = self.request.user.funcao
    self.request.session['username'] = self.request.user.username
    return super().get(request, *args, **kwargs)  



def sessao(request):
    if not request.session.get('username'):
        request.session['username'] = request.user.username
    return




def processUserInfo(request,userInfo):
    #userInfo = json.loads(userInfo)
    print()
    print("USER INFO RECEIVED")
    print('--------------------------')
    #print(f"User Name: {userInfo['name']}")
    #print(f"User Type: {userInfo['type']}")
    print()
    return "Info received successfuly"


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def formatMilhar(valor):
    if valor<0:
        valor=valor*(-1)
        sinal='-'
    else:
        sinal=''        

    vd = f"{valor:,.2f}"
    vd = vd.replace('.','-')
    vd = vd.replace(',','.')
    vd = vd.replace('-',',')
    return sinal+vd


def importacaoFolhaExcel_old(request):


    #lista = listagens.listagemSetores2(86)
    #print (lista)

    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Importar Folha - Atenção: informe apenas arquivo .zip'

    '''
    objs=Eventos_cv.objects.all()
    for obj in objs:
        evento=obj.evento
        evento=funcoes_gerais.remove_combining_fluent(evento)
        obj.evento=evento
    Eventos_cv.objects.bulk_update(objs,['evento'])

    ls1=[e.id_evento_cv for e in Eventos_cv.objects.all()]
    ls2=[e.id_evento_cv for e in Evento.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Eventos_cv.objects.get(pk=ls1[k]).delete()

    ls1=[e.id_funcao_cv for e in Funcoes_cv.objects.all()]
    ls2=[e.id_funcao_cv for e in Funcao.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Funcoes_cv.objects.get(pk=ls1[k]).delete()
    '''            

    mensagem=''
    municipios=Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):

        current_user = 0  #request.user.iduser
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        tabela=request.POST['tabela']
        anomes=int(ano+mes)


        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            empresa = ''
            logerro=LogErro(
            id_municipio = id_municipio,
            anomes = anomes,
            observacao = 'Empresa do municipio nao identificada')
            logerro.save()

        entidade='PREFEITURA MUNICIPAL DE '+municipio.upper()
        if id_municipio==38:
            entidade='GOVERNO MUNICIPAL DE SAO GONCALO DO AMARANTE'


        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is not None:
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Processamento da Folha',
                        'municipio':municipio,
                        'anomes':str(mes)+'/'+str(ano),
                        'mensagem':'A Folha selecionada já foi processada!'

                    }
                )
        mes_ref = funcoes_gerais.mesReferencia(mes)
        if tabela=='Secretaria':
            retorno = importarPlanilha.importarSecretaria(id_municipio,anomes,entidade,empresa)
        elif tabela=='Funcao':
            retorno = importarPlanilha.importarFuncao(id_municipio,anomes,entidade,empresa)
        elif tabela=='Evento':
            retorno = importarPlanilha.importarEventos(id_municipio,anomes,entidade,empresa)
        elif tabela=='Setor':    
            retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Vinculos':
            retorno = importarPlanilha.importarVinculos(id_municipio,anomes,entidade,empresa)
        elif tabela=='Servidor':            
            retorno = importarPlanilha.importarServidores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Folha':
            retorno = importarPlanilha.importarFolha(id_municipio,anomes,entidade,empresa)
        elif tabela == 'Geral':
            retorno = importarPlanilha.importarSecretaria(id_municipio,anomes,entidade,empresa)
            if retorno==1:
                retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarFuncao(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarEventos(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarVinculos(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarServidores(id_municipio,anomes,entidade,empresa)
                retorno = importarPlanilha.importarFolha(id_municipio,anomes,entidade,empresa)
            else:                
                return render(request, 'app01/planilhaErrada.html',
                        {
                            'titulo': 'Processamento da Folha',
                            'municipio':municipio,
                            'anomes':str(mes)+'/'+str(ano),
                            'mensagem':'Nao existe nenhum registro desse municipio e desse mes para ser processado!'

                        }
                    )

        return HttpResponseRedirect(reverse('app01:importacaoFolhaExcel'))


    return render(request, 'app01/importacaoFolhaExcel.html',
            {
                'titulo': titulo_html,
                'mensagem':mensagem,
                'municipios':municipios
            }
          )


def planilhaErrada(request):
    return render(request, 'app01/planilhaErrada.html')

def listFolhaResumo(request):

    opcao=''
    query1=None
    query2=None
    titulo='Listar soma por Secretarias/Setores'
    
    id_municipio=86
    anomes=''
    municipio=''
    referencia=''
    rs=0
    lista1=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    qT=0

    municipios = Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')
    if (request.method == "POST"):
        cursor = connection.cursor()
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        for e in qt[0].values():
            qT=e

        cursor.execute("select s.id_secretaria,s.secretaria,sum(vantagens) as vantagens, sum(descontos) as descontos\
        from v001_valoresmes v,secretarias s\
        where v.id_secretaria=s.id_secretaria\
        and v.id_municipio=%s\
        and v.anomes=%s\
        group by s.id_secretaria,s.secretaria ORDER BY s.secretaria",[id_municipio,anomes])

        query0 = dictfetchall(cursor)

        for q in query0:
            resultado=q['vantagens']-q['descontos']
            total_v+=q['vantagens']
            total_d+=q['descontos']
            total_r+=resultado

            lista1.append(
                {
                    'id_secretaria':q['id_secretaria'],
                    'secretaria':q['secretaria'],
                    'vantagens':formatMilhar(q['vantagens']),
                    'descontos':formatMilhar(q['descontos']),
                    'resultado':formatMilhar(resultado),
                }
                )

#'''''''''''''''''''''''''''''''''''''''
        
        cursor.execute("select s.id_secretaria,s.secretaria,st.setor,sum(vantagens) as vantagens, sum(descontos) as descontos\
        from v001_valoresmes v,secretarias s,setores st\
        where v.id_secretaria=s.id_secretaria\
        and s.id_secretaria=st.secretaria_id\
        and st.id_setor=v.id_setor\
        and v.id_municipio=%s\
        and v.anomes=%s\
        group by s.id_secretaria,s.secretaria,st.setor order by s.secretaria,st.setor",[id_municipio,anomes])

        query1 = dictfetchall(cursor)

        for q in query1:
            secretaria=q['secretaria']
            id_secretaria=q['id_secretaria']

            for k1 in lista1:
                if k1['id_secretaria']==id_secretaria:
                    v_dep=k1['vantagens']
                    d_dep=k1['descontos']
                    r_dep=k1['resultado']

            resultado=q['vantagens']-q['descontos']
            lista2.append(
                {
                    'secretaria':q['secretaria'],
                    'setor':q['setor'],
                    'vantagens':formatMilhar(q['vantagens']),
                    'descontos':formatMilhar(q['descontos']),
                    'resultado':formatMilhar(resultado),
                    'v_dep':v_dep,
                    'd_dep':d_dep,
                    'r_dep':r_dep

                }
                )

        cursor.close()
        del cursor

    return render(request, 'app01/listSomaPorSecSetores.html',
            {
                'titulo': titulo,
                'resumo_depsetor':lista2,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':qT,
                'total_v':formatMilhar(total_v),
                'total_d':formatMilhar(total_d),
                'total_r':formatMilhar(total_r),

            }
          )



def listSomaEventos(request):

    opcao=''
    query1=None
    query2=None
    titulo='Listar Soma por Eventos'
    id_municipio=0
    anomes=''
    municipio=''
    referencia=''
    rs=0
    lista_eventos=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    qT=0

    municipios = Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')

    if (request.method == "POST"):
        cursor = connection.cursor()
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano


        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        for e in qt[0].values():
            qT=e

        cursor.execute("Select evento,tipo,sum(valor) as valor from v005_folhaeventos where \
            anomes=%s and id_municipio=%s group by evento,tipo order by tipo desc,evento",[anomes,id_municipio])

        query0 = dictfetchall(cursor)

        for q in query0:
            if q['tipo']=='V':
                total_v+=q['valor']
                total_r+=q['valor']
            else:
                total_d+=q['valor']
                total_r-=q['valor']

            lista_eventos.append(
                {
                    'evento':q['evento'],
                    'tipo':'('+q['tipo']+')',
                    'valor':formatMilhar(q['valor'])
                }
                )
        total_v=formatMilhar(total_v)
        total_d=formatMilhar(total_d)
        total_r=formatMilhar(total_r)

#'''''''''''''''''''''''''''''''''''''''
        
        cursor.close()
        del cursor


    return render(request, 'app01/listSomaPorEventos.html',
            {
                'titulo': titulo,
                'eventos':lista_eventos,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':qT,
                'total_v':total_v,
                'total_d':total_d,
                'total_r':total_r,
                'qT':qT

            }
          )

def parateste(request):

    lista_grupo_eventos=listagens.listagemGrupoEventos(86)
    dict_grupo_eventos=listagens.criarDictGrupoEventos(86)


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
        ).all()

    for qp in range(len(queryP)):

        cod_servidor = queryP[qp]['codigo']
        evento1 = queryP[qp]['evento']

        evento1=evento1.strip()


        if evento1 in lista_grupo_eventos:
            evento = dict_grupo_eventos[evento1]
        else:
            evento = evento1            


        print (str(cod_servidor) + ' - ' + evento1 + ' - '+ evento)


        
    return render(request, 'app01/planilhaErrada.html')


def eliminarAcentos(tabela):


    if tabela=='eventos':

        obj_evs=Evento.objects.all()
        for ev in obj_evs:
            ev.evento=funcoes_gerais.to_ascii_string(ev.evento)

        Evento.objects.bulk_update(obj_evs,['evento'])

    elif tabela=='secretaria':

        obj_evs=Secretaria.objects.all()
        for ev in obj_evs:
            ev.secretaria=funcoes_gerais.to_ascii_string(ev.secretaria)

        Secretaria.objects.bulk_update(obj_evs,['secretaria'])

    elif tabela=='setor':

        obj_evs=Setor.objects.all()
        for ev in obj_evs:
            ev.setor=funcoes_gerais.to_ascii_string(ev.setor)

        Setor.objects.bulk_update(obj_evs,['setor'])

    elif tabela=='funcoes':

        obj_evs=Funcao.objects.all()
        for ev in obj_evs:
            ev.funcao=funcoes_gerais.to_ascii_string(ev.funcao)

        Funcao.objects.bulk_update(obj_evs,['funcao'])
    else:
        string=funcoes_gerais.to_ascii_string(tabela)
        print (tabela)
        print (string)
        print (tabela.encode('UTF-8'))
        print ('--------------')



def remove_combining_fluent(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return ''.join(
        [l for l in normalized if not unicodedata.combining(l)]
    )


def consultarTabelas(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        tabela = request.POST['tabela']
        lista=[]

        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            municipio=''
            empresa = ''
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="consulta_tabelas.csv"'
        if (1==1):

            if tabela=='Eventos':
                query1 = Evento.objects.filter(id_municipio=id_municipio,cancelado='N').order_by('evento')
                cabecalho = ['municipio','codigo','descricao do evento','tipo','exibe','principal']
            elif tabela=='Funcoes':
                query1 = Funcao.objects.filter(id_municipio=id_municipio,cancelado='N').order_by('funcao')
                cabecalho = ['municipio','codigo','descricao da funcao','principal']


            

            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0
            if tabela=='Eventos':
                for kk in range(0,len(query1)):
                    lista.append(municipio)
                    lista.append(query1[kk].id_evento)
                    lista.append(query1[kk].evento)
                    lista.append(query1[kk].tipo)
                    lista.append(query1[kk].exibe_excel)
                    lista.append(query1[kk].id_evento_cv)
                    writer.writerow(lista)
                    lista=[]
            elif tabela=='Funcoes':
                for kk in range(0,len(query1)):
                    lista.append(municipio)
                    lista.append(query1[kk].id_funcao)
                    lista.append(query1[kk].funcao)
                    lista.append(query1[kk].id_funcao_cv)
                    writer.writerow(lista)
                    lista=[]
            
        return response


    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/consultarTabelas.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )


def folhasProcessadas_bak(request):

    titulo='Folhas Processadas'
    municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')


    municipio=''
    lista_folha=None
    if request.method=='POST':
        id_municipio = int(request.POST['municipio'])
        cursor = connection.cursor()
        lista=[]


        if id_municipio==0:
            municipio='Todos os municípios'
        else:            
            ls_municipio = funcoes_gerais.entidade(id_municipio)
            if len(ls_municipio)>0:
                municipio=ls_municipio[0]
                empresa = ls_municipio[1]
            else:
                municipio=''
                empresa = ''

        if (1==1):

            if id_municipio>0:
                cursor.execute("select v3.municipio,concat(right(concat('',v3.anomes),2),'/',left(concat('',v3.anomes),4)) as mesref,\
                    v3.quantidade,v4.valor,v3.anomes \
                from v003_qtdeServidores v3,v004_valortotalFolha v4 where\
                 v3.id_municipio=v4.id_municipio and v3.anomes=v4.anomes\
                 and v3.id_municipio=%s order by v3.municipio,v3.anomes",[id_municipio])
            else:
                cursor.execute("select v3.municipio,concat(right(concat('',v3.anomes),2),'/',left(concat('',v3.anomes),4)) as mesref,\
                    v3.quantidade,v4.valor,v3.anomes \
                from v003_qtdeServidores v3,v004_valortotalFolha v4 where\
                 v3.id_municipio=v4.id_municipio and v3.anomes=v4.anomes\
                 order by v3.municipio,v3.anomes")

            query1 = dictfetchall(cursor)

            contador=0

            for kk in range(0,len(query1)):
                contador+=1

                valor=formatMilhar(query1[kk]['valor'])

                lista.append(
                        {
                            'item':contador,
                            'municipio':query1[kk]['municipio'],
                            'mesref':query1[kk]['mesref'],
                            'quantidade':query1[kk]['quantidade'],
                            'valor':valor

                        }
                    )

            cursor.close()
            del cursor
            lista_folha=lista
        
    return render(request, 'app01/folhasProcessadas.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':'',
            'municipio':municipio,
            'lista_folha':lista_folha

        }
    )


def imprimirCSVFolha(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)
        cursor = connection.cursor()
        lista=[]


        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            municipio=''
            empresa = ''
        

        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is None:
            municipio = funcoes_gerais.strings_pesquisa(id_municipio)
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipio':municipio,
                        'anomes': str(mes)+'/'+str(ano),
                        'mensagem':'Não existe nenhum registro para essa Folha.'

                    }
                )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'
        if (1==1):


            eventos = [ev.evento for ev in Evento.objects.filter(id_municipio=id_municipio,tipo='V',exibe_excel=1).order_by('evento')]


            cursor.execute("SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,st.setor as setor,fn.funcao,vc.vinculo,\
            fl.carga_horaria,fl.dias,rf.ref_eventos \
            from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor\
            inner join secretarias sec on sec.id_secretaria=fl.id_secretaria \
            inner join setores st on st.secretaria_id=sec.id_secretaria and st.id_setor=fl.id_setor \
            inner join funcoes fn on fn.id_funcao=fl.id_funcao\
            inner join vinculos vc on vc.id_vinculo=fl.id_vinculo\
            left join refeventos rf on rf.id_municipio=fl.id_municipio and rf.cod_servidor=fl.cod_servidor and rf.anomes=fl.anomes \
            where sv.id_municipio=fl.id_municipio and fl.anomes=%s and fl.id_municipio=%s\
            order by fl.cod_servidor",[anomes,id_municipio])

            query1 = dictfetchall(cursor)

            cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0

            dictEventos=funcoes_gerais.eventosMes(id_municipio,anomes)


            for kk in range(0,len(query1)):
                somaEventos=0
                cod_servidor = query1[kk]['cod_servidor']
                eventosDoServidor=dictEventos[cod_servidor]
                dicionario=funcoes_gerais.montarDiciionarioEventoDoServidor(eventosDoServidor)
                listaEventosDoServidor=funcoes_gerais.montaListaEventoDoServidor(eventosDoServidor)


                lista.append(query1[kk]['secretaria'])
                lista.append(query1[kk]['setor'])
                lista.append(query1[kk]['cod_servidor'])
                lista.append(query1[kk]['nome'])
                lista.append(query1[kk]['funcao'])
                lista.append(query1[kk]['vinculo'])
                lista.append(query1[kk]['data_admissao'])
                lista.append(query1[kk]['carga_horaria'])
                lista.append(query1[kk]['ref_eventos'])

                soma=0
                for qq in range(len(eventos)):
                    if eventos[qq] in listaEventosDoServidor:
                        valor=dicionario[eventos[qq]]
                        soma+=valor
                        valor_str=str(valor)
                        valor_str = valor_str.replace('.',',')
                    else:
                        valor_str='0'
                    lista.append(valor_str)
                soma_str=str(soma)
                soma_str = soma_str.replace('.',',')
                lista.append(soma_str)

                writer.writerow(lista)
                lista=[]
            cursor.close()
            del cursor

        return response
        #titulo = 'Impressao do Excel *****'
        #municipios=Municipio.objects.all().order_by('municipio')


    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')

    return render(request, 'app01/gravarCSVFolha.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )


def importacaoFolhaExcel(request):


    #lista = listagens.listagemSetores2(86)
    #print (lista)

    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Importar Folha - Atenção: informe apenas arquivo .zip'

    '''
    objs=Eventos_cv.objects.all()
    for obj in objs:
        evento=obj.evento
        evento=funcoes_gerais.remove_combining_fluent(evento)
        obj.evento=evento
    Eventos_cv.objects.bulk_update(objs,['evento'])

    ls1=[e.id_evento_cv for e in Eventos_cv.objects.all()]
    ls2=[e.id_evento_cv for e in Evento.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Eventos_cv.objects.get(pk=ls1[k]).delete()

    ls1=[e.id_funcao_cv for e in Funcoes_cv.objects.all()]
    ls2=[e.id_funcao_cv for e in Funcao.objects.all()]
    ls3=set(ls2)

    for k in range(len(ls1)):
        if ls1[k] not in ls3:
            #print (ls1[k])
            Funcoes_cv.objects.get(pk=ls1[k]).delete()
    '''            

    mensagem=''
    municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')


    if (request.method == "POST"):

        current_user = 0  #request.user.iduser
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        tabela=request.POST['tabela']
        anomes=int(ano+mes)


        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            empresa = ''
            logerro=LogErro(
            id_municipio = id_municipio,
            anomes = anomes,
            observacao = 'Empresa do municipio nao identificada')
            logerro.save()


        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is not None:
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Processamento da Folha',
                        'municipio':municipio,
                        'anomes':str(mes)+'/'+str(ano),
                        'mensagem':'A Folha selecionada já foi processada!'

                    }
                )
        mes_ref = funcoes_gerais.mesReferencia(mes)
        if tabela=='Secretaria':
            retorno = processamentoFolha.importarSecretaria(id_municipio,anomes,empresa)
        elif tabela=='Funcao':
            retorno = processamentoFolha.importarFuncao(id_municipio,anomes,empresa)
        elif tabela=='Evento':
            retorno = processamentoFolha.importarEventos(id_municipio,anomes,empresa)
        elif tabela=='Setor':    
            retorno = processamentoFolha.importarSetores(id_municipio,anomes,empresa)
        elif tabela=='Vinculos':
            retorno = processamentoFolha.importarVinculos(id_municipio,anomes,empresa)
        elif tabela=='Servidor':            
            retorno = processamentoFolha.importarServidores(id_municipio,anomes,empresa)
        elif tabela=='Folha':
            retorno = processamentoFolha.importarFolhaPasso1(id_municipio,anomes,empresa)
            retorno = processamentoFolha.importarFolhaPasso2(id_municipio,anomes,empresa)
        elif tabela == 'Geral':
            retorno = processamentoFolha.importarSecretaria(id_municipio,anomes,empresa)
            if retorno==1:
                retorno = processamentoFolha.importarSetores(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarFuncao(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarEventos(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarVinculos(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarServidores(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarFolhaPasso1(id_municipio,anomes,empresa)
                retorno = processamentoFolha.importarFolhaPasso2(id_municipio,anomes,empresa)

            else:                
                return render(request, 'app01/planilhaErrada.html',
                        {
                            'titulo': 'Processamento da Folha',
                            'municipio':municipio,
                            'anomes':str(mes)+'/'+str(ano),
                            'mensagem':'Nao existe nenhum registro desse municipio e desse mes para ser processado!'

                        }
                    )

        return HttpResponseRedirect(reverse('app01:importacaoFolhaExcel'))


    return render(request, 'app01/importacaoFolhaExcel.html',
            {
                'titulo': titulo_html,
                'mensagem':mensagem,
                'municipios':municipios
            }
          )

def imprimirFolhaLayout_bak(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)
        cursor = connection.cursor()
        lista=[]

        '''
        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
        else:
            municipio=''
            empresa = ''
        '''
        

        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is None:
            municipio = funcoes_gerais.strings_pesquisa(id_municipio)
            return render(request, 'app01/planilhaErrada.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipio':municipio,
                        'anomes': str(mes)+'/'+str(ano),
                        'mensagem':'Não existe nenhum registro para essa Folha.'

                    }
                )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'
        if (1==1):


            eventos = [ev.evento for ev in Evento.objects.filter(id_municipio=id_municipio,tipo='V',exibe_excel=1).order_by('evento')]


            cursor.execute("SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,st.setor as setor,fn.funcao,vc.vinculo, \
            fl.carga_horaria,rf.ref_eventos,f002_quantidadeEventos(fl.cod_servidor,fl.anomes,fl.id_municipio) as qtde_eventos \
            from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor\
            inner join secretarias sec on sec.id_secretaria=fl.id_secretaria \
            inner join setores st on st.secretaria_id=sec.id_secretaria and st.id_setor=fl.id_setor \
            inner join funcoes fn on fn.id_funcao=fl.id_funcao\
            inner join vinculos vc on vc.id_vinculo=fl.id_vinculo\
            left join refeventos rf on rf.id_municipio=fl.id_municipio and rf.cod_servidor=fl.cod_servidor and rf.anomes=fl.anomes \
            where sv.id_municipio=fl.id_municipio and fl.anomes=%s and fl.id_municipio=%s\
            order by fl.cod_servidor",[anomes,id_municipio])

            query1 = dictfetchall(cursor)


            cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0

            #dictEventos=funcoes_gerais.eventosMes(id_municipio,anomes)
            
            dictEventos=funcoes_gerais.eventosMesDoServidor(id_municipio,anomes)


            for kk in range(0,len(query1)):
                lista.append(query1[kk]['secretaria'])
                lista.append(query1[kk]['setor'])
                lista.append(query1[kk]['cod_servidor'])
                lista.append(query1[kk]['nome'])
                lista.append(query1[kk]['funcao'])
                lista.append(query1[kk]['vinculo'])
                lista.append(query1[kk]['data_admissao'])
                lista.append(query1[kk]['carga_horaria'])
                lista.append(query1[kk]['ref_eventos'])

                soma = 0
                if query1[kk]['qtde_eventos']>0:
                    cod_servidor = query1[kk]['cod_servidor']
                    eventosDoServidor=dictEventos[cod_servidor]
                    #[{'evento': 'ADC PTEMPSERV', 'valor': Decimal('381.28')}, {'evento': 'SALARIO BASE', 'valor': Decimal('3177.33')}]
                    dicionario=funcoes_gerais.montarDiciionarioEventoDoServidor(eventosDoServidor)
                    #{'ADC PTEMPSERV': Decimal('381.28'), 'SALARIO BASE': Decimal('3177.33')}
                    listaEventosDoServidor=funcoes_gerais.montaListaEventoDoServidor(eventosDoServidor)
                    #['ADC PTEMPSERV', 'SALARIO BASE', 'SALARIO FAMILIA']
                    for qq in range(len(eventos)):
                        if eventos[qq] in listaEventosDoServidor:
                            valor=dicionario[eventos[qq]]
                            soma+=valor
                            valor_str=str(valor)
                            valor_str = valor_str.replace('.',',')
                        else:
                            valor_str='0'
                        lista.append(valor_str)
                    soma_str=str(soma)
                    soma_str = soma_str.replace('.',',')
                    lista.append(soma_str)
                else:
                    for qq in range(len(eventos)):
                        valor_str='0'
                        lista.append(valor_str)
                    soma_str=str(soma)
                    lista.append(soma_str)

                writer.writerow(lista)
                lista=[]
            cursor.close()
            del cursor

        return response
        #titulo = 'Impressao do Excel *****'
        #municipios=Municipio.objects.all().order_by('municipio')


    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')


    return render(request, 'app01/gravarFolhaLayout.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )



def imprimirFolhaLayout(request):
    titulo = 'Impressao do Excel'
    municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')


    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)
        #cursor = connection.cursor()
        lista=[]

        eventos = [ev.evento for ev in Evento.objects.filter(id_municipio=id_municipio,tipo='V',exibe_excel=1).order_by('evento')]
        qtde_evento=3
        ultima_coluna=colunas_eventos[qtde_evento-1]


        query=Folhames.objects.filter(id_municipio=id_municipio,anomes=anomes).values('cod_servidor','id_secretaria','id_setor','id_funcao','id_vinculo','previdencia','carga_horaria').order_by('cod_servidor')

        dicNomeDoServidor=listagens.criarDictNomeServidor(id_municipio)
        dicNomeDaSecretaria=listagens.criarDictIdSecretarias(id_municipio)
        dicNomeDoSetor=listagens.criarDictIdSetores(id_municipio)
        dicNomeDaFuncao=listagens.criarDictIdFuncoes(id_municipio)
        dicNomeDoVinculo=listagens.criarDictIdVinculos(id_municipio)
        dicRefEventos=listagens.criarDictRefEventos(id_municipio,anomes)


        contador=2    

        dictEventos=funcoes_gerais.eventosMesDoServidor(id_municipio,anomes)
        lista=[]


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'

        cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
        writer = csv.writer(response, delimiter=';')
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow(cabecalho)

        for qy in query:
            cod_servidor=qy['cod_servidor']


            lista.append(dicNomeDaSecretaria[qy['id_secretaria']])
            lista.append(dicNomeDoSetor[qy['id_setor']])
            lista.append(cod_servidor)
            lista.append(dicNomeDoServidor[cod_servidor]['nome'])
            lista.append(dicNomeDaFuncao[qy['id_funcao']])
            lista.append(dicNomeDoVinculo[qy['id_vinculo']])
            lista.append(dicNomeDoServidor[cod_servidor]['data'])
            lista.append(qy['carga_horaria'])
            lista.append(dicRefEventos[qy['cod_servidor']])

            soma = 0
            '''
            eventosDoServidor=dictEventos[cod_servidor]
            #[{'evento': 'ADC PTEMPSERV', 'valor': Decimal('381.28')}, {'evento': 'SALARIO BASE', 'valor': Decimal('3177.33')}]
            dicionario=funcoes_gerais.montarDicionarioEventoDoServidor(eventosDoServidor)
            #{'ADC PTEMPSERV': Decimal('381.28'), 'SALARIO BASE': Decimal('3177.33')}
            listaEventosDoServidor=funcoes_gerais.montaListaEventoDoServidor(eventosDoServidor)
            #['ADC PTEMPSERV', 'SALARIO BASE', 'SALARIO FAMILIA']
            for qq in range(len(eventos)):
                if eventos[qq] in listaEventosDoServidor:
                    valor=dicionario[eventos[qq]]
                    soma+=valor
                    valor_str=str(valor)
                    valor_str = valor_str.replace('.',',')
                else:
                    valor_str='0'
                lista.append(valor_str)
            '''
            soma_str=str(soma)
            soma_str = soma_str.replace('.',',')
            lista.append(soma_str)
            #ci="J"+str(contador)
            #cf=ultima_coluna+str(contador)
            #formula="=soma("+ci+":"+cf+")"

            contador+=1
            #lista.append(formula)

            writer.writerow(lista)
            lista=[]
        return response

    return render(request, 'app01/gravarFolhaLayout.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

        }
    )



def folhasProcessadas(request):

    titulo='Folhas Processadas'
    municipios=Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')


    municipio=''
    contador=0
    lista_folha=None
    if request.method=='POST':
        id_municipio = int(request.POST['municipio'])
        cursor = connection.cursor()
        lista=[]


        if id_municipio==0:
            municipio='Todos os municípios'
        else:            
            ls_municipio = funcoes_gerais.entidade(id_municipio)
            if len(ls_municipio)>0:
                municipio=ls_municipio[0]
                empresa = ls_municipio[1]
            else:
                municipio=''
                empresa = ''
        if 1==1:
            dictMunicipios=listagens.criarDictMunicipios()
            if id_municipio>0:
                query=Folhames.objects.filter(id_municipio=id_municipio).values('id_municipio','anomes').annotate(qtde=Count("id_folha")).order_by('id_municipio','anomes')
            else:                
                query=Folhames.objects.values('id_municipio','anomes').annotate(qtde=Count("id_folha")).order_by('id_municipio','anomes')

            lista1=[]
            lista2=[]
            for kk in range(len(query)):
                lista1.append(str(query[kk]['id_municipio'])+':'+str(query[kk]['anomes']))
                lista2.append(query[kk]['qtde'])
            dicionario=dict(zip(lista1,lista2))

            if id_municipio>0:
                resumo=Folhaevento.objects.filter(tipo='V',id_municipio=id_municipio).values('id_municipio','anomes').annotate(valor_total=Sum("valor")).order_by('id_municipio','anomes')
            else:
                resumo=Folhaevento.objects.filter(tipo='V').values('id_municipio','anomes').annotate(valor_total=Sum("valor")).order_by('id_municipio','anomes')
            #resumo
            #<QuerySet [{'id_municipio': 76, 'anomes': 202201, 'total': Decimal('2119447.46')}, {'id_municipio': 76, 'anomes': 202202, 'total': Decimal('2168637.07')}]>

            for res in resumo:
                contador+=1
                id_municipio=res['id_municipio']
                anomes=res['anomes']
                valor=res['valor_total']
                quantidade=dicionario[str(res['id_municipio'])+':'+str(res['anomes'])]
                lista.append(
                        {
                        'item':contador,
                        'municipio':dictMunicipios[id_municipio],
                        'mesref':str(anomes)[-2:]+'/'+str(anomes)[0:4],
                        'quantidade':quantidade,
                        'valor':formatMilhar(valor)
                        }
                    )
            lista_folha=lista                



        
    return render(request, 'app01/folhasProcessadas.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':'',
            'municipio':municipio,
            'lista_folha':lista_folha
        }
    )
