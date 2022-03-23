from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import choices,importarPlanilha,listagens,funcoes_gerais
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Folha,Evento,Folhames
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

#https://docs.djangoproject.com/en/4.0/topics/db/sql/


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
    if (request.method == "POST" and request.FILES['filename']):

        current_user = 0  #request.user.iduser
        planilha=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        tabela=request.POST['tabela']
        anomes=int(ano+mes)
        nlinhas=request.POST['nlinhas']
        if nlinhas=='':
            nlinhas=6000
        else:
            nlinhas=int(nlinhas)




        #modelo = funcoes_gerais.modelos(str(id_municipio))
        municipio = funcoes_gerais.strings_pesquisa(str(id_municipio))
        mes_ref = funcoes_gerais.mesReferencia(mes)

        if tabela=='SecFuncVincEventos':
            retorno = importarPlanilha.importarSecFuncVincEventos(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nlinhas)
        elif tabela=='Setor':            
            retorno = importarPlanilha.importarSetores(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nlinhas)
        elif tabela=='Servidor':            
            retorno = importarPlanilha.importarServidores(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nlinhas)
        elif tabela=='Folha':            
            retorno = importarPlanilha.importarFolha(planilha,id_municipio,anomes,current_user,municipio,mes_ref,nlinhas)
            if retorno!='':
                return HttpResponseRedirect(reverse('app01:planilhaErrada'))


        #retorno = importarPlanilha.importarSecretarias(planilha,id_municipio,anomes,current_user)
        #retorno = importarPlanilha.importarSetores(planilha,id_municipio,anomes,current_user)
        #retorno = importarPlanilha.importarVinculos(planilha,id_municipio,anomes,current_user)
        #retorno = importarPlanilha.importarFuncoes(planilha,id_municipio,anomes,current_user)
        #retorno = importarPlanilha.importarEventos(planilha,id_municipio,anomes,current_user)


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


        #quantidade_de_funcionario=Folha.objects.filter(anomes=anomes,id_municipio=id_municipio).annotation(Count('cod_servidor'))

        cursor.execute("SELECT f001_quantidadeServidoresMes (%s,%s)",[anomes,id_municipio])
        qt = dictfetchall(cursor)
        #qt[0]["f001_quantidadeServidores (202111,'86')"]
        #print (qt[0]["f001_quantidadeServidores (202111,'86')"])
        print ('valor da funcao')
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
                'total_v':total_v,
                'total_d':total_d,
                'total_r':total_r,

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


        #quantidade_de_funcionario=Folha.objects.filter(anomes=anomes,id_municipio=id_municipio).annotation(Count('cod_servidor'))

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


        '''
        obj = Folhames.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
        if obj is None:
            municipios=Municipio.objects.all().order_by('municipio')
            return render(request, 'app01/imprimirCSVFolha.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipios':municipios,
                        'mensagem':'O arquivo Zip ainda não foi importado'

                    }
                )

        '''
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'
        if (1==1):

            cursor.execute("SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,sto.setor,fn.funcao,vc.vinculo,\
            fl.carga_horaria,fl.dias\
            from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor\
            inner join secretarias sec on sec.id_secretaria=fl.id_secretaria inner join setores sto on sto.id_setor=fl.id_setor and sto.secretaria_id=fl.id_secretaria\
            inner join funcoes fn on fn.id_funcao=fl.id_funcao\
            inner join vinculos vc on vc.id_vinculo=fl.id_vinculo\
            where fl.anomes=%s and fl.id_municipio=%s\
            order by fl.cod_servidor",[anomes,id_municipio])

            query1 = dictfetchall(cursor)

            cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0



            for kk in range(0,11):
                somaEventos=0
                cod_servidor = query1[kk]['cod_servidor']
                queryEventos=funcoes_gerais.eventosMes(id_municipio,anomes,cod_servidor)
                lista.append(query1[kk]['cod_servidor'])
                lista.append(query1[kk]['nome'])
                lista.append(query1[kk]['data_admissao'])
                lista.append(query1[kk]['secretaria'])
                lista.append(query1[kk]['setor'])
                lista.append(query1[kk]['funcao'])
                lista.append(query1[kk]['vinculo'])
                lista.append(query1[kk]['carga_horaria'])
                lista.append(query1[kk]['dias'])
                for ll in range(len(queryEventos)):
                    lista.append(queryEventos[ll]['valor'])
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



'''
SELECT sv.cod_servidor,sv.nome,sv.data_admissao,sec.secretaria,sto.setor,fn.funcao,vc.vinculo,
fl.carga_horaria,fl.dias
from servidores sv inner join folhames fl on fl.cod_servidor=sv.cod_servidor
inner join secretarias sec on sec.id_secretaria=fl.id_secretaria inner join setores sto on sto.id_setor=fl.id_setor and sto.secretaria_id=fl.id_secretaria
inner join funcoes fn on fn.id_funcao=fl.id_funcao
inner join vinculos vc on vc.id_vinculo=fl.id_vinculo
where fl.anomes=202111 and fl.id_municipio=86
order by fl.cod_servidor;
'''




'''
select ev.id_evento,ev.evento,ifnull(fm.valor,0) as valor
from eventos ev left join folhaeventos fm on fm.id_evento=ev.id_evento and
fm.anomes=202111 and fm.id_municipio=86 and fm.cod_servidor=%s
where ev.tipo='V' and ev.id_municipio=86 order by ev.evento
'''
'''


CREATE VIEW v001_valoresmes AS 
select fm.anomes AS anomes,fm.id_municipio AS id_municipio,fm.
id_secretaria AS id_secretaria,fm.id_setor AS id_setor,fe.tipo AS tipo,
fe.id_evento AS id_evento,
(case when (fe.tipo = 'V') then fe.valor else 0 end) AS vantagens,
(case when (fe.tipo = 'D') then fe.valor else 0 end) AS descontos 
from folhames fm inner join folhaeventos fe 
on fm.cod_servidor = fe.cod_servidor 
    and fm.id_municipio = fe.id_municipio 
    and fm.anomes = fe.anomes;
'''

