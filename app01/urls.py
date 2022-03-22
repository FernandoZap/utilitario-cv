from  django.urls import include, path
from django.contrib import admin
from . import views as v1

app_name = 'app01'

urlpatterns = [

    #path('listDepSetor', v1.listDepSetor, name='listDepSetor'),
    #path('setorList', v1.setorList, name='setorList'),
    #path('deptoList', v1.departamentoList, name='deptoList'),
    path('listFolhaResumo', v1.listFolhaResumo, name='listFolhaResumo'),
    #path('somaProventosDescontos', v1.somaProventosDescontos, name='somaProventosDescontos'),
    path('imprimirCSVFolha', v1.imprimirCSVFolha, name='imprimirCSVFolha'),
    #path('importacaoGeral', v1.importacaoGeral, name='importacaoGeral'),
    #path('importacaoFolha', v1.importacaoFolha, name='importacaoFolha'),
    #path('listFolha', v1.listFolha, name='listFolha'),
    #path('listFolha2', v1.listFolha2, name='listFolha2'),
    path('importacaoFolhaExcel', v1.importacaoFolhaExcel, name='importacaoFolhaExcel'),
    path('planilhaErrada', v1.planilhaErrada, name='planilhaErrada'),
    path('listSomaEventos', v1.listSomaEventos, name='listSomaEventos'),
]
