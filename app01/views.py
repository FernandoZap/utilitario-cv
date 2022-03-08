from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import leituraZip,funcoes_gerais,m2_importacaoGeral,m2_importacaoFolha,choices,importarPlanilha
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Departamento,Setor,ProvDesc,ProventosMes,FolhaMes
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


@login_required
def departamentoList(request):
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        print ('id_municipio: '+str(id_municipio))


        deptos = Departamento.objects.filter(id_municipio=id_municipio).order_by('departamento')
    else:
        deptos = []

    titulo = 'Lists dos Departamentos'
    municipios = Municipio.objects.all().order_by('municipio')
    return render(request, 'app01/deptoList.html',
            {
                'titulo': titulo,
                'departamentos':deptos,
                'municipios':municipios
            }
          )


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


'''
def setorList1(request):
    cursor = connection.cursor()

    #sql = 'Select distinct f.codigo_funcionario,d.codigo,d.departamento,s.codigo,s.setor,c.cargo,f.tipo,f.valor from folha f, departamento d,setor s, cargo c  where f.id_departamento=d.id_departamento and f.id_setor=s.id_setor and f.id_cargo=c.id_cargo order by f.codigo_funcionario,f.tipo'
    #sql = 'select * from view_dep_setor'
    #sql = 'Call my_proc_IN2(76)'
    sql2 = "SELECT f001_total_folha (76,202111,'R')"


    #cursor.execute(sql)
    #r = cursor.fetchall()
    #r = dictfetchall(cursor)

    cursor.execute(sql2)
    r2 = cursor.fetchall()
    #r2 = dictfetchall(cursor)

    r5 =  (r2[0])[0]

    cursor.close()
    del cursor
    #db_connection.close()

    #print (str(r[0][0])+';'+str(r[0][1])+';'+str(r[0][2])+';'+str(r[0][3]))
    
    return render (request, 'app01/output.html',{'valor':r5})

'''



@login_required
def setorList(request):
    #obj = Folha.objects.all()
    
    return render (request, 'app01/output.html',{'data':obj})


'''
def listDepSetor(request):

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio


    else:
        municipio=''
    municipios = Municipio.objects.all().order_by('municipio')
    titulo = 'Lists dos Departamentos'

    sql = "select * from f006_listDepSetor('"+municipio+"')"
    cursor = connection.cursor()

    cursor.execute(sql)
    #r = cursor.fetchall()
    r = dictfetchall(cursor)


    return render(request, 'app01/listDepSetor.html',
            {
                'titulo': titulo,
                'departamentos':r,
                'municipios':municipios
            }
          )
'''          

'''
def listFolhaResumo2(request):

    opcao=''
    query1=None
    query2=None
    cursor = connection.cursor()
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        opcao=request.POST['opcao']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

    else:
        id_municipio=0
        anomes=200001
        municipio=''
        referencia=''
    titulo = 'Totais da Folha'

    if opcao=='01':
        sql = "SELECT * FROM v002_listfolharesumo WHERE id_municipio="+str(id_municipio)+" AND "+" anomes="+str(anomes)+" order by departamento,setor"



    if opcao!='':
        
        if opcao=='01':
            cursor.execute(sql)    
        else:
            cursor.execute("SELECT p.codigo,p.descricao,SUM(vantagem) as vantagem, SUM(desconto) AS desconto FROM v003_proventos v,provdesc p,departamento d WHERE v.id_departamento=d.id_departamento AND  v.id_provento=p.id_provdesc AND v.id_municipio=%s AND v.anomes=%s  GROUP BY p.codigo,p.descricao", [id_municipio,anomes])    
        if opcao=='01':
            query1 = dictfetchall(cursor)
        else:
            query2 = dictfetchall(cursor)

    municipios = Municipio.objects.all().order_by('municipio')


    r5=''
    if opcao!='':
        sql2 = "SELECT f005_countFuncionario_folha ("+str(id_municipio)+','+str(anomes)+")"
        cursor.execute(sql2)
        r2 = cursor.fetchall()
        r5 =  (r2[0])[0]
        cursor.close()
        del cursor

    return render(request, 'app01/listFolhaResumo1.html',
            {
                'titulo': titulo,
                'resumo_depsetor':query1,
                'resumo_provento':query2,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':r5
            }
          )

'''
@login_required
def importacaoGeral(request):
    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Atualizar Informaçoes de Funcionarios - Atenção: informe apenas arquivo .zip'
    municipios=Municipio.objects.all().order_by('municipio')
    mensagem=''

    if (request.method == "POST" and request.FILES['filename']):

        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)



        '''
        obj = Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).first()
        if obj is not None:
            
            mensagem='Essa Folha já foi importada!'
            return render(request, 'app01/importacaoGeral.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
        '''

        municipio = Municipio.objects.get(id_municipio=id_municipio)
        modelo = municipio.modelo
        string_pesquisa = municipio.string_pesquisa
        nome_municipio=municipio.municipio


        mes_extenso = funcoes_gerais.mesPorExtenso(mes,modelo)
        if modelo==1:
            referencia='FOLHA REF:'+mes_extenso+'/'+ano
        elif modelo==2:
            referencia=mes_extenso+' de '+ano


        if leituraZip.validaPDF(file_zip,string_pesquisa,referencia)==1:
            if modelo==2:
                m2_importacaoGeral.importacaoGeral(file_zip,id_municipio)
                #leituraZip.importacaoProventos_modelo2(file_zip,id_municipio,anomes)
                #leituraZip.importacaoFuncionario_modelo2(file_zip,id_municipio,anomes)
            mensagem='Processo Concluido'
        else:
            mensagem='Arquivo Zip não foi localizado!'
            return render(request, 'app01/importacaoGeral.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
                  )


    return render(request, 'app01/importacaoGeral.html',
            {
                'titulo': titulo_html,
                'municipios':municipios,
                'mensagem':mensagem
            }
          )


@login_required
def importacaoFolha(request):
    #------------------------------------------------------------------------------
    # esta rotina para ler o arquivo .zip da folha de pagamento de cada municipio
    # e gravar no banco os departamentos/setores/funcionarios/cargos/vinculos,
    #  proventos e descontos.
    #-----------------------------------------------------------------------------
    titulo_html = 'Importar Folha - Atenção: informe apenas arquivo .zip'
    
    mensagem=''
    municipios=Municipio.objects.all().order_by('municipio')
    if (request.method == "POST" and request.FILES['filename']):

        current_user = request.user.iduser
        file_zip=request.FILES['filename']
        id_municipio=int(request.POST['municipio'])
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)




        '''
        obj = Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).first()
        if obj is not None:
            
            mensagem='Essa Folha já foi importada!'
            return render(request, 'app01/importacaoGeral.html',
                    {
                        'titulo': titulo_html,
                        'municipios':municipios,
                        'mensagem':mensagem
                    }
        '''

        #municipio = Municipio.objects.get(id_municipio=id_municipio)
        #modelo = municipio.modelo
        #string_pesquisa = municipio.string_pesquisa

        modelo = funcoes_gerais.modelos(str(id_municipio))
        string_pesquisa = funcoes_gerais.strings_pesquisa(str(id_municipio))


        mes_extenso = funcoes_gerais.mesPorExtenso(mes,modelo)
        if id_municipio==76:
            referencia='FOLHA REF:'+mes_extenso+'/'+ano
        elif id_municipio==86:
            referencia=mes_extenso+' de '+ano


        if leituraZip.validaPDF(file_zip,string_pesquisa,referencia)==1:
            #Folha.objects.filter(id_municipio=id_municipio,anomes=anomes).delete()
            if modelo==2:
                obj=FolhaMes.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
                if obj is not None:
                    FolhaMes.objects.filter(anomes=anomes,id_municipio=id_municipio).delete()
                obj=ProventosMes.objects.filter(anomes=anomes,id_municipio=id_municipio).first()
                if obj is not None:
                    ProventosMes.objects.filter(anomes=anomes,id_municipio=id_municipio).delete()
                retorno=m2_importacaoFolha.importacaoFolha(file_zip,id_municipio,anomes)
                mensagem='Processo Concluido com Sucesso'
            return HttpResponseRedirect(reverse('app01:importacaoFolha'))

        else:
            mensagem='Arquivo Zip não foi localizado!'
            
            return render(request, 'app01/importacaoFolha.html',
                    {
                        'titulo': titulo_html,
                        'mensagem':mensagem,
                        'municipios':municipios
                    }
                  )
    return render(request, 'app01/importacaoFolha.html',
            {
                'titulo': titulo_html,
                'mensagem':mensagem,
                'municipios':municipios
            }
          )

@login_required
def listFolha(request):
    anomes=202111
    id_municipio=86

    '''
        pp = FolhaMes.objects.filter(anomes=202111).values('departamento__departamento').annotate(Count('proventosmes'))
        pp = FolhaMes.objects.filter(anomes=202111).values('departamento__departamento','setor__setor').annotate(soma=Sum('proventosmes'))

    '''


    ff = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio).aggregate()


    folha = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio)[0:4]

    for f1 in folha:
        lista=[]
        lista.append(f1.funcionario.codigo)
        lista.append(f1.funcionario.nome)
        lista.append(f1.departamento.departamento)
        lista.append(f1.setor.setor)
        lista.append(f1.funcao.funcao)
        lista.append(f1.lotacao.lotacao)
        lista.append(f1.vinculo.vinculo)
        lista.append(f1.funcionario.matricula)


        provs = f1.proventosmes_set.all()

        lista_prov=[]
        rel_prov = ProvDesc.objects.filter(id_municipio=id_municipio, tipo='VANTAGEM').order_by('ordenacao1')
        for pp1 in rel_prov:
            valor=0
            for pp2 in provs:
                if pp2.provdesc.codigo==pp1.codigo:
                    valor=pp2.valor
            lista.append(valor)
        #print(lista)
        #print ('-----------------------------')




    return render(request, 'app01/folha.html',
            {
            'folha':'',
            }
          )


@login_required
def listFolha2(request):
    anomes=202111
    id_municipio=86

    '''
        pp = FolhaMes.objects.filter(anomes=202111).values('departamento__departamento').annotate(Count('proventosmes'))
        pp = FolhaMes.objects.filter(anomes=202111).values('departamento__departamento','setor__setor').annotate(soma=Sum('proventosmes'))

    '''

    pp = FolhaMes.objects.filter(anomes=202111).values('departamento__departamento','setor__setor').annotate(soma=Sum('proventosmes')).order_by('departamento__departamento','setor__setor')



    for kk in range(len(pp)):
        print(pp[kk]['departamento__departamento'],' - ',pp[kk]['setor__setor'],' - ',pp[kk]['soma'])


    return render(request, 'app01/folha.html',
            {
            'folha':'',
            }
          )






@login_required
def gravarCSVFolha(request):

    if request.method=='POST':
        id_municipio = request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        anomes=int(ano+mes)

        obj = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio).first()
        if obj is None:
            municipios=Municipio.objects.all().order_by('municipio')
            return render(request, 'app01/gravarCSVFolha.html',
                    {
                        'titulo': 'Impressao do Excel',
                        'municipios':municipios,
                        'mensagem':'O arquivo Zip ainda não foi importado'

                    }
                )


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="folha_20210215.csv"'
        if (1==1):
            folha = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio).select_related('setor').order_by('funcionario__nome')
            rel_prov = ProvDesc.objects.filter(id_municipio=id_municipio, tipo='VANTAGEM').order_by('ordenacao1')

            cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio)
            #print ('id_municipio: '+str(id_municipio))
            #print(cabecalho)

            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            contador=0



            for f1 in folha:
                lista=[]
                lista.append(f1.setor.departamento)
                lista.append(f1.lotacao.lotacao)
                lista.append(f1.funcionario.codigo)
                lista.append(f1.funcionario.nome)
                lista.append(f1.funcao.funcao)
                lista.append(f1.vinculo.vinculo)
                lista.append(f1.funcionario.carga_horaria)
                
                


                provs = f1.proventosmes_set.all()

                lista_prov=[]
                soma=0
                for pp1 in rel_prov:
                    valor=0
                    for pp2 in provs:
                        if pp2.provdesc.codigo==pp1.codigo:
                            valor=pp2.valor
                            soma+=valor
                    lista.append(valor)

                lista.append(soma)
                writer.writerow(lista)
            
            
        return response

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
@login_required
def listFolhaResumo(request):

    municipios = Municipio.objects.all().order_by('municipio')
    titulo_html = 'Resumo da Folha'
    municipio=''
    anomes=''
    referencia=''
    lista=[]
    totalV=0
    totalD=0
    resultado=0
    mensagem=''
    aviso=''
    quantidade_de_funcionario=''

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        aviso = 'Resumo da Folha do Município de '+ municipio + '  Ref: '+ referencia

        pp = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio).values('departamento__departamento','setor__setor','departamento__id_departamento','setor__id_setor').annotate(soma=Sum('proventosmes__valor')).order_by('departamento__departamento','setor__setor')

        cc = FolhaMes.objects.filter(id_municipio=id_municipio,anomes=anomes).count()
        quantidade_de_funcionario=str(cc)


        if len(pp)>0:

            totalV = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio,proventosmes__provdesc__tipo='VANTAGEM').aggregate(soma=Sum('proventosmes__valor'))
            totalD = FolhaMes.objects.filter(anomes=anomes,funcionario__id_municipio=id_municipio,proventosmes__provdesc__tipo='DESCONTO').aggregate(soma=Sum('proventosmes__valor'))

            resultado = totalV['soma']-totalD['soma']

            totalV = formatMilhar(totalV['soma'])
            totalD = formatMilhar(totalD['soma'])
            resultado = formatMilhar(resultado)

            for k in range(len(pp)):
                
                #print (pp[k]['departamento__id_departamento'])
                id_depto=pp[k]['departamento__id_departamento']
                id_setor=pp[k]['setor__id_setor']

                vantagens_depto = ProventosMes.objects.filter(anomes=202111,folhames__funcionario__id_municipio=86,folhames__departamento__id_departamento=id_depto,provdesc__tipo='VANTAGEM').aggregate(soma=Sum('valor'))
                vantagens_setor = ProventosMes.objects.filter(anomes=202111,folhames__funcionario__id_municipio=86,folhames__setor__id_setor=id_setor,provdesc__tipo='VANTAGEM').aggregate(soma=Sum('valor'))

                descontos_depto = ProventosMes.objects.filter(anomes=202111,folhames__funcionario__id_municipio=86,folhames__departamento__id_departamento=id_depto,provdesc__tipo='DESCONTO').aggregate(soma=Sum('valor'))
                descontos_setor = ProventosMes.objects.filter(anomes=202111,folhames__funcionario__id_municipio=86,folhames__setor__id_setor=id_setor,provdesc__tipo='DESCONTO').aggregate(soma=Sum('valor'))
                
                if descontos_depto['soma'] is None:
                    descontos_depto['soma']=0
                if descontos_setor['soma'] is None:
                    descontos_setor['soma']=0

                if vantagens_setor['soma'] is None:
                    vantagens_setor['soma']=0

                if vantagens_depto['soma'] is None:
                    vantagens_depto['soma']=0



                resultado_depto = vantagens_depto['soma']-descontos_depto['soma']
                resultado_setor = vantagens_setor['soma']-descontos_setor['soma']


                lista.append(
                    {
                        'departamento':pp[k]['departamento__departamento'],
                        'setor':pp[k]['setor__setor'],
                        'vantagens_depto':formatMilhar(vantagens_depto['soma']),
                        'descontos_depto':formatMilhar(descontos_depto['soma']),
                        'vantagens_setor':formatMilhar(vantagens_setor['soma']),
                        'descontos_setor':formatMilhar(descontos_setor['soma']),
                        'resultado_depto':formatMilhar(resultado_depto),
                        'resultado_setor':formatMilhar(resultado_setor)
                    }
                    )
        else:
            mensagem='Nenhum registro encontrado'
            lista=None
    else:
        lista=None

    return render(request, 'app01/listFolhaResumo1.html',
            {
                'titulo': titulo_html,
                'resumo_depsetor':lista,
                'municipios':municipios,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':10,
                'total_vantagens':totalV,
                'total_descontos':totalD,
                'resultado':resultado,
                'mensagem':mensagem,
                'aviso':aviso,
                'quantidade_de_funcionario':quantidade_de_funcionario
            }
          )

'''          

@login_required
def somaProventosDescontos(request):
    municipios = Municipio.objects.all().order_by('municipio')
    titulo_html = 'Resumo da Folha'
    municipio=''
    anomes=''
    referencia=''
    totalV=0
    totalD=0
    resultado=0
    mensagem=''
    aviso=''
    lista_vantagens=[]
    lista_descontos=[]
    lista_final=[]
    soma_v=0
    soma_d=0
    resultado=0
    quantidade_de_funcionario=''

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        cc = FolhaMes.objects.filter(id_municipio=id_municipio,anomes=anomes).count()
        quantidade_de_funcionario=str(cc)

        ##ff = ProventosMes.objects.select_related('folhames__funcionario').filter(id_provento=5)
        #print ('///////////////////')


        aviso = 'Resumo da Folha do Município de '+ municipio + '  Ref: '+ referencia



        pp2 = ProventosMes.objects.select_related('provdesc').filter(anomes=anomes,id_municipio=id_municipio).values('provdesc__codigo','provdesc__tipo','provdesc__descricao').annotate(soma=Sum('valor'))
        if len(pp2)>0:

            for kk in range(len(pp2)):
                if pp2[kk]['provdesc__tipo']=='VANTAGEM':
                    soma_v+=pp2[kk]['soma']

                    lista_vantagens.append(
                        {
                            'codigo':pp2[kk]['provdesc__codigo'],
                            'descricao':pp2[kk]['provdesc__descricao'],
                            'soma':formatMilhar(pp2[kk]['soma']),
                        }
                    )
                else:
                    soma_d+=pp2[kk]['soma']
                    lista_descontos.append(
                        {
                            'codigo':pp2[kk]['provdesc__codigo'],
                            'descricao':pp2[kk]['provdesc__descricao'],
                            'soma':formatMilhar(pp2[kk]['soma']),
                        }
                    )

            resultado=formatMilhar(soma_v-soma_d)
            soma_v=formatMilhar(soma_v)
            soma_d=formatMilhar(soma_d)


        else:
            mensagem='Nenhum registro encontrado'

    return render(request, 'app01/somaProventosDescontos.html',
            {
                'titulo': titulo_html,
                'lista_vantagens':lista_vantagens,
                'lista_descontos':lista_descontos,
                'mensagem':mensagem,
                'municipios':municipios,
                'soma_v':soma_v,
                'soma_d':soma_d,
                'resultado':resultado,
                'quantidade_de_funcionario':quantidade_de_funcionario

            }
          )




def formatMilhar(valor):
    vd = f"{valor:,.2f}"
    vd = vd.replace('.','-')
    vd = vd.replace(',','.')
    vd = vd.replace('-',',')
    return vd



@login_required
def listFolhaResumo(request):

    opcao=''
    query1=None
    query2=None
    titulo=''
    cursor = connection.cursor()
    id_municipio=0
    anomes='202111'
    municipio='Caridade'
    referencia='202111'
    rs=0
    lista1=[]
    lista2=[]

    total_v=0
    total_d=0
    total_r=0
    quantidade_de_funcionario=0

    municipios = Municipio.objects.all().order_by('municipio')
    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        titulo = 'Totais da Folha'

        quantidade_de_funcionario=FolhaMes.objects.filter(anomes=anomes,id_municipio=id_municipio).count()


        cursor.execute("SELECT d.departamento,SUM(v.vantagem) AS vantagens,SUM(v.desconto) AS descontos\
        FROM v001_valoresPorSetor v LEFT JOIN departamento d ON d.id_departamento=v.id_departamento\
        LEFT JOIN setor s ON v.id_setor=s.id_setor\
        WHERE v.id_municipio=%s  AND v.anomes=%s\
        GROUP BY d.departamento ORDER BY d.departamento",[id_municipio,anomes])

        query0 = dictfetchall(cursor)

        for q in query0:
            resultado=q['vantagens']-q['descontos']
            total_v+=q['vantagens']
            total_d+=q['descontos']
            total_r+=resultado


            lista1.append(
                {
                    'departamento':q['departamento'],
                    'vantagens':q['vantagens'],
                    'descontos':q['descontos'],
                    'resultado':resultado,
                }
                )

#'''''''''''''''''''''''''''''''''''''''

        cursor = connection.cursor()
        cursor.execute("SELECT d.departamento,s.setor,SUM(v.vantagem) AS vantagens,SUM(v.desconto) AS descontos\
        FROM v001_valoresPorSetor v LEFT JOIN departamento d ON d.id_departamento=v.id_departamento\
        LEFT JOIN setor s ON v.id_setor=s.id_setor\
        WHERE v.id_municipio=%s  AND v.anomes=%s\
        GROUP BY d.departamento,s.setor ORDER BY d.departamento,s.setor",[id_municipio,anomes])

        query1 = dictfetchall(cursor)

        for q in query1:
            departamento=q['departamento']

            for k1 in lista1:
                if k1['departamento']==departamento:
                    v_dep=k1['vantagens']
                    d_dep=k1['descontos']
                    r_dep=k1['resultado']


            resultado=q['vantagens']-q['descontos']
            lista2.append(
                {
                    'departamento':q['departamento'],
                    'setor':q['setor'],
                    'vantagens':q['vantagens'],
                    'descontos':q['descontos'],
                    'resultado':resultado,
                    'v_dep':v_dep,
                    'd_dep':d_dep,
                    'r_dep':r_dep

                }
                )


        del cursor


    return render(request, 'app01/listFolhaResumo1.html',
            {
                'titulo': titulo,
                'resumo_depsetor':lista2,
                'municipios':municipios,
                'id_municipio':id_municipio,
                'anomes':anomes,
                'municipio':municipio,
                'referencia':referencia,
                'qtde_funcionario':quantidade_de_funcionario,
                'total_v':total_v,
                'total_d':total_d,
                'total_r':total_r,

            }
          )
