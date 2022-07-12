from django.shortcuts import render,redirect
from django.views.generic import (ListView)
from django.http import HttpResponse,HttpResponseRedirect
from . import choices,listagens,funcoes_gerais,cadastro_01,processamentoFolha
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Municipio,Folhames,Secretaria,Setor,Vinculo,Funcao,Evento,Folhaevento
from accounts.models import User
from django.db.models import Count,Sum
import csv
import datetime
import os
import json
#import mysql.connector
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
                cabecalho = ['municipio','codigo','descricao do evento','tipo']
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

        query=Folhaevento.objects.filter(id_municipio=id_municipio,anomes=anomes).values('id_evento').annotate(soma=Sum('valor'))
        lista_id_evento = [e['id_evento'] for e in query]
        eventos = [ev.evento for ev in Evento.objects.filter(id_municipio=id_municipio,tipo='V',exibe_excel=1,id_evento__in=lista_id_evento).order_by('evento')]

        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
            entidade = ls_municipio[2]
        label_arquivo=entidade+'_'+funcoes_gerais.mesPorExtenso(mes,1)+'_'+str(ano)+'.csv'

        ultima_coluna = listagens.cols(len(eventos))

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
        response['Content-Disposition'] = 'attachment; filename='+label_arquivo

        cabecalho = funcoes_gerais.cabecalhoFolha(id_municipio,eventos)
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
            lista.append('CH '+str(qy['carga_horaria']))
            lista.append(dicRefEventos.get(qy['cod_servidor'],''))

            soma = 0
            
            eventosDoServidor=dictEventos.get(cod_servidor)
            if eventosDoServidor is None:
                lista=[]
                continue

            #[{'evento': 'ADC PTEMPSERV', 'valor': Decimal('381.28')}, {'evento': 'SALARIO BASE', 'valor': Decimal('3177.33')}]
            dicionario=funcoes_gerais.montarDicionarioEventoDoServidor(eventosDoServidor)
            #{'ADC PTEMPSERV': Decimal('381.28'), 'SALARIO BASE': Decimal('3177.33')}
            listaEventosDoServidor=funcoes_gerais.montaListaEventoDoServidor(eventosDoServidor)
            #['ADC PTEMPSERV', 'SALARIO BASE', 'SALARIO FAMILIA']
            for qq in range(len(eventos)):
                if eventos[qq] in listaEventosDoServidor:
                    valor=dicionario[eventos[qq]]
                    valor_str=str(valor)
                    valor_str = valor_str.replace('.',',')
                else:
                    valor_str='0'
                lista.append(valor_str)


            ci="J"+str(contador)
            cf=ultima_coluna+str(contador)
            formula="=soma("+ci+":"+cf+")"

            contador+=1
            lista.append(formula)

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
    sel_empresa=''


    municipio=''
    contador=0
    nome_da_empresa=''
    lista_folha=None
    if request.method=='POST':
        id_municipio = int(request.POST['municipio'])
        sel_empresa = request.POST['empresa']
        cursor = connection.cursor()
        lista=[]


        if id_municipio==0:
            municipio='Todos os municípios'
        else:            
            ls_municipio = funcoes_gerais.entidade(id_municipio)
            if len(ls_municipio)>0:
                municipio='Municipio(s): '+ls_municipio[0]
                nome_da_empresa = ls_municipio[1]
            else:
                municipio=''
                nome_da_empresa = ''

        if sel_empresa=='Aspec':
            lista_municipios=[85,34,42,182,109]
        elif sel_empresa=='Layout':
            lista_municipios=[125,52,76,162,98,57,177,119,174,107]
        elif sel_empresa=='SS':
            lista_municipios=[15,86,92,163,44,124,38,16]

        if 1==1:
            dictMunicipios=listagens.criarDictMunicipios()
            if id_municipio>0:
                query=Folhames.objects.filter(id_municipio=id_municipio).values('id_municipio','anomes','data_criacao').annotate(qtde=Count("id_folha")).order_by('id_municipio','anomes')
            elif sel_empresa!='Todas':
                query=Folhames.objects.filter(id_municipio__in=lista_municipios).values('id_municipio','anomes','data_criacao').annotate(qtde=Count("id_folha")).order_by('id_municipio','anomes')                
            else:
                query=Folhames.objects.values('id_municipio','anomes','data_criacao').annotate(qtde=Count("id_folha")).order_by('id_municipio','anomes')



            lista1=[]
            lista2=[]
            lista3=[]
            for kk in range(len(query)):
                lista1.append(str(query[kk]['id_municipio'])+':'+str(query[kk]['anomes']))
                lista2.append(query[kk]['qtde'])
                lista3.append(query[kk]['data_criacao'])

            dicionario=dict(zip(lista1,lista2))
            dicionario2=dict(zip(lista1,lista3))            


            if id_municipio>0:
                resumo=Folhaevento.objects.filter(tipo='V',id_municipio=id_municipio).values('id_municipio','anomes').annotate(valor_total=Sum("valor")).order_by('id_municipio','anomes')
            elif sel_empresa!='Todas':
                resumo=Folhaevento.objects.filter(tipo='V',id_municipio__in=lista_municipios).values('id_municipio','anomes').annotate(valor_total=Sum("valor")).order_by('id_municipio','anomes')
            else:
                resumo=Folhaevento.objects.filter(tipo='V').values('id_municipio','anomes').annotate(valor_total=Sum("valor")).order_by('id_municipio','anomes')


            #resumo
            #<QuerySet [{'id_municipio': 76, 'anomes': 202201, 'total': Decimal('2119447.46')}, {'id_municipio': 76, 'anomes': 202202, 'total': Decimal('2168637.07')}]>
            #data=Folhaevento.objects.filter(id_municipio=id_municipio,anomes=anomes).last()


            for res in resumo:
                contador+=1
                id_municipio=res['id_municipio']
                anomes=res['anomes']
                valor=res['valor_total']
                quantidade=dicionario[str(res['id_municipio'])+':'+str(res['anomes'])]
                data_criacao=dicionario2[str(res['id_municipio'])+':'+str(res['anomes'])]
                if data_criacao is not None:
                    data_criacao=data_criacao.strftime("%d/%m/%Y %H:%M:%S")
                else:
                    data_criacao=''                    

                lista.append(
                        {
                        'item':contador,
                        'municipio':dictMunicipios[id_municipio],
                        'mesref':str(anomes)[-2:]+'/'+str(anomes)[0:4],
                        'quantidade':quantidade,
                        'data_criacao':data_criacao,                        
                        'valor':formatMilhar(valor)
                        }
                    )
            lista_folha=lista  
            if nome_da_empresa!='':
                sel_empresa=nome_da_empresa


        
    return render(request, 'app01/folhasProcessadas.html',
        {
            'titulo': titulo,
            'municipios':municipios,
            'mensagem':'',
            'municipio':municipio,
            'lista_folha':lista_folha,
            'sel_empresa':'Empresa(s): '+sel_empresa
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
    lista=[]

    total=0
    total_v=0
    total_d=0
    total_r=0
    qT=0
    municipios = Municipio.objects.filter(empresa__in=['SS','Layout','Aspec']).order_by('municipio')

    if (request.method == "POST"):
        id_municipio=request.POST['municipio']
        ano=request.POST['ano']
        mes=request.POST['mes']
        modo_form=request.POST.getlist('modo')
        obj=Municipio.objects.get(id_municipio=id_municipio)
        municipio=obj.municipio

        anomes = int(ano+mes)
        referencia = mes+"/"+ano

        query=Folhaevento.objects.filter(id_municipio=id_municipio,anomes=anomes).values('id_evento').annotate(soma=Sum('valor'))        
        qtdeFuncionarios = Folhames.objects.filter(id_municipio=id_municipio,anomes=anomes).count()
        dicionarioEventos = listagens.criarDictIdEventosVantagens(id_municipio)

        lista1=[]
        lista2=[]
        for q in query:
            lista1.append(q['id_evento'])
            lista2.append(q['soma'])
        dicionarioValores = dict(zip(lista1,lista2))

        lista_eventos=[]
        lista_valores=[]

        for id_evento in dicionarioEventos:
            total_v+=dicionarioValores.get(id_evento,0)
            if dicionarioValores.get(id_evento,0)==0:
                continue

            total+=dicionarioValores[id_evento]

            lista_eventos.append(
                {
                    'evento':dicionarioEventos[id_evento],
                    'tipo':'(V)',
                    'valor':formatMilhar(dicionarioValores[id_evento])
                }
                )

        ls_municipio = funcoes_gerais.entidade(id_municipio)
        if len(ls_municipio)>0:
            municipio=ls_municipio[0]
            empresa = ls_municipio[1]
            entidade = ls_municipio[2]
        label_arquivo='Resumo_'+entidade+'_'+funcoes_gerais.mesPorExtenso(mes,1)+'_'+str(ano)+'.csv'

        lista=[]
        row=1

        if 'Excel' in modo_form:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename='+label_arquivo

            cabecalho = ['Evento','Valor']
            writer = csv.writer(response, delimiter=';')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow(cabecalho)
            row=1
            for ki in range(len(lista_eventos)):
                lista.append(lista_eventos[ki]['evento'])
                lista.append(lista_eventos[ki]['valor'])
                writer.writerow(lista)
                lista=[]
                row+=1


            ci="B2"
            cf='B'+str(row)
            formula="=soma("+ci+":"+cf+")"


            lista.append('T o t a l')
            lista.append(formula)
            writer.writerow(lista)

            return response
        else:
            lista=lista_eventos
            total_v=formatMilhar(total_v)
            qT=qtdeFuncionarios
    
    return render(request, 'app01/listSomaPorEventos.html',
            {
                'titulo': titulo,
                'eventos':lista,
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


