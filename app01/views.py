from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import choices,importarPlanilha,listagens,funcoes_gerais,cadastro_01
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Evento,Planilha,Folhames,Secretaria,Setor,Funcao,Eventos_cv,Funcoes_cv,Vinculo
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

#https://docs.djangoproject.com/en/4.0/topics/db/sql/




# git remote set-url origin git@github.com:FernandoZap/utilitario-cv.git



# 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

#curl -H 'Authorization: token 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' https://api.github.com/FernandoZap/utilitario-cv


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
    vd = f"{valor:,.2f}"
    vd = vd.replace('.','-')
    vd = vd.replace(',','.')
    vd = vd.replace('-',',')
    return vd


@login_required
def importacaoFolhaExcel(request):
    #lista = listagens.listagemSetores2(86)
    #print (lista)

    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Importar Folha - Atenção: informe apenas arquivo .zip'

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

        if tabela=='SecFuncVincEvento':
            retorno = importarPlanilha.importarSecFuncVincEventos(id_municipio,anomes,entidade,empresa, )
        elif tabela=='Setor':    
            retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Servidor':            
            retorno = importarPlanilha.importarServidores(id_municipio,anomes,entidade,empresa)
        elif tabela=='Folha':
            retorno = importarPlanilha.importarFolha(id_municipio,anomes,entidade,empresa)
        elif tabela == 'Geral':
            retorno = importarPlanilha.importarSecFuncVincEventos(id_municipio,anomes,entidade,empresa)
            if retorno==1:
                retorno = importarPlanilha.importarSetores(id_municipio,anomes,entidade,empresa)
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
    cursor = connection.cursor()
    id_municipio=86
    anomes='202111'
    municipio='Caridade'
    referencia='202111'
    rs=0
    lista1=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    qT=0

    municipios = Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        #qt[0]["f001_quantidadeServidores (202111,'86')"]
        #print (qt[0]["f001_quantidadeServidores (202111,'86')"])
        #print ('valor da funcao')
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
    cursor = connection.cursor()
    id_municipio=86
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

    municipios = Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):
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

        cursor.execute("Select evento,tipo,sum(valor) as valor from v005_folhaEventos where \
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



@login_required
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

            cursor.execute("SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,sto.setor,fn.funcao,vc.vinculo,\
            fl.carga_horaria,fl.dias,rf.ref_eventos \
            from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor\
            inner join secretarias sec on sec.id_secretaria=fl.id_secretaria inner join setores sto on sto.id_setor=fl.id_setor and sto.secretaria_id=fl.id_secretaria\
            inner join funcoes fn on fn.id_funcao=fl.id_funcao\
            inner join vinculos vc on vc.id_vinculo=fl.id_vinculo\
            left join refeventos rf on rf.id_municipio=fl.id_municipio and rf.cod_servidor=fl.cod_servidor and rf.anomes=fl.anomes \
            where fl.anomes=%s and fl.id_municipio=%s\
            order by fl.cod_servidor",[anomes,id_municipio])

            query1 = dictfetchall(cursor)

            cabecalho = funcoes_gerais.cabecalhoFolha(empresa)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0

            for kk in range(0,len(query1)):
                somaEventos=0
                cod_servidor = query1[kk]['cod_servidor']
                queryEventos=funcoes_gerais.eventosMes(id_municipio,anomes,cod_servidor,empresa)


                lista.append(query1[kk]['secretaria'])
                lista.append(query1[kk]['setor'])
                lista.append(query1[kk]['cod_servidor'])
                lista.append(query1[kk]['nome'])
                lista.append(query1[kk]['funcao'])
                lista.append(query1[kk]['vinculo'])
                lista.append(query1[kk]['data_admissao'])
                lista.append(query1[kk]['carga_horaria'])
                lista.append(query1[kk]['ref_eventos'])
                for ll in range(len(queryEventos)):
                    valor_evento = queryEventos[ll]['valor']
                    valor_str = str(valor_evento)
                    valor_str = valor_str.replace('.',',')
                    lista.append(valor_str)
                    somaEventos+=queryEventos[ll]['valor']
                lista.append(somaEventos)


                writer.writerow(lista)
                lista=[]
            
        return response
        #titulo = 'Impressao do Excel *****'
        #municipios=Municipio.objects.all().order_by('municipio')


    else:
        titulo = 'Impressao do Excel'
        municipios=Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/gravarCSVFolha.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':''

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



def agrupareventos(request):
    sessao(request)
    titulo_html = 'Agrupar Eventos'
    current_user_id = request.user.id
    current_user_name = request.user.username


    mensagem=''
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser


        fileExcel=request.FILES['filename']
        empresa=int(request.POST['empresa'])


        retorno = cadastro_01.grupo_eventos(fileExcel,empresa,current_user_id)

        if retorno==1:
            return HttpResponseRedirect(reverse('app01:agrupar-eventos'))



    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/agruparEventos.html',
            {
                'titulo': titulo_html,
                'usuario_id': current_user_id,
                'usuario_username': current_user_name,
                'municipios': municipios,
            }
          )

def agruparfuncoes(request):
    sessao(request)
    titulo_html = 'Agrupar Funções'
    current_user_id = request.user.id
    current_user_name = request.user.username


    mensagem=''
    if (request.method == "POST" and request.FILES['filename']):
        current_user = request.user.iduser


        fileExcel=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])

        retorno = cadastro_01.grupo_funcoes(fileExcel,id_municipio,current_user_id)

        if retorno==1:
            return HttpResponseRedirect(reverse('app01:agrupar-funcoes'))



    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/agruparFuncoes.html',
            {
                'titulo': titulo_html,
                'usuario_id': current_user_id,
                'usuario_username': current_user_name,
                'municipios': municipios,
            }
          )


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











